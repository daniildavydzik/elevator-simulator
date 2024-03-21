from unittest.mock import Mock

import pytest

from elevator import Elevator


@pytest.fixture
def elevator():
    return Elevator(max_passengers=10, floors=20, elevator_id=1, response_queue=Mock())
