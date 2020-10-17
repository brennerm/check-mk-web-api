import os
import random
import string

import pytest

from check_mk_web_api import WebApi, CheckMkWebApiException

api = WebApi(
    os.environ['CHECK_MK_URL'],
    os.environ['CHECK_MK_USER'],
    os.environ['CHECK_MK_SECRET']
)


def setup():
    api.delete_all_hosts()
    api.delete_all_hostgroups()
    api.delete_all_servicegroups()

    for group in api.get_all_contactgroups():
        if group != 'all':
            api.delete_contactgroup(group)

    for user_id in api.get_all_users():
        if user_id != 'cmkadmin' and user_id != os.environ['CHECK_MK_USER']:
            api.delete_user(user_id)

    for folder in api.get_all_folders():
        if folder != '':
            api.delete_folder(folder)


def test_add_host():
    api.add_host('host00')
    assert 'host00' in api.get_all_hosts()


def test_add_duplicate_host():
    with pytest.raises(CheckMkWebApiException):
        api.add_host('host00')
        api.add_host('host00')


def test_edit_host():
    api.add_host('host00', ipaddress='192.168.0.100')
    assert api.get_host('host00')['attributes']['ipaddress'] == '192.168.0.100'

    api.edit_host('host00', ipaddress='192.168.0.101')
    assert api.get_host('host00')['attributes']['ipaddress'] == '192.168.0.101'


def test_unset_host_attribute():
    api.add_host('host00', ipaddress='192.168.0.100')
    assert api.get_host('host00')['attributes']['ipaddress'] == '192.168.0.100'
    api.edit_host('host00', unset_attributes=['ipaddress'])
    assert 'ipaddress' not in api.get_host('host00')['attributes']


def test_edit_nonexistent_host():
    with pytest.raises(CheckMkWebApiException):
        api.edit_host('host00', ipaddress='192.168.0.101')


def test_get_host():
    api.add_host('host00')
    assert api.get_host('host00')['hostname'] == 'host00'


def test_get_nonexistent_host():
    with pytest.raises(CheckMkWebApiException):
        api.get_host('host00')


def test_get_all_hosts():
    api.add_host('host00')
    api.add_host('host01')

    all_hosts = api.get_all_hosts()
    assert len(all_hosts) == 2
    assert 'host00' in all_hosts
    assert 'host01' in all_hosts


def test_get_hosts_by_folder():
    api.add_folder('test')
    api.add_host('host00', 'test')
    api.add_host('host01', 'test')

    hosts = api.get_hosts_by_folder('test')
    assert len(hosts) == 2
    assert 'host00' in hosts
    assert 'host01' in hosts


def test_delete_host():
    api.add_host('host00')
    assert len(api.get_all_hosts()) == 1

    api.delete_host('host00')
    assert len(api.get_all_hosts()) == 0


def test_delete_nonexistent_host():
    with pytest.raises(CheckMkWebApiException):
        api.delete_host('host00')


def test_delete_all_hosts():
    api.add_host('host00')
    api.add_host('host01')
    assert len(api.get_all_hosts()) == 2

    api.delete_all_hosts()
    assert len(api.get_all_hosts()) == 0

def test_delete_hosts():
    api.add_host('host00')
    api.add_host('host01')
    api.add_host('host02')
    assert len(api.get_all_hosts()) == 3

    api.delete_hosts(['host00', 'host01'])
    assert len(api.get_all_hosts()) == 1

def test_discover_services():
    api.add_host('localhost')
    result = api.discover_services('localhost')

    assert int(result['added']) >= 0
    assert int(result['removed']) >= 0
    assert int(result['kept']) >= 0
    assert int(result['new_count']) >= 0


def test_discover_services_for_nonexistent_host():
    with pytest.raises(CheckMkWebApiException):
        api.discover_services('localhost')


def test_get_user():
    api.add_user('user00', 'User 00', 'p4ssw0rd')
    assert api.get_user('user00')['alias'] == 'User 00'


def test_get_all_users():
    api.add_user('user00', 'User 00', 'p4ssw0rd')
    api.add_user('user01', 'User 01', 'p4ssw0rd')

    users = api.get_all_users()
    assert 'user00' in users
    assert 'user01' in users


def test_add_user():
    api.add_user('user00', 'User 00', 'p4ssw0rd')
    assert 'user00' in api.get_all_users()


def test_add_automation_user():
    api.add_automation_user('automation00', 'Automation 00', 's3cr3t1234')
    assert 'automation00' in api.get_all_users()


def test_add_duplicate_user():
    with pytest.raises(CheckMkWebApiException):
        api.add_user('user00', 'User 00', 'p4ssw0rd')
        api.add_user('user00', 'User 00', 'p4ssw0rd')


def test_add_duplicate_automation_user():
    with pytest.raises(CheckMkWebApiException):
        api.add_automation_user('automation00', 'Automation 00', 's3cr3t1234')
        api.add_automation_user('automation00', 'Automation 00', 's3cr3t1234')


def test_edit_user():
    api.add_user('user00', 'User 00', 'p4ssw0rd')
    assert api.get_all_users()['user00']['alias'] == 'User 00'

    api.edit_user('user00', {'alias': 'User 0'})
    assert api.get_all_users()['user00']['alias'] == 'User 0'


def test_unset_user_attribute():
    api.add_user('user00', 'User 00', 'p4ssw0rd', pager='49123456789')
    assert api.get_all_users()['user00']['pager'] == '49123456789'
    api.edit_user('user00', {}, unset_attributes=['pager'])
    assert 'pager' not in api.get_all_users()['user00']


def test_edit_nonexistent_user():
    with pytest.raises(CheckMkWebApiException):
        api.edit_user('user00', {})


def test_delete_user():
    api.add_user('user00', 'User 00', 'p4ssw0rd')
    assert 'user00' in api.get_all_users()

    api.delete_user('user00')
    assert 'user00' not in api.get_all_users()


def test_delete_nonexistent_user():
    with pytest.raises(CheckMkWebApiException):
        api.delete_user('user00')


def test_get_folder():
    api.add_folder('productive')
    assert api.get_folder('productive')


def test_get_nonexistent_folder():
    with pytest.raises(CheckMkWebApiException):
        assert api.get_folder('productive')


def test_get_all_folders():
    api.add_folder('productive')
    api.add_folder('testing')

    folders = api.get_all_folders()
    assert 'productive' in folders
    assert 'testing' in folders


def test_add_folder():
    api.add_folder('productive')
    assert 'productive' in api.get_all_folders()


def test_edit_folder():
    api.add_folder('productive', snmp_community='public')
    assert api.get_folder('productive')['attributes']['snmp_community'] == 'public'

    api.edit_folder('productive', snmp_community='private')
    assert api.get_folder('productive')['attributes']['snmp_community'] == 'private'


def test_edit_nonexistent_folder():
    with pytest.raises(CheckMkWebApiException):
        assert api.edit_folder('productive')


def test_delete_folder():
    api.add_folder('productive')
    assert 'productive' in api.get_all_folders()

    api.delete_folder('productive')
    assert 'productive' not in api.get_all_folders()


def test_delete_nonexistent_folder():
    with pytest.raises(CheckMkWebApiException):
        api.delete_folder('productive')


def test_get_contactgroup():
    api.add_contactgroup('user', 'User')
    assert api.get_contactgroup('user')


def test_get_all_contactgroups():
    api.add_contactgroup('user', 'User')
    api.add_contactgroup('admin', 'Admin')
    groups = api.get_all_contactgroups()
    assert 'user' in groups
    assert 'admin' in groups


def test_get_nonexistent_contactgroup():
    with pytest.raises(KeyError):
        api.get_contactgroup('user')


def test_add_contactgroup():
    api.add_contactgroup('user', 'User')
    assert api.get_contactgroup('user')['alias'] == 'User'


def test_add_duplicate_contactgroup():
    with pytest.raises(CheckMkWebApiException):
        api.add_contactgroup('user', 'User')
        api.add_contactgroup('user', 'User')


def test_edit_contactgroup():
    api.add_contactgroup('user', 'User')
    assert api.get_contactgroup('user')['alias'] == 'User'
    api.edit_contactgroup('user', 'Users')
    assert api.get_contactgroup('user')['alias'] == 'Users'


def test_edit_nonexisting_contactgroup():
    with pytest.raises(CheckMkWebApiException):
        api.edit_contactgroup('user', 'Users')


def test_delete_contactgroup():
    api.add_contactgroup('user', 'User')
    assert 'user' in api.get_all_contactgroups()
    api.delete_contactgroup('user')
    assert 'user' not in api.get_all_contactgroups()


def test_delete_nonexistent_contactgroup():
    with pytest.raises(CheckMkWebApiException):
        api.delete_contactgroup('user')


def test_get_hostgroup():
    api.add_hostgroup('vm', 'VM')
    api.get_hostgroup('vm')


def test_get_all_hostgroups():
    api.add_hostgroup('vm', 'VM')
    api.add_hostgroup('physical', 'Physical')
    groups = api.get_all_hostgroups()
    assert 'vm' in groups
    assert 'physical' in groups


def test_get_nonexistent_hostgroup():
    with pytest.raises(KeyError):
        api.get_hostgroup('vm')


def test_add_hostgroup():
    api.add_hostgroup('vm', 'VM')
    assert api.get_hostgroup('vm')['alias'] == 'VM'


def test_add_duplicate_hostgroup():
    with pytest.raises(CheckMkWebApiException):
        api.add_hostgroup('vm', 'VM')
        api.add_hostgroup('vm', 'VM')


def test_edit_hostgroup():
    api.add_hostgroup('vm', 'VM')
    assert api.get_hostgroup('vm')['alias'] == 'VM'
    api.edit_hostgroup('vm', 'VMs')
    assert api.get_hostgroup('vm')['alias'] == 'VMs'


def test_edit_nonexisting_hostgroup():
    with pytest.raises(CheckMkWebApiException):
        api.edit_hostgroup('vm', 'VM')


def test_delete_hostgroup():
    api.add_hostgroup('vm', 'VM')
    assert 'vm' in api.get_all_hostgroups()
    api.delete_hostgroup('vm')
    assert 'vm' not in api.get_all_hostgroups()


def test_delete_nonexistent_hostgroup():
    with pytest.raises(CheckMkWebApiException):
        api.delete_hostgroup('vm')


def test_get_servicegroup():
    api.add_servicegroup('db', 'Database')
    assert api.get_servicegroup('db')


def test_get_all_servicegroups():
    api.add_servicegroup('db', 'Database')
    api.add_servicegroup('web', 'Webserver')
    groups = api.get_all_servicegroups()
    assert 'db' in groups
    assert 'web' in groups


def test_get_nonexistent_servicegroup():
    with pytest.raises(KeyError):
        api.get_servicegroup('db')


def test_add_servicegroup():
    api.add_servicegroup('db', 'Database')
    assert api.get_servicegroup('db')['alias'] == 'Database'


def test_add_duplicate_servicegroup():
    with pytest.raises(CheckMkWebApiException):
        api.add_servicegroup('db', 'Database')
        api.add_servicegroup('db', 'Database')


def test_edit_servicegroup():
    api.add_servicegroup('db', 'Database')
    assert api.get_servicegroup('db')['alias'] == 'Database'
    api.edit_servicegroup('db', 'Databases')
    assert api.get_servicegroup('db')['alias'] == 'Databases'


def test_edit_nonexisting_servicegroup():
    with pytest.raises(CheckMkWebApiException):
        api.edit_servicegroup('db', 'Database')


def test_delete_servicegroup():
    api.add_servicegroup('db', 'Database')
    assert 'db' in api.get_all_servicegroups()
    api.delete_servicegroup('db')
    assert 'db' not in api.get_all_servicegroups()


def test_delete_nonexistent_servicegroup():
    with pytest.raises(CheckMkWebApiException):
        api.delete_servicegroup('db')


def test_get_hosttags():
    assert api.get_hosttags()


def test_set_hosttags():
    current_tags = api.get_hosttags()
    current_tags["tag_groups"].append({
        "id": ''.join(random.choice(string.ascii_lowercase) for i in range(10)),
        "title": "Test",
        "tags": [
            {
                "aux_tags": [],
                "id": ''.join(random.choice(string.ascii_lowercase) for i in range(10)),
                "title": "Test & test"
            }
        ]
    })
    api.set_hosttags(current_tags)


def test_get_ruleset():
    assert api.get_ruleset('checkgroup_parameters:hw_fans_perc')


def test_get_nonexistent_rulesets():
    with pytest.raises(CheckMkWebApiException):
        api.get_ruleset('nonexistent')


def test_set_nonexistent_rulesets():
    with pytest.raises(CheckMkWebApiException):
        api.set_ruleset('nonexistent', {})


def test_get_rulesets():
    assert api.get_rulesets()


def test_get_site():
    assert api.get_site('cmk')


def test_set_site():
    random_alias = 'alias_' + ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
    config = api.get_site('cmk')['site_config']
    config['alias'] = random_alias

    api.set_site('cmk', config)
    assert api.get_site('cmk')['site_config']['alias'] == random_alias


@pytest.mark.skip(reason="bug in Check_Mk")
def test_login_site():
    api.add_user('user00', 'User 00', 'p4ssw0rd')
    api.login_site('cmk', 'user00', 'p4ssw0rd')


@pytest.mark.skip(reason="bug in Check_Mk")
def test_logout_site():
    api.add_user('user00', 'User 00', 'p4ssw0rd')
    api.login_site('cmk', 'user00', 'p4ssw0rd')
    api.logout_site('cmk')
