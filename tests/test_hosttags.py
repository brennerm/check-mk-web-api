import os
from tests import filter_uri
import pytest

from check_mk_web_api.web_api import WebApi

api = WebApi(
    os.environ['CHECK_MK_URL'],
    os.environ['CHECK_MK_USER'],
    os.environ['CHECK_MK_SECRET']
)


class TestHosttags():

    @filter_uri
    def test_get_hosttags(self):
        assert api.get_hosttags()

    @pytest.mark.skip('incomplete code')
    def test_set_hosttags(self):
        assert api.set_hosttags('hosttags')

