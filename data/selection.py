from tempfile import NamedTemporaryFile
import shutil
import csv
import typing

from data.data import Data
from data.lesson import Lesson


class Selection(Data):
    def __init__(self):
        super().__init__("selection", ["student_id", "lesson_ids"])

    def find_with_student_id(self, student_id: str):
        data = self.find_all(student_id=student_id)
        if len(data):
            return data[0]
        raise Exception("You have not yet select lessons")

    def update_selection(self, id: str, lesson_ids: typing.List[str]):
        tempfile = NamedTemporaryFile(mode="w", delete=False)
        with open(self.filename, "r") as f, tempfile:
            reader = csv.DictReader(f, fieldnames=self.headers)
            writer = csv.DictWriter(tempfile, fieldnames=self.headers)
            for row in reader:
                if row["id"] == id:
                    row["lesson_ids"] = lesson_ids
                    writer.writerow(row)

        shutil.move(tempfile.name, self.filename)

    def select(self, student_id: str, new_lesson_code: str):
        lesson = Lesson()

        new_lesson = lesson.find(new_lesson_code)
        if not new_lesson:
            raise Exception(
                "there is not any lesson with code: {}".format(new_lesson_code)
            )

        try:
            other_lessons = []
            data = self.find_with_student_id(student_id)

            for lesson_code in data["lesson_ids"]:
                other_lessons.append(lesson.find(lesson_code))

            conflicts = lesson.check_for_conflict(new_lesson, other_lessons)
            if len(conflicts):
                conflicts_names = ""
                for conflict in conflicts:
                    conflicts_names += ", " + conflict["name"]

                error = "{} has conflict with {}".format(
                    new_lesson["name"], conflicts_names
                )
                raise Exception(error)

            other_lessons.append(new_lesson)

            self.update_selection(
                data["id"], lesson_ids=[lesson["code"] for lesson in other_lessons]
            )

        except Exception:
            self.insert({"student_id": student_id, "lesson_ids": [new_lesson["code"]]})
