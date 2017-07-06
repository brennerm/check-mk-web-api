import enum
import json
import os.path
import re
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
        'added': re.compile(r'.*Added (\d+),.*'),
        'removed': re.compile(r'.*Removed (\d+),.*'),
        'kept': re.compile(r'.*Kept (\d+),.*'),
        'new_count': re.compile(r'.*New Count (\d+)$')
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
    def __build_request_data(data):
        if not data:
            return None
        return ('request=' + json.dumps(data)).encode()

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
        Makes arbitrary request to Check_Mk Web API

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

        response = urllib.request.urlopen(
            self.__build_request_path(query_params),
            WebApi.__build_request_data(data)
        )

        if response.code != 200:
            raise CheckMkWebApiResponseException(response)

        body = response.read().decode()

        if body.startswith('Authentication error:'):
            raise CheckMkWebApiAuthenticationException(body)

        body_json = json.loads(body)
        result = body_json['result']

        if body_json['result_code'] == 0:
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

    def get_host(self, hostname, effective_attributes=False):
        """
        Gets information about one host

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
        Gets information about all hosts

        # Arguments
        effective_attributes (bool): If True attributes with default values will be returned
        """
        query_params = {
            'effective_attributes': 1 if effective_attributes else 0
        }

        return self.make_request('get_all_hosts', query_params=query_params)

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
        for k, regex in WebApi.__DISCOVERY_REGEX.items():
            counters[k] = regex.match(result).group(1)

        return counters

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
