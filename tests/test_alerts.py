import os
import random
import string

import pytest

from check_mk_web_api.web_api_base import WebApiBase
from check_mk_web_api.web_api_alerts import WebApiAlerts

api = WebApiAlerts(
    os.environ['CHECK_MK_URL'],
    os.environ['CHECK_MK_USER'],
    os.environ['CHECK_MK_SECRET']
)


class TestAlerts():



        def test_get_alerts(self):
            assert api.get_alerts()