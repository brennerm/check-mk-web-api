import os
import random
import string

import pytest

from check_mk_web_api.web_api_base import WebApiBase
from check_mk_web_api.web_api_ruleset import WebApiRuleset
from check_mk_web_api.exception import CheckMkWebApiException

api = WebApiRuleset(
    os.environ['CHECK_MK_URL'],
    os.environ['CHECK_MK_USER'],
    os.environ['CHECK_MK_SECRET']
)

@pytest.mark.vcr()
class TestRuleset():

#     for group in api.get_all_contactgroups():
#         if group != 'all':
#             api.delete_contactgroup(group)
#
#     for user_id in api.get_all_users():
#         if user_id != 'cmkadmin' and user_id != os.environ['CHECK_MK_USER']:
#             api.delete_user(user_id)
#
#     for folder in api.get_all_folders():
#         if folder != '':
#             api.delete_folder(folder)
# #
    def test_get_ruleset(self):
        assert api.get_ruleset('checkgroup_parameters:hw_fans_perc')

# #
    def test_get_nonexistent_rulesets(self):
        with pytest.raises(CheckMkWebApiException):
            api.get_ruleset('nonexistent')

#
    def test_set_nonexistent_rulesets(self):
        with pytest.raises(CheckMkWebApiException):
            api.set_ruleset('nonexistent', {})
#
# #
    def test_get_rulesets(self):
        assert api.get_rulesets()
# #
#
# def test_get_site():
#     assert api.get_site('cmk')
#
#
# def test_set_site():
#     random_alias = 'alias_' + ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
#     config = api.get_site('cmk')['site_config']
#     config['alias'] = random_alias
#
#     api.set_site('cmk', config)
#     assert api.get_site('cmk')['site_config']['alias'] == random_alias
#
#
# @pytest.mark.skip(reason="bug in Check_Mk")
# def test_login_site():
#     api.add_user('user00', 'User 00', 'p4ssw0rd')
#     api.login_site('cmk', 'user00', 'p4ssw0rd')
#
#
# @pytest.mark.skip(reason="bug in Check_Mk")
# def test_logout_site():
#     api.add_user('user00', 'User 00', 'p4ssw0rd')
#     api.login_site('cmk', 'user00', 'p4ssw0rd')
#     api.logout_site('cmk')
