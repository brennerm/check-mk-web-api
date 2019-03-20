from check_mk_web_api.web_api_base import WebApiBase
from check_mk_web_api.no_none_value_dict import NoNoneValueDict


class WebApiFolders(WebApiBase):

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
