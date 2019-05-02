import os
from tests import filter_uri
import pytest


from check_mk_web_api.exception import CheckMkWebApiException
from check_mk_web_api.web_api import WebApi

api = WebApi(
    os.environ['CHECK_MK_URL'],
    os.environ['CHECK_MK_USER'],
    os.environ['CHECK_MK_SECRET']
)


#@pytest.mark.vcr()
class TestHosts():
    def setup(self):
        api.delete_all_hosts()

        for folder in api.get_all_folders():
            if folder != '':
                api.delete_folder(folder)

    @filter_uri
    def test_add_host(self):
        api.add_host('host00')
        assert 'host00' in api.get_all_hosts()

    @filter_uri
    def test_add_duplicate_host(self):
        with pytest.raises(CheckMkWebApiException):
            api.add_host('host00')
            api.add_host('host00')

    @filter_uri
    def test_edit_host(self):
        api.add_host('host00', ipaddress='192.168.0.100')
        assert api.get_host('host00')['attributes']['ipaddress'] == '192.168.0.100'

        api.edit_host('host00', ipaddress='192.168.0.101')
        assert api.get_host('host00')['attributes']['ipaddress'] == '192.168.0.101'

    @filter_uri
    def test_unset_host_attribute(self):
        api.add_host('host00', ipaddress='192.168.0.100')
        assert api.get_host('host00')['attributes']['ipaddress'] == '192.168.0.100'
        api.edit_host('host00', unset_attributes=['ipaddress'])
        assert 'ipaddress' not in api.get_host('host00')['attributes']

    @filter_uri
    def test_edit_nonexistent_host(self):
        with pytest.raises(CheckMkWebApiException):
            api.edit_host('host00', ipaddress='192.168.0.101')

    @filter_uri
    def test_get_host(self):
        api.add_host('host00')
        assert api.get_host('host00')['hostname'] == 'host00'

    @filter_uri
    def test_get_nonexistent_host(self):
        with pytest.raises(CheckMkWebApiException):
            api.get_host('host00')

    @filter_uri
    def test_get_all_hosts(self):
        api.add_host('host00')
        api.add_host('host01')

        all_hosts = api.get_all_hosts()
        assert len(all_hosts) == 2
        assert 'host00' in all_hosts
        assert 'host01' in all_hosts

    @filter_uri
    def test_get_hosts_by_folder(self):
        api.add_folder('test')
        api.add_host('host00', 'test')
        api.add_host('host01', 'test')

        hosts = api.get_hosts_by_folder('test')
        assert len(hosts) == 2
        assert 'host00' in hosts
        assert 'host01' in hosts

    @pytest.mark.skip('Skipping due to issues with determinstic nature')
    def test_delete_host(self):
        api.add_host('host00')
        assert len(api.get_all_hosts()) == 1

        api.delete_host('host00')
        assert len(api.get_all_hosts()) == 0

    #
    @filter_uri
    def test_delete_nonexistent_host(self):
        with pytest.raises(CheckMkWebApiException):
            api.delete_host('host00')

    #
    @filter_uri
    def test_delete_all_hosts(self):
        api.add_host('host00')
        api.add_host('host01')
        assert len(api.get_all_hosts()) == 2

        api.delete_all_hosts()
        assert len(api.get_all_hosts()) == 0

    @filter_uri
    def test_view_host_events(self):
        result = api.view_host_events()
        expected_result = [['log_icon', 'log_time', 'log_type', 'host', 'service_description', 'log_state_type', 'log_plugin_output']]

        assert result == expected_result

