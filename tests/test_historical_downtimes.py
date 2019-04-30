import os
import pytest

from check_mk_web_api.web_api import WebApi
from tests import my_workingvcr

api = WebApi(
    os.environ['CHECK_MK_URL'],
    os.environ['CHECK_MK_USER'],
    os.environ['CHECK_MK_SECRET']
)


# @pytest.mark.vcr()
class TestHistoricalDowntimes():

    @my_workingvcr
    def test_view_historical_downtimes(self):
        result = api.view_historical_downtimes()
        assert result

    @my_workingvcr
    def test_historical_downtimes(self):
        result = api.view_historical_downtimes()
        expected_result = [[
                "log_icon",
                "log_time",
                "host",
                "service_description",
                "log_state_type",
                "log_plugin_output"
            ],
            [
                "",
                "44 h",
                "localhost",
                "Check_MK Discovery",
                "STOPPED",
                " Service has exited from a period of scheduled downtime"
            ],
            [
                "",
                "46 h",
                "localhost",
                "Check_MK Discovery",
                "STARTED",
                " Service has entered a period of scheduled downtime"
            ],
            [
                "",
                "21 h",
                "localhost",
                "",
                "STOPPED",
                " Host has exited from a period of scheduled downtime"
            ],
            [
                "",
                "23 h",
                "localhost",
                "",
                "STARTED",
                " Host has entered a period of scheduled downtime"
            ]
        ]

        assert result == expected_result


