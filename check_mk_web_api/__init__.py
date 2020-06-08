import enum
import json
import os.path
import re
import ast

from six.moves import urllib

from check_mk_web_api.exception import CheckMkWebApiResponseException, CheckMkWebApiException, CheckMkWebApiAuthenticationException


class NoNoneValueDict(dict):
    """Dictionary that does not allow items with None as value"""
    def __init__(self, dictionary=None):
        super(NoNoneValueDict, self).__init__()
        if dictionary:
            for k, v in dictionary.items():
                self.__setitem__(k, v)

    def __setitem__(self, key, value):
        if value is not None:
            super(NoNoneValueDict, self).__setitem__(key, value)


class WebApi:
    """
    Abstraction for Check_Mk Web API

    # Arguments
    check_mk_url (str): URL to Check_Mk web application, multiple formats are supported
    username (str): Name of user to connect as. Make sure this is an automation user.
    secret (str): Secret for automation user. This is different from the password!

    # Examples
    ```python
    WebApi('http://checkmk.company.com/monitor/check_mk/webapi.py', 'automation', 'secret')
    ```
    ```python
    WebApi('http://checkmk.company.com/monitor/check_mk', 'automation', 'secret')
    ```
    ```python
    WebApi('http://checkmk.company.com/monitor', 'automation', 'secret')
    ```
    """

    __DISCOVERY_REGEX = {
        'added': [re.compile(r'.*Added (\d+),.*')],
        'removed': [re.compile(r'.*[Rr]emoved (\d+),.*')],
        'kept': [re.compile(r'.*[Kk]ept (\d+),.*')],
        'new_count': [re.compile(r'.*New Count (\d+)$'), re.compile(r'.*(\d+) new.*')]  # output changed in 1.6 so we have to try multiple patterns
    }

    class DiscoverMode(enum.Enum):
        """
        # Members
        NEW: Only discover new services
        REMOVE: Remove exceeding services
        FIXALL: Remove exceeding services and discover new services (Tabula Rasa)
        REFRESH: Start from scratch
        """
        NEW = 'new'
        REMOVE = 'remove'
        FIXALL = 'fixall'
        REFRESH = 'refresh'

    class ActivateMode(enum.Enum):
        """
        # Members
        DIRTY: Update sites with changes
        ALL: Update all slave sites
        SPECIFIC: Only update specified sites
        """
        DIRTY = 'dirty'
        ALL = 'all'
        SPECIFIC = 'specific'

    def __init__(self, check_mk_url, username, secret):
        check_mk_url = check_mk_url.rstrip('/')

        if check_mk_url.endswith('.py'):  # ends with /webapi.py
            self.web_api_base = check_mk_url
        elif check_mk_url.endswith('check_mk'):  # ends with /$SITE_NAME/check_mk
            self.web_api_base = os.path.join(check_mk_url, 'webapi.py')
        else:  # ends with /$SITE_NAME
            self.web_api_base = os.path.join(check_mk_url, 'check_mk', 'webapi.py')

        self.username = username
        self.secret = secret

    @staticmethod
    def __build_request_data(data, request_format):
        if not data:
            return None

        if request_format == 'json':
            request_string = 'request=' + json.dumps(data)
        elif request_format == 'python':
            request_string = 'request=' + str(data)

        request_string = urllib.parse.quote(request_string, safe="{[]}\"=, :")

        return request_string.encode()

    def __build_request_path(self, query_params=None):
        path = self.web_api_base + '?'

        if not query_params:
            query_params = {}

        query_params.update({
            '_username': self.username,
            '_secret': self.secret
        })

        query_string = urllib.parse.urlencode(query_params)

        path += query_string
        return path

    def make_request(self, action, query_params=None, data=None):
        """
        Make arbitrary request to Check_Mk Web API

        # Arguments
        action (str): Action request, e.g. add_host
        query_params (dict): dict of path parameters
        data (dict): dict that will be sent as request body

        # Raises
        CheckMkWebApiResponseException: Raised when the HTTP status code != 200
        CheckMkWebApiException: Raised when the action's result_code != 0
        """
        if not query_params:
            query_params = {}
        else:
            query_params = dict(query_params)  # work on copy

        query_params.update({'action': action})

        request_format = query_params.get('request_format', 'json')

        response = urllib.request.urlopen(
            self.__build_request_path(query_params),
            WebApi.__build_request_data(data, request_format)
        )

        if response.code != 200:
            raise CheckMkWebApiResponseException(response)

        body = response.read().decode()

        if body.startswith('Authentication error:'):
            raise CheckMkWebApiAuthenticationException(body)

        if 'output_format' in query_params and query_params['output_format'] == 'python':
            body_dict = ast.literal_eval(body)
        else:
            body_dict = json.loads(body)

        result = body_dict['result']
        if body_dict['result_code'] == 0:
            return result

        raise CheckMkWebApiException(result)

    def add_host(self, hostname, folder='/', ipaddress=None,
                 alias=None, tags=None, **custom_attrs):
        """
        Adds a nonexistent host to the Check_MK inventory

        # Arguments
        hostname (str): Name of host to add
        folder (str): Name of folder to add the host to
        ipaddress (str): IP address of host
        alias (str): Alias for host
        tags (dict): Dictionary of tags, prefix tag_ can be omitted
        custom_attrs (dict): dict that will get merged with generated attributes, mainly for compatibility reasons
        """
        data = NoNoneValueDict({
            'hostname': hostname,
            'folder': folder,
        })

        attributes = NoNoneValueDict()

        attributes['ipaddress'] = ipaddress
        attributes['alias'] = alias

        if tags:
            for tag, value in tags.items():
                prefix = 'tag_'
                if tag.startswith(prefix):
                    attributes[tag] = value
                else:
                    attributes[prefix + tag] = value

        attributes.update(custom_attrs)
        data['attributes'] = attributes

        return self.make_request('add_host', data=data)

    def edit_host(self, hostname, unset_attributes=None, **custom_attrs):
        """
        Edits the properties of an existing host

        # Arguments
        hostname (str): Name of host to edit
        unset_attributes (list): List of attributes to unset
        custom_attrs (dict): dict that will get merged with generated attributes, mainly for compatibility reasons
        """
        data = NoNoneValueDict(
            {
                'hostname': hostname,
                'unset_attributes': unset_attributes,
                'attributes': custom_attrs
            }
        )

        return self.make_request('edit_host', data=data)

    def delete_host(self, hostname):
        """
        Deletes a host from the Check_MK inventory

        # Arguments
        hostname (str): Name of host to delete
        """
        data = NoNoneValueDict({
            'hostname': hostname
        })

        return self.make_request('delete_host', data=data)

    def delete_hosts(self, hostnames):
        """
        Deletes multiple hosts from the Check_MK inventory

        # Arguments
        hostnames (list): Name of hosts to delete
        """
        data = NoNoneValueDict({
            'hostnames': hostnames
        })

        return self.make_request('delete_hosts', data=data)


    def delete_all_hosts(self):
        """
        Deletes all hosts from the Check_MK inventory
        """
        all_hosts = self.get_all_hosts()

        for hostname in all_hosts:
            self.delete_host(hostname)

    def get_host(self, hostname, effective_attributes=False):
        """
        Gets one host

        # Arguments
        hostname (str): Name of host to get
        effective_attributes (bool): If True attributes with default values will be returned
        """
        data = NoNoneValueDict({
            'hostname': hostname,
        })

        query_params = {
            'effective_attributes': 1 if effective_attributes else 0
        }

        return self.make_request('get_host', query_params=query_params, data=data)

    def get_all_hosts(self, effective_attributes=False):
        """
        Gets all hosts

        # Arguments
        effective_attributes (bool): If True attributes with default values will be returned
        """
        query_params = {
            'effective_attributes': 1 if effective_attributes else 0
        }

        return self.make_request('get_all_hosts', query_params=query_params)

    def get_hosts_by_folder(self, folder, effective_attributes=False):
        """
        Gets hosts in folder

        # Arguments
        folder (str): folder to get hosts for
        effective_attributes (bool): If True attributes with default values will be returned
        """
        hosts = {}

        for host, attr in self.get_all_hosts(effective_attributes).items():
            if attr['path'] == folder:
                hosts[host] = attr

        return hosts

    def discover_services(self, hostname, mode=DiscoverMode.NEW):
        """
        Discovers the services of a specific host

        # Arguments
        hostname (str): Name of host to discover services for
        mode (DiscoverMode): see #WebApi.DiscoverMode
        """
        data = NoNoneValueDict({
            'hostname': hostname,
        })

        query_params = {
            'mode': mode.value
        }

        result = self.make_request('discover_services', data=data, query_params=query_params)

        counters = {}
        for k, patterns in WebApi.__DISCOVERY_REGEX.items():
            for pattern in patterns:
                try:
                    counters[k] = pattern.match(result).group(1)
                except AttributeError:
                    continue

        return counters

    def discover_services_for_all_hosts(self, mode=DiscoverMode.NEW):
        """
        Discovers the services of all hosts

        # Arguments
        mode (DiscoverMode): see #WebApi.DiscoverMode
        """
        for host in self.get_all_hosts():
            self.discover_services(host, mode)

    def get_user(self, user_id):
        """
        Gets a single user

        # Arguments
        user_id (str): ID of user to get
        """
        return self.get_all_users()[user_id]

    def get_all_users(self):
        """
        Gets all users and their attributes
        """
        return self.make_request('get_all_users')

    def add_user(self, user_id, username, password, **custom_attrs):
        """
        Adds a new user

        # Arguments
        user_id (str): user ID that will be used to log in
        username (str): name of the user to create
        password (str): password that will be used to log in
        custom_attrs (dict): attributes that can be set for a user, look at output from #WebApi.get_all_users
        """
        data = NoNoneValueDict({
            'users': {
                user_id: {
                    'alias': username,
                    'password': password
                }
            }
        })

        data['users'][user_id].update(custom_attrs)

        return self.make_request('add_users', data=data)

    def add_automation_user(self,user_id, username, secret, **custom_attrs):
        """
        Adds a new automation user

        # Arguments
        user_id (str): user ID that will be used to log in
        username (str): name of the user to create
        secret (str): secret that will be used to log in
        custom_attrs (dict): attributes that can be set for a user, look at output from #WebApi.get_all_users
        """
        data = NoNoneValueDict({
            'users': {
                user_id: {
                    'alias': username,
                    'automation_secret': secret
                }
            }
        })

        data['users'][user_id].update(custom_attrs)

        return self.make_request('add_users', data=data)

    def edit_user(self, user_id, attributes, unset_attributes=None):
        """
        Edits an existing user

        # Arguments
        user_id (str): ID of user to edit
        attributes (dict): attributes to set for given host
        unset_attributes (list): list of attribute keys to unset
        """
        data = NoNoneValueDict({
            'users': {
                user_id: {
                    'set_attributes': attributes,
                    'unset_attributes': unset_attributes if unset_attributes else []
                }
            }
        })

        return self.make_request('edit_users', data=data)

    def delete_user(self, user_id):
        """
        Deletes a user

        # Arguments
        user_id (str): ID of user to delete
        """
        data = NoNoneValueDict({
            'users': [user_id]
        })

        return self.make_request('delete_users', data=data)

    def get_folder(self, folder, effective_attributes=False):
        """
        Gets one folder

        # Arguments
        folder (str): name of folder to get
        effective_attributes (bool): If True attributes with default values will be returned
        """
        data = NoNoneValueDict({
            'folder': folder
        })

        query_params = {
            'effective_attributes': 1 if effective_attributes else 0
        }

        return self.make_request('get_folder', data=data, query_params=query_params)

    def get_all_folders(self):
        """
        Gets all folders
        """
        return self.make_request('get_all_folders')

    def add_folder(self, folder, **attributes):
        """
        Adds a new folder

        # Arguments
        folder (str): name of folder to add
        attributes (dict): attributes to set for the folder, look at output from #WebApi.get_folder
        """
        data = NoNoneValueDict({
            'folder': folder,
            'attributes': attributes if attributes else {}
        })

        return self.make_request('add_folder', data=data)

    def edit_folder(self, folder, **attributes):
        """
        Edits an existing folder

        # Arguments
        folder (str): name of folder to edit
        attributes (dict): attributes to set for the folder, look at output from #WebApi.get_folder
        """
        data = NoNoneValueDict({
            'folder': folder,
            'attributes': attributes if attributes else {}
        })

        return self.make_request('edit_folder', data=data)

    def delete_folder(self, folder):
        """
        Deletes an existing folder

        # Arguments
        folder (str): name of folder to delete
        """
        data = NoNoneValueDict({
            'folder': folder
        })

        return self.make_request('delete_folder', data=data)

    def get_contactgroup(self, group):
        """
        Gets one contact group

        # Arguments
        group (str): name of contact group to get
        """
        return self.get_all_contactgroups()[group]

    def get_all_contactgroups(self):
        """
        Gets all contact groups
        """
        return self.make_request('get_all_contactgroups')

    def add_contactgroup(self, group, alias):
        """
        Adds a contact group

        # Arguments
        group (str): name of group to add
        alias (str): alias for group
        """
        data = NoNoneValueDict({
            'groupname': group,
            'alias': alias,
        })

        return self.make_request('add_contactgroup', data=data)

    def edit_contactgroup(self, group, alias):
        """
        Edits a contact group

        # Arguments
        group (str): name of group to edit
        alias (str): new alias for group
        """
        data = NoNoneValueDict({
            'groupname': group,
            'alias': alias,
        })

        return self.make_request('edit_contactgroup', data=data)

    def delete_contactgroup(self, group):
        """
        Deletes a contact group

        # Arguments
        group (str): name of group to delete
        """
        data = NoNoneValueDict({
            'groupname': group,
        })

        return self.make_request('delete_contactgroup', data=data)

    def delete_all_contactgroups(self):
        """
        Deletes all contact groups
        """
        for group in self.get_all_contactgroups():
            self.delete_contactgroup(group)

    def get_hostgroup(self, group):
        """
        Gets one host group

        # Arguments
        group (str): name of host group to get
        """
        return self.get_all_hostgroups()[group]

    def get_all_hostgroups(self):
        """
        Gets all host groups
        """
        return self.make_request('get_all_hostgroups')

    def add_hostgroup(self, group, alias):
        """
        Adds a host group

        # Arguments
        group (str): name of group to add
        alias (str): alias for group
        """
        data = NoNoneValueDict({
            'groupname': group,
            'alias': alias,
        })

        return self.make_request('add_hostgroup', data=data)

    def edit_hostgroup(self, group, alias):
        """
        Edits a host group

        # Arguments
        group (str): name of group to edit
        alias (str): new alias for group
        """
        data = NoNoneValueDict({
            'groupname': group,
            'alias': alias,
        })

        return self.make_request('edit_hostgroup', data=data)

    def delete_hostgroup(self, group):
        """
        Deletes a host group

        # Arguments
        group (str): name of group to delete
        """
        data = NoNoneValueDict({
            'groupname': group,
        })

        return self.make_request('delete_hostgroup', data=data)

    def delete_all_hostgroups(self):
        """
        Deletes all host groups
        """
        for group in self.get_all_hostgroups():
            self.delete_hostgroup(group)

    def get_servicegroup(self, group):
        return self.get_all_servicegroups()[group]

    def get_all_servicegroups(self):
        """
        Gets all service groups
        """
        return self.make_request('get_all_servicegroups')

    def add_servicegroup(self, group, alias):
        """
        Adds a service group

        # Arguments
        group (str): name of group to add
        alias (str): alias for group
        """
        data = NoNoneValueDict({
            'groupname': group,
            'alias': alias,
        })

        return self.make_request('add_servicegroup', data=data)

    def edit_servicegroup(self, group, alias):
        """
        Edits a service group

        # Arguments
        group (str): name of group to edit
        alias (str): new alias for group
        """
        data = NoNoneValueDict({
            'groupname': group,
            'alias': alias,
        })

        return self.make_request('edit_servicegroup', data=data)

    def delete_servicegroup(self, group):
        """
        Deletes a service group

        # Arguments
        group (str): name of group to delete
        """
        data = NoNoneValueDict({
            'groupname': group,
        })

        return self.make_request('delete_servicegroup', data=data)

    def delete_all_servicegroups(self):
        """
        Deletes all service groups
        """
        for group in self.get_all_servicegroups():
            self.delete_servicegroup(group)

    def get_ruleset(self, ruleset):
        """
        Gets one rule set

        # Arguments
        ruleset (str): name of rule set to get
        """
        data = NoNoneValueDict({
            'ruleset_name': ruleset,
        })

        return self.make_request('get_ruleset', data=data, query_params={'output_format': 'python'})

    def get_rulesets(self):
        """
        Gets all rule sets
        """
        return self.make_request('get_rulesets_info', query_params={'output_format': 'python'})

    def set_ruleset(self, ruleset, ruleset_config):
        """
        Edits one rule set

        # Arguments
        ruleset (str): name of rule set to edit
        ruleset_config (dict): config that will be set, have a look at return value of #WebApi.get_ruleset
        """
        data = NoNoneValueDict({
            'ruleset_name': ruleset,
            'ruleset': ruleset_config if ruleset_config else {}
        })

        return self.make_request('set_ruleset', data=data, query_params={'request_format': 'python'})

    def get_hosttags(self):
        """
        Gets all host tags
        """
        return self.make_request('get_hosttags')

    def set_hosttags(self, hosttags):
        """
        Sets host tags
   
        As implemented by Check_MK, it is only possible to write the whole Host Tag Settings within an API-Call
        You can use the #WebApi.get_hosttags to get the current Tags, modify them and write the dict back via set_hosttags  
        To ensure that no Tags are modified in the meantime you can use the configuration_hash key.

        e.g. 'configuration_hash': u'f31ea758a59473d15f378b692110996c'

        # Arguments
        hosttags (dict) with 2 mandatory keys:  { 'aux_tags' : [], 'tag_groups' : [] }
        """
        data = NoNoneValueDict(hosttags)

        return self.make_request('set_hosttags', data=data)

    def get_site(self, site_id):
        """
        Gets a site

        # Arguments
        site_id (str): ID of site to get
        """
        data = NoNoneValueDict({
            'site_id': site_id
        })

        return self.make_request('get_site', data=data, query_params={'output_format': 'python'})

    def set_site(self, site_id, site_config):
        """
        Edits the connection to a site

        # Arguments
        site_id (str): ID of site to edit
        site_config: config that will be set, have a look at return value of #WebApi.get_site
        """
        data = NoNoneValueDict({
            'site_id': site_id,
            'site_config': site_config if site_config else {}
        })

        return self.make_request('set_site', data=data, query_params={'request_format': 'python'})

    def delete_site(self, site_id):
        """
        Deletes a connection to a site

        # Arguments
        site_id (str): ID of site to delete the connection to
        """
        data = NoNoneValueDict({
            'site_id': site_id
        })

        return self.make_request('delete_site', data=data)

    def login_site(self, site_id, user, password):
        """
        Logs in to site

        # Arguments
        site_id (str): ID of site to log in to
        """
        data = NoNoneValueDict({
            'site_id': site_id,
            'username': user,
            'password': password
        })

        return self.make_request('login_site', data=data)

    def logout_site(self, site_id):
        """
        Logs out of site

        # Arguments
        site_id (str): ID of site to log out of
        """
        data = NoNoneValueDict({
            'site_id': site_id
        })

        return self.make_request('logout_site', data=data)

    def bake_agents(self):
        """
        Bakes all agents

        Enterprise Edition only!
        """
        return self.make_request('bake_agents')

    def activate_changes(self, mode=ActivateMode.DIRTY,
                         sites=None, allow_foreign_changes=False):
        """
        Activates all changes previously done

        # Arguments
        mode (ActivateMode): see #WebApi.ActivateMode
        sites (list): List of sites to activates changes on
        allow_foreign_changes (bool): If True changes of other users will be applied as well
        """
        data = NoNoneValueDict({
            'sites': sites
        })

        query_params = {
            'mode': mode.value,
            'allow_foreign_changes': 1 if allow_foreign_changes else 0
        }

        return self.make_request('activate_changes', query_params=query_params, data=data)
