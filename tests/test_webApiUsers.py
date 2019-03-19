import os
import random
import string

import pytest
from check_mk_web_api.web_api_users import WebApiUsers

from check_mk_web_api.exception import CheckMkWebApiException

api = WebApiUsers(
    os.environ['CHECK_MK_URL'],
    os.environ['CHECK_MK_USER'],
    os.environ['CHECK_MK_SECRET']
)


@pytest.mark.vcr()
class TestUsers():
    def setup(self):

        for user_id in api.get_all_users():
            if user_id != 'cmkadmin' and user_id != os.environ['CHECK_MK_USER']:
                api.delete_user(user_id)

    def test_get_user(self):
        api.add_user('user00', 'User 00', 'p4ssw0rd')
        assert api.get_user('user00')['alias'] == 'User 00'

#
    def test_get_all_users(self):
        api.add_user('user00', 'User 00', 'p4ssw0rd')
        api.add_user('user01', 'User 01', 'p4ssw0rd')

        users = api.get_all_users()
        assert 'user00' in users
        assert 'user01' in users

#
    def test_add_user(self):
        api.add_user('user00', 'User 00', 'p4ssw0rd')
        assert 'user00' in api.get_all_users()
#
#
    def test_add_automation_user(self):
        api.add_automation_user('automation00', 'Automation 00', 's3cr3t1234')
        assert 'automation00' in api.get_all_users()
#
#
    def test_add_duplicate_user(self):
        with pytest.raises(CheckMkWebApiException):
            api.add_user('user00', 'User 00', 'p4ssw0rd')
            api.add_user('user00', 'User 00', 'p4ssw0rd')
#
#
    def test_add_duplicate_automation_user(self):
        with pytest.raises(CheckMkWebApiException):
            api.add_automation_user('automation00', 'Automation 00', 's3cr3t1234')
            api.add_automation_user('automation00', 'Automation 00', 's3cr3t1234')
#
#
    def test_edit_user(self):
        api.add_user('user00', 'User 00', 'p4ssw0rd')
        assert api.get_all_users()['user00']['alias'] == 'User 00'

        api.edit_user('user00', {'alias': 'User 0'})
        assert api.get_all_users()['user00']['alias'] == 'User 0'
#
#
    def test_unset_user_attribute(self):
        api.add_user('user00', 'User 00', 'p4ssw0rd', pager='49123456789')
        assert api.get_all_users()['user00']['pager'] == '49123456789'
        api.edit_user('user00', {}, unset_attributes=['pager'])
        assert 'pager' not in api.get_all_users()['user00']
#
#
    def test_edit_nonexistent_user(self):
        with pytest.raises(CheckMkWebApiException):
            api.edit_user('user00', {})

#
    def test_delete_user(self):
        api.add_user('user00', 'User 00', 'p4ssw0rd')
        assert 'user00' in api.get_all_users()

        api.delete_user('user00')
        assert 'user00' not in api.get_all_users()

#
    def test_delete_nonexistent_user(self):
        with pytest.raises(CheckMkWebApiException):
            api.delete_user('user00')

# def test_get_contactgroup():
#     api.add_contactgroup('user', 'User')
#     assert api.get_contactgroup('user')
#
#
# def test_get_all_contactgroups():
#     api.add_contactgroup('user', 'User')
#     api.add_contactgroup('admin', 'Admin')
#     groups = api.get_all_contactgroups()
#     assert 'user' in groups
#     assert 'admin' in groups
#
#
# def test_get_nonexistent_contactgroup():
#     with pytest.raises(KeyError):
#         api.get_contactgroup('user')
#
#
# def test_add_contactgroup():
#     api.add_contactgroup('user', 'User')
#     assert api.get_contactgroup('user')['alias'] == 'User'
#
#
# def test_add_duplicate_contactgroup():
#     with pytest.raises(CheckMkWebApiException):
#         api.add_contactgroup('user', 'User')
#         api.add_contactgroup('user', 'User')
#
#
# def test_edit_contactgroup():
#     api.add_contactgroup('user', 'User')
#     assert api.get_contactgroup('user')['alias'] == 'User'
#     api.edit_contactgroup('user', 'Users')
#     assert api.get_contactgroup('user')['alias'] == 'Users'
#
#
# def test_edit_nonexisting_contactgroup():
#     with pytest.raises(CheckMkWebApiException):
#         api.edit_contactgroup('user', 'Users')
#
#
# def test_delete_contactgroup():
#     api.add_contactgroup('user', 'User')
#     assert 'user' in api.get_all_contactgroups()
#     api.delete_contactgroup('user')
#     assert 'user' not in api.get_all_contactgroups()
#
#
# def test_delete_nonexistent_contactgroup():
#     with pytest.raises(CheckMkWebApiException):
#         api.delete_contactgroup('user')
