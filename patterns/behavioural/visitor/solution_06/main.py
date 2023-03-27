from .files import Audio, Image, Text, SealedFileType
from .algorithms import Print


def main():
    collection = [Audio(), Text(), Image()]
    algorithm = Print[SealedFileType]()
    for element in collection:
        algorithm.visit(element)


if __name__ == "__main__":
    main()
