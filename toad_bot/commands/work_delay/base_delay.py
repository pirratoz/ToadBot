from datetime import timedelta


class WorkTimeDelaySec:
    seconds = 60
    def __init__(self):
        self.walk_to_work: int = 0
        self.work_time: int = 0
        self.next_opportunity_to_work: int = 0
        self.command: str = ""

    def next_work_delay(self) -> timedelta:
        return timedelta(
            seconds=self.walk_to_work + self.work_time + self.next_opportunity_to_work
        )
