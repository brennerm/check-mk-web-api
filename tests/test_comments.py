import os
import pytest


from check_mk_web_api.web_api import WebApi

api = WebApi(
    os.environ['CHECK_MK_URL'],
    os.environ['CHECK_MK_USER'],
    os.environ['CHECK_MK_SECRET']
)

@pytest.mark.vcr
class TestComments():

    def test_view_comments(self):
        result = api.view_comments()
        expected_result = [['comment_author', 'comment_time', 'comment_expires', 'comment_entry_type', 'comment_comment', 'host', 'service_description', 'comment_id']]

        assert result == expected_result
