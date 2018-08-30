import pytest

import mock
from unfollowLogManager import UnfollowLogManager

@pytest.fixture
def nc():
    nc = UnfollowLogManager('niclasguenther')
    return nc

def test_saveInstaInfoInDb(nc):
    assert 1 == 2
