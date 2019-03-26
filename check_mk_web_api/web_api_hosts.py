from check_mk_web_api.discover_mode import DiscoverMode
from check_mk_web_api.no_none_value_dict import NoNoneValueDict
from check_mk_web_api.web_api_base import WebApiBase


class WebApiHosts(WebApiBase):
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
        for k, regex in WebApi.__DISCOVERY_REGEX.items():
            counters[k] = regex.match(result).group(1)

        return counters

    def discover_services_for_all_hosts(self, mode=DiscoverMode.NEW):
        """
        Discovers the services of all hosts

        # Arguments
        mode (DiscoverMode): see #WebApi.DiscoverMode
        """
        for host in self.get_all_hosts():
            self.discover_services(host, mode)
