import logging
import time
from enum import Enum, auto
from multiprocessing import Queue

from exceptions import ElevatorFullException, InvalidFloorException


class ElevatorStatus(Enum):
    """Enumeration for the status of the elevator."""
    IDLE = auto()
    MOVING_UP = auto()
    MOVING_DOWN = auto()


class Direction:
    """Class representing the direction constants for the elevator."""
    UP = 1
    DOWN = -1


class Elevator:
    def __init__(
        self,
        response_queue: Queue,
        elevator_id: int,
        max_passengers: int,
        floors: int = 10,
    ) -> None:
        self.elevator_id: int = elevator_id
        self.current_floor: int = 0
        self.status: ElevatorStatus = ElevatorStatus.IDLE
        self.queue: list[int] = []
        self.max_floors: int = floors
        self.passengers: int = 0
        self.max_passengers: int = max_passengers
        self.request_queue: Queue = Queue()
        self.response_queue: Queue = response_queue

    def _is_valid_floor(self, floor: int) -> bool:
        """
        Checks if the given floor is valid.

        Args:
            floor (int): Floor number to be checked.

        Returns:
            bool: True if the floor is valid, False otherwise.
        """

        return 0 <= floor < self.max_floors

    def move(self) -> None:
        """
        Moves the elevator to the next floor based on the current status and queue.
        """

        if not self.queue:
            self.status = ElevatorStatus.IDLE
            return

        target_floor = self._get_next_floor()
        self._move_towards(target_floor)

        if self.current_floor == target_floor:
            self._stop_at(target_floor)

    def _get_next_floor(self) -> int:
        """
        Determines the next floor the elevator should move towards.

        Returns:
            int: Next floor to move towards.
        """
        if self.status == ElevatorStatus.IDLE:
            if self.current_floor in self.queue:
                return self.current_floor

            floors_above = [floor for floor in self.queue if floor > self.current_floor]
            floors_below = [floor for floor in self.queue if floor < self.current_floor]

            if floors_above:
                return min(floors_above)
            elif floors_below:
                return max(floors_below)

        direction = (
            Direction.UP if self.status == ElevatorStatus.MOVING_UP else Direction.DOWN
        )

        movement_range = range(
            self.current_floor + direction, self.max_floors, direction
        )
        if direction == Direction.DOWN:
            movement_range = range(
                self.max_floors, self.current_floor + direction - 1, direction
            )

        for floor in movement_range:
            if floor in self.queue:
                return floor

        self.status = (
            ElevatorStatus.MOVING_DOWN
            if self.status == ElevatorStatus.MOVING_UP
            else ElevatorStatus.MOVING_UP
        )

        for floor in range(self.current_floor - direction, -1, -direction):
            if floor in self.queue:
                return floor

        return self.current_floor

    def _move_towards(self, target_floor: int) -> None:
        """
        Moves the elevator towards the target floor.

        Args:
            target_floor (int): Floor number to move towards.
        """

        if self.current_floor == target_floor:
            self.status = ElevatorStatus.IDLE
            return

        direction = (
            Direction.UP if target_floor > self.current_floor else Direction.DOWN
        )

        self.current_floor += direction
        self.status = (
            ElevatorStatus.MOVING_UP
            if direction == Direction.UP
            else ElevatorStatus.MOVING_DOWN
        )

    def add_stop(self, floor: int) -> None:
        """
        Adds a stop to the elevator's queue.

        Args:
            floor (int): Floor number to add as a stop.
        """

        if not self._is_valid_floor(floor):
            raise InvalidFloorException(floor)

        if self.passengers >= self.max_passengers:
            raise ElevatorFullException()

        if floor not in self.queue:
            self.queue.append(floor)
            self._sort_queue()

    def _sort_queue(self) -> None:
        """
        Sorts the elevator's queue based on the current status.
        """

        if self.status == ElevatorStatus.IDLE and self.queue:
            self.queue.sort(key=lambda floor: (abs(floor - self.current_floor), floor))
        elif self.status == ElevatorStatus.MOVING_UP:
            self.queue.sort()
        elif self.status == ElevatorStatus.MOVING_DOWN:
            self.queue.sort(reverse=True)

    def _stop_at(self, floor: int) -> None:
        """
        Stops the elevator at the given floor.

        Args:
            floor (int): Floor number to stop at.
        """

        self.queue.remove(floor)
        logging.info("Stopping at floor %s", floor)
        self.status = ElevatorStatus.IDLE if not self.queue else self.status

    def run(self) -> None:
        """
        Runs the elevator loop, continuously moving the elevator and handling requests.
        """

        while True:
            # Check that at least one message in the queue to not black the process
            if not self.request_queue.empty():
                floor = self.request_queue.get()  # getting the message from requests queue
                if floor not in self.queue and self.current_floor != floor:
                    self.queue.append(floor)
            self.move()

            # Notify about current elevator position
            self.response_queue.put((self.elevator_id, self.current_floor))
            if self.status != ElevatorStatus.IDLE:
                logging.info(
                    "Elevator %s arrived at floor %s.",
                    self.elevator_id,
                    self.current_floor,
                )
            time.sleep(1)

    def add_floor(self, floor: int) -> None:
        """
        Adds a floor to the elevator's request queue.

        Args:
            floor (int): Floor number to add to the request queue.
        """

        self.request_queue.put(floor)
