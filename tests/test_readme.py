from __future__ import print_function

import doctest
import os
import sys
import pytest

import munch

_HERE = os.path.abspath(os.path.dirname(__file__))
_README_PATH = os.path.join(_HERE, '..', 'README.md')
assert os.path.exists(_README_PATH)


@pytest.mark.skipif(sys.version_info[:2] < (3, 6), reason="Requires Python version >= 3.6")
@pytest.mark.usefixtures("yaml")
def test_readme():
    globs = {
        'print_function': print_function,
    }
    result = doctest.testfile(_README_PATH, module_relative=False, globs=globs)
    assert not result.failed
