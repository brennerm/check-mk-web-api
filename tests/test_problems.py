import os
import random
import string

import pytest

from check_mk_web_api.web_api_base import WebApiBase
from check_mk_web_api.web_api_problems import WebApiProblems
# from check_mk_web_api.exception import CheckMkWebApiException

api = WebApiProblems(
    os.environ['CHECK_MK_URL'],
    os.environ['CHECK_MK_USER'],
    os.environ['CHECK_MK_SECRET']
)


@pytest.mark.vcr()
class TestProblems():

    def test_get_svc_problems(self):
        assert api.get_svc_problems

