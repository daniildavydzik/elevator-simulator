from multiprocessing import Queue

from .elevator import Elevator


class ElevatorController:
    def __init__(self, num_elevators: int) -> None:
        self.num_elevators = num_elevators
        self.elevators: dict[int, Elevator] = {}
        self.request_queue: Queue = Queue()
        self.response_queue: Queue = Queue()

    def add_elevator(self, elevator: Elevator) -> None:
        """
        Adds an elevator to the controller.

        Args:
            elevator (Elevator): The elevator object to add.
        """
        self.elevators[elevator.elevator_id] = elevator

    def handle_request(self, elevator_id: int, floor: int) -> None:
        """
        Handles a request to move an elevator to a specific floor.

        Args:
            elevator_id (int): The ID of the elevator to handle the request.
            floor (int): The floor to move the elevator to.
        """
        self.request_queue.put((elevator_id, floor))

    def start(self):
        """
        Starts the elevator controller and listens for requests.
        """
        while True:
            elevator_id, floor = self.request_queue.get()
            elevator = self.elevators[elevator_id]
            elevator.add_floor(floor)
