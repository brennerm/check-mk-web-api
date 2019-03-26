from check_mk_web_api.web_api_base import WebApiBase


class WebApiProblems(WebApiBase):

    def get_svc_problems(self):
        """
        Get current SVC problems

        """

        return self.make_view_name_request('svcproblems')
