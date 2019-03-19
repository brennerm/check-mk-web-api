from check_mk_web_api.web_api_base import WebApiBase


class WebApiAlerts(WebApiBase):

    def get_alerts(self):
        """
        Return current Alert Statists

        """

        return self.make_view_name_request('alertstats')
