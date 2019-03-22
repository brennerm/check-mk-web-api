import os
import pytest

from check_mk_web_api.web_api import WebApi


class TestWebApi():
    def setup(self):
        self.all_methods_in_web_api = dir(WebApi)

    def test_for_membership(self):
        # assert 'get_all_folders' exitss in the api.methods list
        # I am almost 100% sure that the call to get python class mehtods list is NOT api.methods

        assert 'activate_changes' in self.all_methods_in_web_api
        assert 'add_automation_user' in self.all_methods_in_web_api
        assert 'add_contactgroup' in self.all_methods_in_web_api
        assert 'add_folder' in self.all_methods_in_web_api
        assert 'add_host' in self.all_methods_in_web_api
        assert 'add_hostgroup' in self.all_methods_in_web_api
        assert 'add_servicegroup' in self.all_methods_in_web_api
        assert 'add_user' in self.all_methods_in_web_api
        assert 'bake_agents' in self.all_methods_in_web_api
        assert 'bake_agents' in self.all_methods_in_web_api
        assert 'checking' in self.all_methods_in_web_api
        assert 'delete_all_contactgroups' in self.all_methods_in_web_api
        assert 'delete_all_hostgroups' in self.all_methods_in_web_api
        assert 'delete_all_hosts' in self.all_methods_in_web_api
        assert 'delete_all_servicegroups' in self.all_methods_in_web_api
        assert 'delete_contactgroup' in self.all_methods_in_web_api
        assert 'delete_folder' in self.all_methods_in_web_api
        assert 'delete_host' in self.all_methods_in_web_api
        assert 'delete_hostgroup' in self.all_methods_in_web_api
        assert 'delete_servicegroup' in self.all_methods_in_web_api
        assert 'delete_site' in self.all_methods_in_web_api
        assert 'delete_user' in self.all_methods_in_web_api
        assert 'discover_services' in self.all_methods_in_web_api
        assert 'discover_services_for_all_hosts' in self.all_methods_in_web_api
        assert 'edit_contactgroup' in self.all_methods_in_web_api
        assert 'edit_folder' in self.all_methods_in_web_api
        assert 'edit_host' in self.all_methods_in_web_api
        assert 'edit_hostgroup' in self.all_methods_in_web_api
        assert 'edit_servicegroup' in self.all_methods_in_web_api
        assert 'edit_user' in self.all_methods_in_web_api
        assert 'get_alerts' in self.all_methods_in_web_api
        assert 'get_alerts' in self.all_methods_in_web_api
        assert 'get_all_contactgroups' in self.all_methods_in_web_api
        assert 'get_all_contactgroups' in self.all_methods_in_web_api
        assert 'get_all_downtimes' in self.all_methods_in_web_api
        assert 'get_all_folders' in self.all_methods_in_web_api
        assert 'get_all_folders' in self.all_methods_in_web_api
        assert 'get_all_hostgroups' in self.all_methods_in_web_api
        assert 'get_all_hostgroups' in self.all_methods_in_web_api
        assert 'get_all_hosts' in self.all_methods_in_web_api
        assert 'get_all_servicegroups' in self.all_methods_in_web_api
        assert 'get_all_servicegroups' in self.all_methods_in_web_api
        assert 'get_all_users' in self.all_methods_in_web_api
        assert 'get_all_users' in self.all_methods_in_web_api
        assert 'get_contactgroup' in self.all_methods_in_web_api
        assert 'get_folder' in self.all_methods_in_web_api
        assert 'get_host' in self.all_methods_in_web_api
        assert 'get_host' in self.all_methods_in_web_api
        assert 'get_hostgroup' in self.all_methods_in_web_api
        assert 'get_hosts_by_folder' in self.all_methods_in_web_api
        assert 'get_hosttags' in self.all_methods_in_web_api
        assert 'get_hosttags' in self.all_methods_in_web_api
        assert 'get_ruleset' in self.all_methods_in_web_api
        assert 'get_rulesets' in self.all_methods_in_web_api
        assert 'get_rulesets' in self.all_methods_in_web_api
        assert 'get_servicegroup' in self.all_methods_in_web_api
        assert 'get_site' in self.all_methods_in_web_api
        assert 'get_site' in self.all_methods_in_web_api
        assert 'get_svc_problems' in self.all_methods_in_web_api
        assert 'get_svc_problems' in self.all_methods_in_web_api
        assert 'get_user' in self.all_methods_in_web_api
        assert 'login_site' in self.all_methods_in_web_api
        assert 'logout_site' in self.all_methods_in_web_api
        assert 'make_request' in self.all_methods_in_web_api
        assert 'make_view_name_request' in self.all_methods_in_web_api
        assert 'set_downtime' in self.all_methods_in_web_api
        assert 'set_downtime' in self.all_methods_in_web_api
        assert 'set_hosttags' in self.all_methods_in_web_api
        assert 'set_ruleset' in self.all_methods_in_web_api
        assert 'set_site' in self.all_methods_in_web_api
