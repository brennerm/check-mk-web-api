import os
import random
import string

import pytest

from check_mk_web_api.web_api_base import WebApiBase
from check_mk_web_api.web_api_hosttags import WebApiHosttags
from check_mk_web_api.exception import CheckMkWebApiException

api = WebApiHosttags(
    os.environ['CHECK_MK_URL'],
    os.environ['CHECK_MK_USER'],
    os.environ['CHECK_MK_SECRET']
)

@pytest.mark.vcr()
class TestHosttags():


    def test_get_hosttags(self):
        assert api.get_hosttags()

        #make a set hosttags
    def test_set_hosttags(self):
        assert api.set_hosttags

