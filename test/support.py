import unittest
from coverage import Coverage
from setuptools import Command


class CoverageAnalysis(Command):
    """ python setup.py coverage """
    description = "Run coverage analysis with unit test"
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

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
