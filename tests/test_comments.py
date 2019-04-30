import os
import pytest

from check_mk_web_api.web_api import WebApi
from tests import my_workingvcr

api = WebApi(
    os.environ['CHECK_MK_URL'],
    os.environ['CHECK_MK_USER'],
    os.environ['CHECK_MK_SECRET']
)


# @pytest.mark.vcr()
class TestComments():

    @my_workingvcr
    def test_view_comments(self):
        result = api.view_comments()
        expected_result = [
            ['comment_author',
                'comment_time',
                'comment_expires',
                'comment_entry_type',
                'comment_comment',
                'host',
                'service_description',
                'comment_id'],
             ['(Nagios Process)',
                   '16 m',
                   '-',
                   '',
                   'This service has been scheduled for fixed downtime from 2019-03-27 16:15:48 '
                 'to 2019-03-27 18:15:48.  Notifications for the service will not be sent out '
                 'during that time period.',
                   'localhost',
                   'Check_MK Discovery',
                   '8'],
              ['(Nagios Process)',
                   '16 m',
                   '-',
                   '',
                   'This service has been scheduled for fixed downtime from 2019-03-27 16:15:48 '
                 'to 2019-03-27 18:15:48.  Notifications for the service will not be sent out '
                 'during that time period.',
                   'localhost',
                   'PING',
                   '9']]

        assert result == expected_result
