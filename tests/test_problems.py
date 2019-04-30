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
class TestProblems():

    @my_workingvcr
    def test_get_svc_problems(self):
        assert api.get_svc_problems

