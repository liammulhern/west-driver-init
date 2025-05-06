import pytest
from argparse import Namespace

@pytest.fixture
def dummy_args():
    """
    Provides a default Namespace without flags set.
    """
    return Namespace(name=None, compatible=None, bus=None, path=None, yes=False)
