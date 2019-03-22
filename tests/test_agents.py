import os
import random
import string

import pytest

from check_mk_web_api.web_api import WebApi
from check_mk_web_api.web_api_agents import WebApiAgents
from check_mk_web_api.exception import CheckMkWebApiException

api = WebApi(
    os.environ['CHECK_MK_URL'],
    os.environ['CHECK_MK_USER'],
    os.environ['CHECK_MK_SECRET']
)


@pytest.mark.vcr()
class TestAgents():
    @pytest.mark.skip('bake agents only works on enterprise editions. is not working on public edition')
    def test_bake_agents(self):
        result = api.bake_agents()
        assert result
