import os
from data.time import time_seed
from data.lesson import lesson_seed


def seed():
    try:
        os.remove("./tmp/lesson.csv")
        os.remove("./tmp/time.csv")
    except Exception:
        pass

    time_seed()
    lesson_seed()


seed()
