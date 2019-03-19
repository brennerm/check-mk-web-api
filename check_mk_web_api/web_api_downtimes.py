from check_mk_web_api.web_api_base import WebApiBase


class WebApiDowntimes(WebApiBase):
    def get_all_downtimes(self):
        """
        Gets list of downtimes from CheckMk

        """

        return self.make_view_name_request('downtimes')

    def set_downtime(self, hostname, message, serviceName, downTime=120):
        """
        Sets Downtime for host with message

        # Arguments
        hostname: Name of the host to set downtime on
        message: Message to set for downtime
        downTime: minutes of downtime
        serviceName: Name of service to down
        """

        base = {
            '_do_confirm': 'yes',
            '_transid': -1,
            '_do_actions': 'yes',
            'service': serviceName,
            'host': hostname,
            'site': siteName,
            'viewname': 'service',
            '_down_minutes': downTime,
            '_down_comment': message,

        }

        query_param = self.__check_query_params(base)

        return self.make_request()
