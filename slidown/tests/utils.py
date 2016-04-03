# -*- coding: utf-8 -*-K

def with_setup(setup_function):
    def decorator(testcase):
        kwargs = {}

        test_wrapper = lambda: testcase(**kwargs)
        test_wrapper.__name__ = testcase.__name__

        def setup_wrapper():
            setup_kwargs = setup_function()
            kwargs.update(setup_kwargs)

        test_wrapper.setup = setup_wrapper

        return test_wrapper

    return decorator
