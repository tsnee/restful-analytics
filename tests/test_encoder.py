import pytest
from restful_analytics.encoder import StrEncoder
import numpy

@pytest.fixture()
def code_under_test():
    return StrEncoder()

def test_list(code_under_test):
    assert isinstance(code_under_test.encode([]), str)

def test_integer(code_under_test):
    assert isinstance(code_under_test.encode(numpy.int(1)), str)

def test_float(code_under_test):
    assert isinstance(code_under_test.encode(numpy.float(1.0)), str)

def test_ndarray(code_under_test):
    assert isinstance(code_under_test.encode(numpy.ndarray([1,2,3])), str)
