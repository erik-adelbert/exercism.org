"""
kindergarten_garden.py -- 
"""

CHILDRENS = (
    "Alice",
    "Bob",
    "Charlie",
    "David",
    "Eve",
    "Fred",
    "Ginny",
    "Harriet",
    "Ileana",
    "Joseph",
    "Kincaid",
    "Larry",
)


class Garden:
    """Garden"""

    names = {"G": "Grass", "C": "Clover", "R": "Radishes", "V": "Violets"}

    def __init__(self, diagram, students=CHILDRENS):
        self.diagram = [list(s) for s in diagram.split("\n")]
        self.students = sorted(students)

    def plants(self, student: str) -> list[str]:
        """plants"""

        i = self.students.index(student)
        return [
            Garden.names[plant]
            for row in self.diagram
            for plant in (row[2 * i], row[2 * i + 1])
        ]
