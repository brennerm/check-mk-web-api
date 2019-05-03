import pytest
import re


# caputures the server url and replaces IP or name with localhost-testing to help with cassette errors
def scrub_string(string, replacement=""):
    def before_record_response(response):
        regexp_http = "^https?://[^/]+/+[^/]+/+[^/]+/"
        regexp_username = "_username=[a-zA-Z]+"
        regexp_secret = "_secret=.*$"

        replaced_uri = re.sub(regexp_http, "http://localhost/checkmd2/check_mk/", response.uri)
        replaced_uri = re.sub(regexp_username, "_username=automation", replaced_uri)
        replaced_uri = re.sub(regexp_secret, "_secret=not_a_secret", replaced_uri)
        response.uri = replaced_uri

        return response

    return before_record_response


@pytest.fixture(scope='module')
def vcr_config():
    return {
        # Replace the Authorization request header with "DUMMY" in cassettes
        'before_record': scrub_string("_secret", "_username"),
    }