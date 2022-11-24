import time

from config import settings
from task_service import TaskService


if __name__ == "__main__":

    svc = TaskService()
    while True:
        print("start iter")
        svc.check_tasks()
        time.sleep(settings.polling_frequency)
