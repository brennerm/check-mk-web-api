from check_mk_web_api.web_api_base import WebApiBase


class WebApiDowntimes(WebApiBase):
    def get_all_downtimes(self):
        """
        Gets list of downtimes from CheckMk

        """

        return self.make_view_name_request('downtimes')

    def set_downtime(self, hostname, message, down_time=120):
        """
        Sets Downtime for host with message

        # Arguments
        hostname: Name of the host to set downtime on
        message: Message to set for downtime
        downTime: minutes of downtime
        serviceName: Name of service to down
        """

        url_params = {
            '_do_confirm': 'yes',
            '_transid': -1,
            '_do_actions': 'yes',
            'host': hostname,
            # 'site': None,
            'view_name': 'hoststatus',
            # '_down_2h': '2+hours',
            '_down_comment': 'THISISWORKING',
            '_down_minutes': 120,
            'output_format': 'json'
        }

        return self.make_view_request(url_params)

    def view_historical_downtimes(self):

        """Get Historical Downtimes"""

        return self.make_view_name_request('downtime_history')