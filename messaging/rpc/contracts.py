import abc

class ClockNodeContract(metaclass=abc.ABCMeta):
    """ Contract Mixin for clock node rpc clients and server """

    @abc.abstractmethod
    def add_schedule(self, msg):
        ...

    @abc.abstractmethod
    def remove_schedule(self, msg):
        ...

    @abc.abstractmethod
    def replace_schedules(self, msg):
        ...

    @abc.abstractmethod
    def health_ping(self, msg):
        ...


class RegistryServiceContract(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def register_clocknode(self, msg):
        ...

