import logging
import random

from elevator import Elevator
from elevator.elevator_controller import ElevatorController


class Passenger:
    def __init__(self, current_floor: int, destination_floor: int) -> None:
        self.current_floor: int = current_floor
        self.destination_floor: int = destination_floor
        self.requested_elevator: int | None = None

    def call_elevator(
        self, elevator_controller: ElevatorController, elevator_id: int | None = None
    ) -> Elevator:
        # Add the current floor to the elevator's queue to be picked up
        if elevator_id:
            elevator = elevator_controller.elevators[elevator_id]
        else:
            elevator = random.choice(elevator_controller.elevators)

        if self.current_floor != elevator.current_floor:
            elevator_controller.handle_request(elevator.elevator_id, self.current_floor)

        return elevator

    def enter_elevator(self, elevator: Elevator) -> None:
        # Enter the elevator and select the destination floor
        logging.info(
            "Passenger entering on floor %s and wants to go to floor %s",
            self.current_floor,
            self.destination_floor,
        )
        elevator.add_floor(self.destination_floor)
