import os

import pytest

from check_mk_web_api.web_api import WebApi

# from check_mk_web_api.exception import CheckMkWebApiException

api = WebApi(
    os.environ['CHECK_MK_URL'],
    os.environ['CHECK_MK_USER'],
    os.environ['CHECK_MK_SECRET']
)


@pytest.mark.vcr()
class TestDowntimes():

    def test_no_error_on_all_downtimes(self):
        assert api.get_all_downtimes()

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

    @pytest.mark.skip('incomplete code')
    def test_set_downtime(self):
        hostname = "localhost"
        message = "downtime host for testing"
        down_time = 120
        result = api.set_downtime(hostname, message, down_time)
        print(result)
        assert False
