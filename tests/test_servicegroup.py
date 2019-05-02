import os

import pytest
from tests import my_workingvcr

from check_mk_web_api.exception import CheckMkWebApiException
from check_mk_web_api.web_api import WebApi

api = WebApi(
    os.environ["CHECK_MK_URL"],
    os.environ["CHECK_MK_USER"],
    os.environ["CHECK_MK_SECRET"],
)


# @pytest.mark.vcr()
class TestServiceGroup:
    def setup(self):
        api.delete_all_servicegroups()


    @pytest.mark.skip('bad cassette, will not find url currently')
    def test_get_servicegroup(self):
        api.add_servicegroup('db', 'Database')
        assert api.get_servicegroup('db')

    @pytest.mark.skip('bad cassette, will not find url currently')
    def test_get_all_servicegroups(self):
        api.add_servicegroup('db', 'Database')
        api.add_servicegroup('web', 'Webserver')
        groups = api.get_all_servicegroups()
        assert 'db' in groups
        assert 'web' in groups

    @my_workingvcr
    def test_get_nonexistent_servicegroup(self):
        with pytest.raises(KeyError):
            api.get_servicegroup('db')

    @my_workingvcr
    def test_add_servicegroup(self):
        api.add_servicegroup('db', 'Database')
        assert api.get_servicegroup('db')['alias'] == 'Database'

    @my_workingvcr
    def test_add_duplicate_servicegroup(self):
        with pytest.raises(CheckMkWebApiException):
            api.add_servicegroup('db', 'Database')
            api.add_servicegroup('db', 'Database')

    @my_workingvcr
    def test_edit_servicegroup(self):
        api.add_servicegroup('db', 'Database')
        assert api.get_servicegroup('db')['alias'] == 'Database'
        api.edit_servicegroup('db', 'Databases')
        assert api.get_servicegroup('db')['alias'] == 'Databases'

    @my_workingvcr
    def test_edit_nonexisting_servicegroup(self):
        with pytest.raises(CheckMkWebApiException):
            api.edit_servicegroup('db', 'Database')


    @my_workingvcr
    def test_delete_servicegroup(self):
        api.add_servicegroup('db', 'Database')
        assert 'db' in api.get_all_servicegroups()
        api.delete_servicegroup('db')
        assert 'db' not in api.get_all_servicegroups()

    @my_workingvcr
    def test_delete_nonexistent_servicegroup(self):
        with pytest.raises(CheckMkWebApiException):
            api.delete_servicegroup('db')

    @my_workingvcr
    def test_get_all_services(self):
        result = api.get_all_services()
        expected_result = [
            [
                "service_state",
                "service_description",
                "service_icons",
                "svc_plugin_output",
                "svc_state_age",
                "svc_check_age",
                "perfometer",
            ]
        ]
        assert result == expected_result

    @my_workingvcr
    def test_get_pending_services(self):
        result = api.get_pending_services()
        expected_result = [
            ['service_description']
        ]
        assert result == expected_result