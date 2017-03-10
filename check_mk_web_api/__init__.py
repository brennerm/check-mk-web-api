import enum
import json
import os.path
import re
import urllib.parse
import urllib.request

from check_mk_web_api.exception import CheckMkWebApiResponseException, CheckMkWebApiException


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
    """Abstraction for Check_Mk Web API"""

    DISCOVERY_REGEX = {
        'added': re.compile(r'.*Added (\d+),.*'),
        'removed': re.compile(r'.*Removed (\d+),.*'),
        'kept': re.compile(r'.*Kept (\d+),.*'),
        'new_count': re.compile(r'.*New Count (\d+)$')
    }

    class DiscoverMode(enum.Enum):
        """
        new - Only discover new services
        remove - Remove exceeding services
        fixall - Remove exceeding services and discover new services
        refresh - Start from scratch
        """
        NEW = 'new'
        REMOVE = 'remove'
        FIXALL = 'fixall'
        REFRESH = 'refresh'

    class ActivateMode(enum.Enum):
        """
        dirty - Update sites with changes
        all - Update all slave sites
        specific - Only update specified sites
        """
        DIRTY = 'dirty'
        ALL = 'all'
        SPECIFIC = 'specific'

    def __init__(self, check_mk_url: str, username: str, secret: str):
        """
        :param check_mk_url: URL to Check_Mk web application, multiple formats are supported
        :param username: Name of user to connect as, make sure this is an automation user
        :param secret: Secret for automation user, this is not a password!
        """
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
    def __build_request_data(data: dict):
        if not data:
            return None
        return ('request=' + json.dumps(data)).encode()

    def __build_request_path(self, query_params: dict=None):
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

    def make_request(self, action: str, query_params: dict=None, data: dict=None):
        """
        Makes arbitrary request to Check_Mk Web API

        :param action: Action request, e.g. add_host
        :param query_params: dict of path parameters
        :param data: dict that will be sent as request body

        :raises CheckMkWebApiResponseException if HTTP status code != 200
        :raises CheckMkWebApiException if result_code != 0
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

        if response.status != 200:
            raise CheckMkWebApiResponseException(response)

        body = json.loads(response.read().decode())
        result = body['result']

        if body['result_code'] == 0:
            return result

        raise CheckMkWebApiException(result)

    def add_host(self, hostname: str, folder: str='/', ipaddress: str=None,
                 alias: str=None, tags: dict=None, **custom_attrs):
        """
        Executes add_host action on Check_Mk Web API

        :param hostname: Name of host to add
        :param folder: Name of folder to add the host to
        :param ipaddress: IPv4 address of host
        :param alias: Alias for host
        :param tags: List of tags, prefix tag_ can be omitted
        :param custom_attrs: dict that will get merged with generated attributes, mainly for compatibility reasons
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

    def edit_host(self, hostname: str, unset_attributes: list=None, **custom_attrs):
        """
        Executes edit_host action on Check_Mk Web API

        :param hostname: Name of host to edit
        :param unset_attributes: List of attributes to unset
        :param custom_attrs: dict that will get merged with generated attributes, mainly for compatibility reasons
        """
        data = NoNoneValueDict(
            {
                'hostname': hostname,
                'unset_attributes': unset_attributes,
                'attributes': custom_attrs
            }
        )

        return self.make_request('edit_host', data=data)

    def delete_host(self, hostname: str):
        """
        Executes delete_host action on Check_Mk Web API

        :param hostname: Name of host to delete
        """
        data = NoNoneValueDict({
            'hostname': hostname
        })

        return self.make_request('delete_host', data=data)

    def get_host(self, hostname: str, effective_attributes: bool=False):
        """
        Executes get_host action on Check_Mk Web API

        :param hostname: Name of host to get
        :param effective_attributes: If True attributes with default values will be returned
        """
        data = NoNoneValueDict({
            'hostname': hostname,
        })

        query_params = {
            'effective_attributes': 1 if effective_attributes else 0
        }

        return self.make_request('get_host', query_params=query_params, data=data)

    def get_all_hosts(self, effective_attributes: bool=False):
        """
        Executes get_all_hosts action on Check_Mk Web API

        :param effective_attributes: If True attributes with default values will be returned
        """
        query_params = {
            'effective_attributes': 1 if effective_attributes else 0
        }

        return self.make_request('get_all_hosts', query_params=query_params)

    def discover_services(self, hostname: str, mode: DiscoverMode=DiscoverMode.NEW):
        """
        Executes discover_services action on Check_Mk Web API

        :param hostname: Name of host to discover services for
        :param mode: see WebApi.DiscoverMode
        """
        data = NoNoneValueDict({
            'hostname': hostname,
        })

        query_params = {
            'mode': mode.value
        }

        result = self.make_request('discover_services', data=data, query_params=query_params)

        counters = {}
        for k, regex in WebApi.DISCOVERY_REGEX.items():
            counters[k] = regex.match(result).group(1)

        return counters

    def bake_agents(self):
        """
        Executes bake_agents action on Check_Mk Web API

        Enterprise Edition only
        """
        return self.make_request('bake_agents')

    def activate_changes(self, mode: ActivateMode=ActivateMode.DIRTY,
                         sites: list=None, allow_foreign_changes: bool=False):
        """
        Executes activate_changes action on Check_Mk Web API

        :param mode: see WebApi.ActivateMode
        :param sites: List of sites to activates changes on
        :param allow_foreign_changes: If True foreign changes will be applied as well
        """
        data = NoNoneValueDict({
            'sites': sites
        })

        query_params = {
            'mode': mode.value,
            'allow_foreign_changes': 1 if allow_foreign_changes else 0
        }

        return self.make_request('activate_changes', query_params=query_params, data=data)
