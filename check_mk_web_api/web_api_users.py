from check_mk_web_api.web_api_base import WebApiBase
from check_mk_web_api.no_none_value_dict import NoNoneValueDict

class WebApiUsers(WebApiBase):

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

    def add_automation_user(self, user_id, username, secret, **custom_attrs):
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
