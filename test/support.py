import unittest
try:
    from coverage import Coverage
except ImportError:
    pass
from setuptools.command.test import test as TestCommand


class CoverageAnalysisCommand(TestCommand):
    """ add coverage analysis to test command """
    description = "Run coverage analysis with unit test"

    def run(self):
        " Run coverage on unit test "
        coverage = Coverage()
        coverage.start()

        unittest.main(
            module='tests',
            argv=['coverage'],
            verbosity=2,
            exit=False
        )

        coverage.stop()
        coverage.save()
        coverage.report(show_missing=False)
