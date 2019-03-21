import os
import random
import string

import pytest

from check_mk_web_api.web_api_base import WebApiBase
from check_mk_web_api.web_api_servicegroup import WebApiServiceGroup
from check_mk_web_api.exception import CheckMkWebApiException

api = WebApiServiceGroup(
    os.environ['CHECK_MK_URL'],
    os.environ['CHECK_MK_USER'],
    os.environ['CHECK_MK_SECRET']
)

@pytest.mark.vcr()
class TestServiceGroup():
    def setup(self):
        api.delete_all_servicegroups()

    def test_get_servicegroup(self):
        api.add_servicegroup('db', 'Database')
        assert api.get_servicegroup('db')

    def test_get_all_servicegroups(self):
        api.add_servicegroup('db', 'Database')
        api.add_servicegroup('web', 'Webserver')
        groups = api.get_all_servicegroups()
        assert 'db' in groups
        assert 'web' in groups


    def test_get_nonexistent_servicegroup(self):
        with pytest.raises(KeyError):
            api.get_servicegroup('db')


    def test_add_servicegroup(self):
        api.add_servicegroup('db', 'Database')
        assert api.get_servicegroup('db')['alias'] == 'Database'


    def test_add_duplicate_servicegroup(self):
        with pytest.raises(CheckMkWebApiException):
            api.add_servicegroup('db', 'Database')
            api.add_servicegroup('db', 'Database')


    def test_edit_servicegroup(self):
        api.add_servicegroup('db', 'Database')
        assert api.get_servicegroup('db')['alias'] == 'Database'
        api.edit_servicegroup('db', 'Databases')
        assert api.get_servicegroup('db')['alias'] == 'Databases'


    def test_edit_nonexisting_servicegroup(self):
        with pytest.raises(CheckMkWebApiException):
            api.edit_servicegroup('db', 'Database')


    def test_delete_servicegroup(self):
        api.add_servicegroup('db', 'Database')
        assert 'db' in api.get_all_servicegroups()
        api.delete_servicegroup('db')
        assert 'db' not in api.get_all_servicegroups()


    def test_delete_nonexistent_servicegroup(self):
        with pytest.raises(CheckMkWebApiException):
            api.delete_servicegroup('db')

