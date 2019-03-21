from check_mk_web_api.web_api_base import WebApiBase
from check_mk_web_api.no_none_value_dict import NoNoneValueDict


class WebApiSite(WebApiBase):

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
