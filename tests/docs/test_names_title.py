import pytest
from doc.names_title import file_name_to_title_name


class TestNamesToTitle:

    def test_activate_mode_to_title_function(self):
     assert file_name_to_title_name('activate_mode') == 'Activate Mode: activate_mode.md'


    def test_discover_mode_to_title_function(self):
        assert file_name_to_title_name('discover_mode') == 'Discover Mode: discover_mode.md'

    def test_exception_to_title_function(self):
        assert file_name_to_title_name('exception') == 'Exception: exception.md'

    def test_web_api_contactgroups_to_title_function(self):
        assert file_name_to_title_name('web_api_contactgroups') == 'Web Api Contactgroups: web_api_contactgroups.md'
