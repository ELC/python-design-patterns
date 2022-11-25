from dataclasses import dataclass


@dataclass
class TrainCar:
    """See https://www.wikiwand.com/en/Railroad_car"""

    length_in_meters: float
    tare_in_kilograms: float


@dataclass
class TankWagon(TrainCar):
    """See https://www.wikiwand.com/en/Tank_car"""

    capacity_in_liters: float


@dataclass
class PassengerCoach(TrainCar):
    """See https://www.wikiwand.com/en/Passenger_car_(rail)"""

    number_of_seats: int


@dataclass
class Locomotive(TrainCar):
    """See https://www.wikiwand.com/en/Passenger_car_(rail)"""

    horse_power: float
    maximum_speed_in_kmh: float


@dataclass
class Train:
    cars: list[TrainCar]

    def __post_init__(self):
        first_car, *_, last_car = self.cars

        if Locomotive not in [type(first_car), type(last_car)]:
            raise ValueError("A train must start or end with a Locomotive")
