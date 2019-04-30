from check_mk_web_api.web_api_base import WebApiBase


class WebApiAlerts(WebApiBase):
    def get_alerts(self):
        """
        Return current Alert Statuses

        """

        return self.make_view_name_request('alertstats')

    def ack_alerts(self, hostname, comment, serviceName):
        # acknowledge alerts
        base = {
            'host': hostname,
            'alert_comment': comment,
            'service': serviceName,
        }
        return self.make_request(base)
