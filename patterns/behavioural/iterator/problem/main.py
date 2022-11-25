from .consumer import ConsolePrinter
from .iterables import (
    Train,
    TankWagon,
    PassengerCoach,
    Locomotive,
    Classroom,
    Student,
    Memory,
)


def main():
    train = Train(
        [
            TankWagon(
                length_in_meters=6.10,
                tare_in_kilograms=1250,
                capacity_in_liters=23000,
            ),
            PassengerCoach(
                length_in_meters=6.10,
                tare_in_kilograms=5750,
                number_of_seats=40,
            ),
            Locomotive(
                length_in_meters=23.16,
                tare_in_kilograms=192000,
                horse_power=6000,
                maximum_speed_in_kmh=121,
            ),
        ]
    )

    classroom = Classroom(
        {
            Student("Matthew", 12),
            Student("Sofia", 13),
            Student("Alex", 11),
        }
    )

    memory = Memory(4)

    printer = ConsolePrinter()

    printer.print(train)
    printer.print(classroom, alphabetical=True)
    printer.print(memory)


if __name__ == "__main__":
    main()
