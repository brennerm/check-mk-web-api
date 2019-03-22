from check_mk_web_api.web_api_hosts import WebApiHosts
from check_mk_web_api.web_api_folders import WebApiFolders
from check_mk_web_api.web_api_hosttags import WebApiHosttags
from check_mk_web_api.web_api_users import WebApiUsers
from check_mk_web_api.web_api_site import WebApiSite
from check_mk_web_api.web_api_servicegroup import WebApiServiceGroup
from check_mk_web_api.web_api_ruleset import WebApiRuleset
from check_mk_web_api.web_api_agents import WebApiAgents
from check_mk_web_api.web_api_alerts import WebApiAlerts
from check_mk_web_api.web_api_contactgroups import WebApiContactGroups
from check_mk_web_api.web_api_downtimes import WebApiDowntimes
from check_mk_web_api.web_api_hostgroup import WebApiHostGroup
from check_mk_web_api.web_api_problems import WebApiProblems

# in web_api.py
class WebApi(WebApiHosts, WebApiFolders, WebApiHosttags, WebApiUsers, WebApiSite, WebApiServiceGroup, WebApiRuleset, WebApiAgents, WebApiAlerts, WebApiContactGroups, WebApiDowntimes, WebApiHostGroup, WebApiProblems):
    def checking(self):
        print('Yeppers')