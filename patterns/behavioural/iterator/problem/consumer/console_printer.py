from ..iterables import Train, Classroom, Memory


class ConsolePrinter:
    def print(self, collection: Train | Classroom | Memory, alphabetical: bool = False):

        if isinstance(collection, Classroom):
            if alphabetical:
                collection_items = sorted(collection.students, key=lambda x: x.name)
            else:
                collection_items = list(collection.students)

        elif isinstance(collection, Train):
            collection_items = collection.cars

        else:
            collection_items = list(collection.addresses)

        for item in collection_items:
            print(item)
