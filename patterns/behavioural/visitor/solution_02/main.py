from .files import Audio, Image, Text
from .algorithms import Print


def main():
    collection = [Audio(), Text(), Image()]
    algorithm = Print()
    for element in collection:
        element.accept(algorithm.visit)


if __name__ == "__main__":
    main()
