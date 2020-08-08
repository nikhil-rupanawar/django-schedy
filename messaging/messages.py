from common.util import DictModel
from typing import Type, List


class BaseMessage(DictModel):
    NESTED_TYPE_MAP = {}
    def __str__(self):
        return f"Object of {self.__class__} {super().__str__()}"


class M_ClockNode(BaseMessage):
    def __init__(self, uuid=None, uri=None, minute=None, max_schedule_count=None):
        self.uuid = uuid
        self.uri = uri
        self.max_schedule_count = max_schedule_count
        self.minute = minute


class M_RegisterClockNodeRequest(BaseMessage):
    NESTED_TYPE_MAP = {'node': M_ClockNode }
    def __init__(self, node=None, reschedule_on_registration=True):
        self.node = node
        self.reschedule_on_registration = reschedule_on_registration


class M_RegisterClockNodeResponse(BaseMessage):
    pass
