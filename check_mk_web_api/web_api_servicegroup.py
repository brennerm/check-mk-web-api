from check_mk_web_api.no_none_value_dict import NoNoneValueDict
from check_mk_web_api.web_api_base import WebApiBase


class WebApiServiceGroup(WebApiBase):

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

    def get_all_services(self):
        return self.make_view_request("allservices")

    def get_pending_services(self):
        return self.make_view_request("pendingsvc")