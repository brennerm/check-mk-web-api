from check_mk_web_api.web_api_base import WebApiBase


class WebApiContactGroup(WebApiBase):

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
