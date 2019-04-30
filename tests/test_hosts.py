import os

import pytest

from check_mk_web_api.exception import CheckMkWebApiException
from check_mk_web_api.web_api import WebApi

from tests import my_workingvcr

import socket

timeout = 10
socket.setdefaulttimeout(timeout)

api = WebApi(
    os.environ['CHECK_MK_URL'],
    os.environ['CHECK_MK_USER'],
    os.environ['CHECK_MK_SECRET']
)


# @pytest.mark.vcr()
class TestHosts():
    def setup(self):
        api.delete_all_hosts()

        for folder in api.get_all_folders():
            if folder != '':
                api.delete_folder(folder)

    @my_workingvcr
    def test_add_host(self):
        api.add_host('host00')
        assert 'host00' in api.get_all_hosts()

    @my_workingvcr
    def test_add_duplicate_host(self):
        with pytest.raises(CheckMkWebApiException):
            api.add_host('host00')
            api.add_host('host00')

    @my_workingvcr
    def test_edit_host(self):
        api.add_host('host00', ipaddress='192.168.0.100')
        assert api.get_host('host00')['attributes']['ipaddress'] == '192.168.0.100'

        api.edit_host('host00', ipaddress='192.168.0.101')
        assert api.get_host('host00')['attributes']['ipaddress'] == '192.168.0.101'

    @my_workingvcr
    def test_unset_host_attribute(self):
        api.add_host('host00', ipaddress='192.168.0.100')
        assert api.get_host('host00')['attributes']['ipaddress'] == '192.168.0.100'
        api.edit_host('host00', unset_attributes=['ipaddress'])
        assert 'ipaddress' not in api.get_host('host00')['attributes']

    @my_workingvcr
    def test_edit_nonexistent_host(self):
        with pytest.raises(CheckMkWebApiException):
            api.edit_host('host00', ipaddress='192.168.0.101')

    @my_workingvcr
    def test_get_host(self):
        api.add_host('host00')
        assert api.get_host('host00')['hostname'] == 'host00'

    @my_workingvcr
    def test_get_nonexistent_host(self):
        with pytest.raises(CheckMkWebApiException):
            api.get_host('host00')

    @my_workingvcr
    def test_get_all_hosts(self):
        api.add_host('host00')
        api.add_host('host01')

        all_hosts = api.get_all_hosts()
        assert len(all_hosts) == 2
        assert 'host00' in all_hosts
        assert 'host01' in all_hosts

    @my_workingvcr
    def test_get_hosts_by_folder(self):
        api.add_folder('test')
        api.add_host('host00', 'test')
        api.add_host('host01', 'test')

        hosts = api.get_hosts_by_folder('test')
        assert len(hosts) == 2
        assert 'host00' in hosts
        assert 'host01' in hosts

    @my_workingvcr
    # @pytest.mark.skip('Skipping due to issues with determinstic nature')
    def test_delete_host(self):
        api.add_host('host00')
        assert len(api.get_all_hosts()) == 1

        api.delete_host('host00')
        assert len(api.get_all_hosts()) == 0

    #
    @my_workingvcr
    def test_delete_nonexistent_host(self):
        with pytest.raises(CheckMkWebApiException):
            api.delete_host('host00')

    #
    @my_workingvcr
    def test_delete_all_hosts(self):
        api.add_host('host00')
        api.add_host('host01')
        assert len(api.get_all_hosts()) == 2

        api.delete_all_hosts()
        assert len(api.get_all_hosts()) == 0

    @my_workingvcr
    def test_view_host_events(self):
        result = api.view_host_events()
        expected_result = [['log_icon',
                            'log_time',
                            'log_type',
                            'host',
                            'service_description',
                            'log_state_type',
                            'log_plugin_output'],
                           ['',
                            '76 m',
                            'SERVICE NOTIFICATION',
                            'localhost',
                            'Check_MK Discovery',
                            'ACKNOWLEDGEMENT (CRITICAL)',
                            'CRIT - no unmonitored services found, no vanished services found, [agent] '
                            'Communication failed: [Errno 111] Connection refusedCRIT'],
                           ['',
                            '104 m',
                            'SERVICE NOTIFICATION',
                            'localhost',
                            'PING',
                            'DOWNTIMESTART (OK)',
                            'OK - 127.0.0.1: rta 0.010ms, lost 0%'],
                           ['',
                            '104 m',
                            'SERVICE DOWNTIME ALERT',
                            'localhost',
                            'PING',
                            'STARTED',
                            ' Service has entered a period of scheduled downtime'],
                           ['',
                            '104 m',
                            'SERVICE NOTIFICATION',
                            'localhost',
                            'Check_MK Discovery',
                            'DOWNTIMESTART (CRITICAL)',
                            'CRIT - no unmonitored services found, no vanished services found, [agent] '
                            'Communication failed: [Errno 111] Connection refusedCRIT'],
                           ['',
                            '104 m',
                            'SERVICE DOWNTIME ALERT',
                            'localhost',
                            'Check_MK Discovery',
                            'STARTED',
                            ' Service has entered a period of scheduled downtime'],
                           ['',
                            '23 h',
                            'HOST NOTIFICATION',
                            'localhost',
                            '',
                            'DOWNTIMEEND (UP)',
                            'OK - 127.0.0.1: rta 0.005ms, lost 0%'],
                           ['',
                            '23 h',
                            'HOST DOWNTIME ALERT',
                            'localhost',
                            '',
                            'STOPPED',
                            ' Host has exited from a period of scheduled downtime'],
                           ['',
                            '25 h',
                            'HOST NOTIFICATION',
                            'localhost',
                            '',
                            'DOWNTIMESTART (UP)',
                            'OK - 127.0.0.1: rta 0.010ms, lost 0%'],
                           ['',
                            '25 h',
                            'HOST DOWNTIME ALERT',
                            'localhost',
                            '',
                            'STARTED',
                            ' Host has entered a period of scheduled downtime'],
                           ['',
                            '46 h',
                            'SERVICE NOTIFICATION',
                            'localhost',
                            'Check_MK Discovery',
                            'DOWNTIMEEND (CRITICAL)',
                            'CRIT - no unmonitored services found, no vanished services found, [agent] '
                            'Communication failed: [Errno 111] Connection refusedCRIT'],
                           ['',
                            '46 h',
                            'SERVICE DOWNTIME ALERT',
                            'localhost',
                            'Check_MK Discovery',
                            'STOPPED',
                            ' Service has exited from a period of scheduled downtime'],
                           ['',
                            '2019-03-25 17:11:25',
                            'SERVICE NOTIFICATION',
                            'localhost',
                            'Check_MK Discovery',
                            'DOWNTIMESTART (CRITICAL)',
                            'CRIT - no unmonitored services found, no vanished services found, [agent] '
                            'Communication failed: [Errno 111] Connection refusedCRIT'],
                           ['',
                            '2019-03-25 17:11:25',
                            'SERVICE DOWNTIME ALERT',
                            'localhost',
                            'Check_MK Discovery',
                            'STARTED',
                            ' Service has entered a period of scheduled downtime'],
                           ['',
                            '2019-03-25 16:44:17',
                            'SERVICE NOTIFICATION',
                            'localhost',
                            'Check_MK Discovery',
                            'CRITICAL',
                            'CRIT - no unmonitored services found, no vanished services found, [agent] '
                            'Communication failed: [Errno 111] Connection refusedCRIT'],
                           ['',
                            '2019-03-25 16:44:17',
                            'SERVICE ALERT',
                            'localhost',
                            'Check_MK Discovery',
                            'HARD',
                            'CRIT - no unmonitored services found, no vanished services found, [agent] '
                            'Communication failed: [Errno 111] Connection refusedCRIT']]
        assert result == expected_result

    @my_workingvcr
    def test_view_host_events(self):
        result = api.view_host_notifications()
        expected_result = [['log_icon', 'log_time', 'log_contact_name', 'log_command', 'log_type', 'host', 'service_description', 'log_state', 'log_plugin_output'], ['', '18 m', 'check-mk-notify', 'check-mk-notify', 'SERVICE NOTIFICATION', 'localhost', 'PING', 'OK', 'OK - 127.0.0.1: rta 0.007ms, lost 0%'], ['', '18 m', 'check-mk-notify', 'check-mk-notify', 'SERVICE NOTIFICATION', 'localhost', 'Check_MK Discovery', 'CRIT', 'CRIT - no unmonitored services found, no vanished services found, [agent] Communication failed: [Errno 111] Connection refusedCRIT'], ['', '110 m', 'check-mk-notify', 'check-mk-notify', 'SERVICE NOTIFICATION', 'localhost', 'Check_MK Discovery', 'CRIT', 'CRIT - no unmonitored services found, no vanished services found, [agent] Communication failed: [Errno 111] Connection refusedCRIT'], ['', '138 m', 'check-mk-notify', 'check-mk-notify', 'SERVICE NOTIFICATION', 'localhost', 'PING', 'OK', 'OK - 127.0.0.1: rta 0.010ms, lost 0%'], ['', '138 m', 'check-mk-notify', 'check-mk-notify', 'SERVICE NOTIFICATION', 'localhost', 'Check_MK Discovery', 'CRIT', 'CRIT - no unmonitored services found, no vanished services found, [agent] Communication failed: [Errno 111] Connection refusedCRIT'], ['', '23 h', 'check-mk-notify', 'check-mk-notify', 'HOST NOTIFICATION', 'localhost', '', 'UP', 'OK - 127.0.0.1: rta 0.005ms, lost 0%'], ['', '26 h', 'check-mk-notify', 'check-mk-notify', 'HOST NOTIFICATION', 'localhost', '', 'UP', 'OK - 127.0.0.1: rta 0.010ms, lost 0%'], ['', '47 h', 'check-mk-notify', 'check-mk-notify', 'SERVICE NOTIFICATION', 'localhost', 'Check_MK Discovery', 'CRIT', 'CRIT - no unmonitored services found, no vanished services found, [agent] Communication failed: [Errno 111] Connection refusedCRIT'], ['', '2019-03-25 17:11:25', 'check-mk-notify', 'check-mk-notify', 'SERVICE NOTIFICATION', 'localhost', 'Check_MK Discovery', 'CRIT', 'CRIT - no unmonitored services found, no vanished services found, [agent] Communication failed: [Errno 111] Connection refusedCRIT'], ['', '2019-03-25 16:44:17', 'check-mk-notify', 'check-mk-notify', 'SERVICE NOTIFICATION', 'localhost', 'Check_MK Discovery', 'CRIT', 'CRIT - no unmonitored services found, no vanished services found, [agent] Communication failed: [Errno 111] Connection refusedCRIT']]
        assert result == expected_result