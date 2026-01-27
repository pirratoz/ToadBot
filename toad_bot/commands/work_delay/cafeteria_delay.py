from toad_bot.commands.work_delay.base_delay import WorkTimeDelaySec


class CafeteriaWork(WorkTimeDelaySec):
    def __init__(self):
        _work_delay = 1 * self.seconds
        _walk_delay = 1 * self.seconds
        _opportunity_work_delay = 1 * self.seconds
        super().__init__()
        self.walk_to_work = 10 * self.seconds + _walk_delay
        self.work_time = 120 * self.seconds + _work_delay
        self.next_opportunity_to_work = 6 * self.seconds + _opportunity_work_delay
        self.command = "@toadbot Отправиться в кафетерий"
