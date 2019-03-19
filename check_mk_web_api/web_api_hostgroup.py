from check_mk_web_api.web_api_base import WebApiBase
from check_mk_web_api.no_none_value_dict import NoNoneValueDict


class WebApiHostGroup(WebApiBase):

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
