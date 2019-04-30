import os

import pytest

from check_mk_web_api.exception import CheckMkWebApiException
from check_mk_web_api.web_api import WebApi
from tests import my_workingvcr

api = WebApi(
    os.environ['CHECK_MK_URL'],
    os.environ['CHECK_MK_USER'],
    os.environ['CHECK_MK_SECRET']
)

# @pytest.mark.vcr()
class TestContactGroups() :
    def setup(self):

        for group in api.get_all_contactgroups():
            if group != 'all':
                api.delete_contactgroup(group)

    @my_workingvcr
    def test_get_contactgroup(self):
        api.add_contactgroup('user', 'User')
        assert api.get_contactgroup('user')

    @my_workingvcr
    def test_get_all_contactgroups(self):
        api.add_contactgroup('user', 'User')
        api.add_contactgroup('admin', 'Admin')
        groups = api.get_all_contactgroups()
        assert 'user' in groups
        assert 'admin' in groups

    @my_workingvcr
    def test_get_nonexistent_contactgroup(self):
        with pytest.raises(KeyError):
            api.get_contactgroup('user')

    @my_workingvcr
    def test_add_contactgroup(self):
        api.add_contactgroup('user', 'User')
        assert api.get_contactgroup('user')['alias'] == 'User'

    @my_workingvcr
    def test_add_duplicate_contactgroup(self):
        with pytest.raises(CheckMkWebApiException):
            api.add_contactgroup('user', 'User')
            api.add_contactgroup('user', 'User')

    @my_workingvcr
    def test_edit_contactgroup(self):
        api.add_contactgroup('user', 'User')
        assert api.get_contactgroup('user')['alias'] == 'User'
        api.edit_contactgroup('user', 'Users')
        assert api.get_contactgroup('user')['alias'] == 'Users'

    @my_workingvcr
    def test_edit_nonexisting_contactgroup(self):
        with pytest.raises(CheckMkWebApiException):
            api.edit_contactgroup('user', 'Users')

    @my_workingvcr
    def test_delete_contactgroup(self):
        api.add_contactgroup('user', 'User')
        assert 'user' in api.get_all_contactgroups()
        api.delete_contactgroup('user')
        assert 'user' not in api.get_all_contactgroups()

    @my_workingvcr
    def test_delete_nonexistent_contactgroup(self):
        with pytest.raises(CheckMkWebApiException):
            api.delete_contactgroup('user')
