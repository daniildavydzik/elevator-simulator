# Elevator simulator

The Elevator  is a Python class that simulates an elevator system. It uses algorithm to determine the next floor to move towards based on the current status and queued floor requests.

## Features

- Supports multiple floors and a customizable maximum number of passengers.
- Implements algorithm to efficiently handle floor requests.
- Provides methods to add floor requests and move the elevator towards the next floor.
- Handles edge cases such as invalid floor numbers and elevator capacity.

## UseCases
1. Efficient Floor-to-Floor Transportation:
User enters the elevator and selects their desired floor.
The elevator system determines the optimal route to reach the selected floor, considering factors such as current elevator location, direction, and other requested floors.
The elevator stops at each floor where passengers have requested to get on or off, following a logical order to minimize travel time.
If multiple users request the same floor, the elevator optimizes the order of stops to reduce unnecessary stops and delays.

2. Dynamic Floor Priority:
A person enters the elevator on a higher floor and selects floor 8.
The elevator is currently moving in the downward direction.
The elevator system prioritizes the selected floor 8, even though it is in the opposite direction of the current travel.
As the elevator descends towards the first floor, a new person enters and presses floor 5.
The elevator system dynamically adjusts its route and stops at floor 5 before continuing down to the first floor.
This ensures that the new passenger's requested floor is accommodated, even if it means temporarily interrupting the downward movement.
This use case demonstrates how the elevator system can intelligently prioritize and adjust its route based on user input, allowing for efficient transportation and minimizing disruptions.

3. Dynamic Floor Priority (Reversed):
A person enters the elevator on a lower floor and selects floor 2.
The elevator is currently moving in the upward direction.
The elevator system prioritizes the selected floor 2, even though it is in the opposite direction of the current travel.
As the elevator ascends towards the top floor, a new person enters and presses floor 5.
The elevator system dynamically adjusts its route and stops at floor 5 before continuing up to the top floor.
This ensures that the new passenger's requested floor is accommodated, even if it means temporarily interrupting the upward movement.
In this reversed use case, the elevator system still intelligently prioritizes and adjusts its route based on user input, ensuring efficient transportation regardless of whether the person is on a higher or lower floor relative to the elevator's current direction.

## Technical notes

Each elevator runs in a separate process. We implemented it this way because our task is fully CPU-bound, and using threads would result in the Global Interpreter Lock (GIL) causing delays for passengers.

Our elevator simulator also supports buildings with multiple elevators. By default, the nearest elevator will arrive for the passenger. However, if a single button corresponds to a specific elevator, you can adjust the behavior accordingly.
## Installation

1. Clone the repository:

   ```bash
   git clone 

2. Navigate to the project directory:

   ```bash
   cd elevator

3. [Optional] Create and activate a virtual environment:

   ```bash
   python -m venv env
   source env/bin/activate

4. Run it as a console application using the following command
   
   ```bash
   --max_passengers 5 --passengers 1=4 2=5 --num_elevators 2
   ```
   Parameters explonation: 

* **max_passengers**
  Corresponds to the maximum load capacity of the elevator.

* **passengers**
  Key-value pairs, where key is current floor of a passenger and value is a destination floor. 

* **num_elevators**
  Number of elevators in the building.


## Usage

Instantiate an Elevator object with the desired maximum number of passengers and floors:
   ```python
     from elevator import Elevator


     elevator = Elevator(max_passengers=10, floors=20)
   ```
     
To add a floor request, use the add_stop(floor) method:
```python
elevator.add_stop(5)  # Request to stop at floor 5
elevator.add_stop(12)  # Request to stop at floor 12
```

To move the elevator towards the next floor, use the `move()` method:

`elevator.move()`
The `move()` method will automatically determine the next floor to move towards based on the queued floor requests and the LOOK algorithm.

Customization
You can customize the Elevator class by modifying the following parameters during instantiation:

* **max_passengers (int)**
  Maximum number of passengers that the elevator can hold.

* **floors (int)**
Total number of floors in the building.

## Running tests
 1. Navigate to the project directory:
   ```bash
   cd root_project_directory
   ```
 2. Run the following command:
   ```bash
   pytest tests/unit
   ```
