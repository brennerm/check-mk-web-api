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
class TestHosttags():

    @my_workingvcr
    def test_get_hosttags(self):
        assert api.get_hosttags()

        # make a set hosttags

    @my_workingvcr
    def test_set_hosttags(self):
        assert api.set_hosttags
