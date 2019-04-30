import os

import pytest

from check_mk_web_api.web_api import WebApi
from tests import my_workingvcr

# from check_mk_web_api.exception import CheckMkWebApiException

api = WebApi(
    os.environ['CHECK_MK_URL'],
    os.environ['CHECK_MK_USER'],
    os.environ['CHECK_MK_SECRET']
)


# @pytest.mark.vcr()
class TestDowntimes():

    @my_workingvcr
    def test_no_error_on_all_downtimes(self):
        assert api.get_all_downtimes()

    @my_workingvcr
    def test_get_all_downtimes(self):
        expected_result = [
            ['host', 'service_description', 'downtime_origin', 'downtime_author', 'downtime_entry_time',
             'downtime_start_time', 'downtime_end_time', 'downtime_fixed', 'downtime_duration',
             'downtime_recurring', 'downtime_comment'],
            ['localhost', 'Check_MK Discovery', 'command', 'cmkadmin', '11 m', '11 m ago', 'in 108 m',
             'fixed', '', '(not supported)', 'downtime test 1'],
            ['localhost', 'Check_MK Discovery', 'command', 'cmkadmin', '11 m', '11 m ago', 'in 108 m',
             'fixed', '', '(not supported)', 'downtime test 2']
        ]

        result = api.get_all_downtimes()
        assert result == expected_result

    @my_workingvcr
    def test_set_downtime(self):
        hostname = "localhost"
        message = "downtime host for testing"
        down_time = 120
        result = api.set_downtime(hostname, message, down_time)

        expected_result = [
            ['sitealias', 'host', 'host_parents', 'host_childs', 'host_addresses', 'alias', 'host_icons', 'host_state',
             'host_plugin_output', 'host_pnpgraph', 'host_perf_data', 'host_in_downtime', 'num_services',
             'num_services_ok', 'num_services_warn', 'num_services_crit', 'num_services_unknown',
             'num_services_pending', 'host_attempt', 'host_state_age', 'host_check_age', 'host_next_check',
             'host_check_latency', 'host_check_duration', 'host_notifper', 'host_in_notifper',
             'host_notification_number', 'host_last_notification', 'host_next_notification',
             'host_notification_postponement_reason', 'host_check_interval', 'host_contact_groups', 'host_contacts',
             'host_group_memberlist', 'host_servicelevel', 'host_check_command', 'host_custom_vars',
             'host_custom_notes'],
            ['alias_green', 'localhost', '', '', '127.0.0.1', 'localhost',
             'themes/facelift/images/icon_menu themes/facelift/images/icon_pnp derived_downtime comment',
             'UP', 'OK - 127.0.0.1: rta 0.008ms, lost 0%',
             "render_pnp_graphs('checkmd2_localhost__HOST__graph', 'checkmd2', 'localhost', '_HOST_', '1', '/checkmd2/check_mk/', '../pnp4nagios/', false, 'Add this graph to...', null, null, 'facelift')",
             'rta=0.008ms;200.000;500.000;0; pl=0%;80;100;; rtmax=0.029ms;;;; rtmin=0.002ms;;;;',
             'yes', '2', '1', '0', '1', '0', '0', '1/1', '24 h', '24.7 s', 'in 36.3 s',
             '113 ms', '2.57 ms', '24X7', 'yes', '0', '-', '-', 'None', '60 s / 60 s',
             'check-mk-notify, all', 'check-mk-notify', 'check_mk', '',
             'check-mk-host-ping!-w 200.00,80.00% -c 500.00,100.00%', '', '']
        ]
        assert result == expected_result

    @my_workingvcr
    def test_get_failed_notifications(self):
        result = api.get_failed_notifications()
        expected_result = [['log_icon',
                            'log_time',
                            'log_contact_name',
                            'log_command',
                            'log_type',
                            'host',
                            'service_description',
                            'log_state',
                            'log_plugin_output',
                            'log_comment']]

        assert result == expected_result
