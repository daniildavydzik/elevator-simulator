class InvalidFloorException(Exception):
    """Raised when a requested floor is outside the range of valid floors."""

    def __init__(self, floor, message="Floor requested is invalid."):
        self.floor = floor
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f"{self.message} Floor: {self.floor}"


class ElevatorFullException(Exception):
    """Raised when the elevator is at full capacity and cannot take more passengers."""

    def __init__(self, message="Elevator is full."):
        self.message = message
        super().__init__(self.message)


class NoElevatorAvailableException(Exception):
    """Raised when there is no elevator available to take a passenger."""

    def __init__(self, message="No elevator available."):
        self.message = message
        super().__init__(self.message)
