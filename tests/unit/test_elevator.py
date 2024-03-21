import pytest

from elevator.elevator import ElevatorStatus
from exceptions import ElevatorFullException, InvalidFloorException


class TestElevator:
    @pytest.mark.parametrize("floor", [5, 3, 7])
    def test_add_stop_valid_floor(self, elevator, floor):
        elevator.add_stop(floor)
        assert floor in elevator.queue

    @pytest.mark.parametrize("invalid_floor", [-1, 30, 100])
    def test_add_stop_invalid_floor(self, elevator, invalid_floor):
        with pytest.raises(InvalidFloorException):
            elevator.add_stop(invalid_floor)

    def test_add_stop_elevator_full(self, elevator):
        elevator.passengers = 10
        with pytest.raises(ElevatorFullException):
            elevator.add_stop(7)

    @pytest.mark.parametrize(
        "queue, expected_queue",
        [
            ([6, 4, 1, 9], [1, 4, 6, 9]),
            ([9, 4, 6, 1], [1, 4, 6, 9]),
            ([3, 2, 4, 5], [2, 3, 4, 5]),
        ],
    )
    def test_sort_queue_idle(self, elevator, queue, expected_queue):
        elevator.current_floor = 2
        elevator.status = ElevatorStatus.IDLE
        elevator.queue = queue
        elevator._sort_queue()
        assert elevator.queue == expected_queue

    def test_sort_queue_moving_up(self, elevator):
        elevator.status = ElevatorStatus.MOVING_UP
        elevator.queue = [6, 4, 1, 9]
        elevator._sort_queue()
        assert elevator.queue == [1, 4, 6, 9]

    def test_sort_queue_moving_down(self, elevator):
        elevator.status = ElevatorStatus.MOVING_DOWN
        elevator.queue = [6, 4, 1, 9]
        elevator._sort_queue()
        assert elevator.queue == [9, 6, 4, 1]

    @pytest.mark.parametrize(
        "current_floor, target_floor, expected_floor, expected_status",
        [
            (5, 7, 6, ElevatorStatus.MOVING_UP),
            (9, 2, 8, ElevatorStatus.MOVING_DOWN),
            (3, 3, 3, ElevatorStatus.IDLE),
        ],
    )
    def test_move_towards(
        self, elevator, current_floor, target_floor, expected_floor, expected_status
    ):
        elevator.current_floor = current_floor
        elevator._move_towards(target_floor)
        assert elevator.current_floor == expected_floor
        assert elevator.status == expected_status

    def test_move_idle_elevator(self, elevator):
        elevator.move()
        assert elevator.status == ElevatorStatus.IDLE

    def test_move_with_queue(self, elevator):
        elevator.add_stop(3)
        elevator.add_stop(8)
        for _ in range(3):
            elevator.move()
        assert elevator.current_floor == 3
        assert elevator.status == ElevatorStatus.MOVING_UP
        for _ in range(5):
            elevator.move()
        assert elevator.current_floor == 8
        assert elevator.status == ElevatorStatus.IDLE
        assert len(elevator.queue) == 0

    def test_move_with_queue_and_direction(self, elevator):
        elevator.add_stop(3)
        for _ in range(2):
            elevator.move()

        elevator.add_stop(1)
        elevator.move()

        assert elevator.current_floor == 3

        for _ in range(2):
            elevator.move()

        assert elevator.current_floor == 1
        assert elevator.status == ElevatorStatus.IDLE
        assert len(elevator.queue) == 0
