import os
import pytest
from check_mk_web_api.exception import CheckMkWebApiException
from check_mk_web_api.web_api import WebApi
from tests import scrub_string

api = WebApi(
    os.environ['CHECK_MK_URL'],
    os.environ['CHECK_MK_USER'],
    os.environ['CHECK_MK_SECRET']
)

@pytest.fixture(scope='module')
def vcr_config():
    return {
        # Replace the Authorization request header with "DUMMY" in cassettes
        'before_record': scrub_string("_secret", "_username"),
    }

@pytest.mark.vcr
class TestRuleset():

    # @filter_uri
    def test_get_ruleset(self):
        assert api.get_ruleset('checkgroup_parameters:hw_fans_perc')

    # @filter_uri
    # def test_get_nonexistent_rulesets(self):
    #     with pytest.raises(CheckMkWebApiException):
    #         api.get_ruleset('nonexistent')
    #
    # @filter_uri
    # def test_set_nonexistent_rulesets(self):
    #     with pytest.raises(CheckMkWebApiException):
    #         api.set_ruleset('nonexistent', {})
    #
    # @filter_uri
    # def test_get_rulesets(self):
    #     assert api.get_rulesets()
