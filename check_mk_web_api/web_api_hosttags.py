from check_mk_web_api.web_api_base import WebApiBase


class WebApiHosttags(WebApiBase):

    def get_hosttags(self):
        """
        Gets all host tags
        """
        return self.make_request('get_hosttags')

    def set_hosttags(self, hosttags):
        """
        Sets host tags

        # Arguments
        hosttags (dict): new host tags that will be set, have a look at return value of #WebApi.get_hosttags
        """
        data = NoNoneValueDict({
            hosttags
        })

        return self.make_request('set_hosttags', data=data)
