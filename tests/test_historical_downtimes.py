import os
import pytest
from tests import filter_uri
from check_mk_web_api.web_api import WebApi

api = WebApi(
    os.environ['CHECK_MK_URL'],
    os.environ['CHECK_MK_USER'],
    os.environ['CHECK_MK_SECRET']
)


class TestHistoricalDowntimes():

    @filter_uri
    def test_view_historical_downtimes(self):
        result = api.view_historical_downtimes()
        assert result

    @filter_uri
    def test_historical_downtimes(self):
        result = api.view_historical_downtimes()
        expected_result = [[
                "log_icon",
                "log_time",
                "host",
                "service_description",
                "log_state_type",
                "log_plugin_output"],

        ]

        assert result == expected_result


