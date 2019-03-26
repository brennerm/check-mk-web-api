import os

import pytest

from check_mk_web_api.web_api_alerts import WebApiAlerts

api = WebApiAlerts(
    os.environ['CHECK_MK_URL'],
    os.environ['CHECK_MK_USER'],
    os.environ['CHECK_MK_SECRET']
)

@pytest.mark.vcr()
class TestAlerts():

    def test_get_alerts_does_not_error(self):
        assert api.get_alerts()

    def test_get_alerts_contains_information(self):
        alert_results = api.get_alerts()
        assert len(alert_results) == 2
        assert alert_results[1] == ['localhost', 'Check_MK Discovery', '1', '0', '0', '1']

    @pytest.mark.skip('incomplete code')
    def test_ack_alert(self):
        hostname = "hostname"
        comment = "acknowledge"
        servicename = "serviceName"

        result = api.ack_alerts(hostname, comment, servicename)
        assert api.ack_alerts(hostname, comment, servicename)