import six
import sys
try:
    from coverage import Coverage
except ImportError:
    pass
from pkg_resources import _namespace_packages
from setuptools.command.test import test as TestCommand
from setuptools.py31compat import unittest_main


class CoverageAnalysisTestCommand(TestCommand):
    """ add coverage analysis to test command """
    description = "Run coverage analysis with unit test"

    def run_tests(self):
        " Run coverage on unit test "
        coverage = Coverage()
        coverage.start()

        # Purge modules under test from sys.modules. The test loader will
        # re-import them from the build location. Required when 2to3 is used
        # with namespace packages.
        if six.PY3 and getattr(self.distribution, 'use_2to3', False):
            module = self.test_suite.split('.')[0]
            if module in _namespace_packages:
                del_modules = []
                if module in sys.modules:
                    del_modules.append(module)
                module += '.'
                for name in sys.modules:
                    if name.startswith(module):
                        del_modules.append(name)
                list(map(sys.modules.__delitem__, del_modules))

        unittest_main(
            None, None, self._argv,
            testLoader=self._resolve_as_ep(self.test_loader),
            testRunner=self._resolve_as_ep(self.test_runner),
            exit=False,
        )

        coverage.stop()
        coverage.save()
        coverage.report(show_missing=False)
