# -*- coding: utf-8 -*-

from nose.tools import assert_equals

from . import utils_testing

def a_testing_setup_with_some_arguments():
    return {'arg1': 1, 'arg2': 'two', 'argN': 'nth argument'}

@utils_testing.with_setup
def test_arguments_from_setup(arg1, arg2, argN):
    assert_equals(1, arg1)
    assert_equals('two', arg2)
    assert_equals('nth argument', argN)
