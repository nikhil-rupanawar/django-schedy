from common.util import DictModel

class DictMessage(DictModel):
    pass


class M_ClockNode(DictMessage):
    def __init__(self, uuid, uri, minute, max_schedule_count):
        self.uuid = uuid
        self.uri = uri
        self.max_schedule_count = max_schedule_count
        self.minute = minute


class M_RegisterClockNodeRequest(DictMessage):
    def __init__(self, node, reschedule_on_registration=True):
        self.node = node
        self.reschedule_on_registration = reschedule_on_registration


