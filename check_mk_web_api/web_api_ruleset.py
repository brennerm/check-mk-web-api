from check_mk_web_api.no_none_value_dict import NoNoneValueDict
from check_mk_web_api.web_api_base import WebApiBase


class WebApiRuleset(WebApiBase):

    def get_ruleset(self, ruleset):
        """
        Gets one rule set

        # Arguments
        ruleset (str): name of rule set to get
        """
        data = NoNoneValueDict({
            'ruleset_name': ruleset,
        })

        return self.make_request('get_ruleset', data=data, query_params={'output_format': 'python','request_format': 'python'})

    def get_rulesets(self):
        """
        Gets all rule sets
        """
        return self.make_request('get_rulesets_info', query_params={'request_format': 'python'})

    def set_ruleset(self, ruleset, ruleset_config):
        """
        Edits one rule set

        # Arguments
        ruleset (str): name of rule set to edit
        ruleset_config (dict): config that will be set, have a look at return value of #WebApi.get_ruleset
        """
        data = NoNoneValueDict({
            'ruleset_name': ruleset,
            'ruleset': ruleset_config if ruleset_config else {}
        })

        return self.make_request('set_ruleset', data=data, query_params={'request_format': 'python'})
