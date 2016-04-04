# -*- coding: utf-8 -*-K

def with_setup(setup_function):
    def decorator(testcase):
        keyword_arguments_from_setup = {}

        testcase_with_arguments = lambda: testcase(**keyword_arguments_from_setup)
        testcase_with_arguments.__name__ = testcase.__name__
        testcase_with_arguments.setup = lambda: keyword_arguments_from_setup.update(setup_function())

        return testcase_with_arguments

    return decorator
