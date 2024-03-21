import argparse
import logging
import multiprocessing
from collections import defaultdict

from elevator import Elevator
from elevator.elevator_controller import ElevatorController
from exceptions import (
    ElevatorFullException,
    InvalidFloorException,
    NoElevatorAvailableException,
)
from passenger import Passenger

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


class DictAction(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        setattr(namespace, self.dest, defaultdict(list))

        for value in values:
            key, value = map(int, value.split("="))
            getattr(namespace, self.dest)[key].append(value)


def main(input_args):
    elevator_controller = ElevatorController(input_args.num_elevators)

    for elevator_id in range(input_args.num_elevators):
        # Initialize the elevator with a maximum capacity
        elevator = Elevator(
            response_queue=elevator_controller.response_queue,
            max_passengers=input_args.max_passengers,
            elevator_id=elevator_id,
        )
        elevator_controller.add_elevator(elevator)

    try:
        # Create a passengers with current and destination floors from arguments
        passengers = []
        for current_floor, destination_floors in input_args.passengers.items():
            for destination_floor in destination_floors:
                passenger = Passenger(
                    current_floor=current_floor, destination_floor=destination_floor
                )
                passengers.append(passenger)

        for passenger in passengers:
            # Simulate the passenger calling the elevator
            elevator = passenger.call_elevator(elevator_controller)
            passenger.requested_elevator = elevator.elevator_id
            logging.info(
                "Passenger on floor %s called the elevator %s.",
                passenger.current_floor,
                elevator.elevator_id,
            )

        # Creates and starts Elevator controller process
        elevator_controller_process = multiprocessing.Process(
            target=elevator_controller.start
        )
        elevator_controller_process.start()

        # Starts Elevator processes
        elevator_processes = []
        for elevator in elevator_controller.elevators.values():
            elevator_process = multiprocessing.Process(target=elevator.run)
            elevator_processes.append(elevator_process)
            elevator_process.start()

        while passengers:
            elevator_id, floor = elevator_controller.response_queue.get()
            for passenger in passengers.copy():
                if (
                    passenger.requested_elevator == elevator_id
                    and floor == passenger.current_floor
                ):
                    passengers.remove(passenger)

                    # Simulate the passenger entering the elevator
                    passenger.enter_elevator(elevator_controller.elevators[elevator_id])
                    logging.info(
                        "Passenger entered the elevator to go to floor %s.",
                        passenger.destination_floor,
                    )

        # Joins Elevator controller and Elevator processes
        elevator_controller_process.join()
        for elevator_process in elevator_processes:
            elevator_process.join()

    except InvalidFloorException as e:
        logging.error(e)
    except NoElevatorAvailableException as e:
        logging.error(e)
    except ElevatorFullException as e:
        logging.error(e)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Simulate an elevator system.")

    parser.add_argument(
        "--max_passengers",
        type=int,
        default=5,
        help="Maximum number of passengers the elevator can carry.",
    )
    parser.add_argument(
        "--passengers",
        action=DictAction,
        nargs="*",
        required=True,
        help="Current floors of the passengers and floors they want to go.",
    )
    parser.add_argument(
        "--num_elevators", type=int, default=2, help="Number of elevators."
    )

    args = parser.parse_args()

    main(args)
