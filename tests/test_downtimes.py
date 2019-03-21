import os
import random
import string

import pytest

from check_mk_web_api.web_api_base import WebApiBase
from check_mk_web_api.web_api_downtimes import WebApiDowntimes
# from check_mk_web_api.exception import CheckMkWebApiException

api = WebApiDowntimes(
    os.environ['CHECK_MK_URL'],
    os.environ['CHECK_MK_USER'],
    os.environ['CHECK_MK_SECRET']
)

@pytest.mark.vcr()
class TestDowntimes():

    def test_get_all_downtimes(self):
        result = api.get_all_downtimes()
        assert api.get_all_downtimes()

    @pytest.mark.skip
    def test_set_downtime(self):
            hostname="hostname"
            message="downtime host for testing"
            serviceName="downtime name"
            result = api.set_downtime(hostname, message, serviceName)
            assert api.set_downtime(hostname, message, serviceName)

