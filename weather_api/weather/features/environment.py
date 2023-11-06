from behave import fixture, use_fixture
from rest_framework.test import APIClient
from test_plus.test import TestCase


@fixture
def behave_test_case(context):
    context.test_case = TestCase
    context.test_case.setUpClass()
    context.test_case_instance = context.test_case()


@fixture
def behave_api_client(context):
    context.api_client = APIClient()


def before_all(context):
    use_fixture(behave_test_case, context)
    use_fixture(behave_api_client, context)


def before_scenario(context, scenario):
    context.last_request_json = None
