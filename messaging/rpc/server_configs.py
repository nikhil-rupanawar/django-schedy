import os
from common.util import DictModel


class ServerConfig(DictModel):
    def __init__(self, *args, **kwargs):
        self.uri = self.uri

    @classmethod
    def from_env_vars(cls):
        pass


class ClockNodeServerConfig(ServerConfig):
    DEFAULT_URI = 'grpc://localhost:10000'
    DEFAULT_REGISTERY_SERVICE_URI = 'grpc://localhost:50001'
    DEFAULT_TICKER_TYPE = 'apscheduler_redis'
    DEFAULT_MAX_SCHEDULE_COUNT = 10000
    DEFAULT_APS_REDIS_DB = 0
    DEFAULT_APS_MISFIRE_GRACE_TIME = 59
    DEFAULT_APS_MAX_EXECUTERS = 5
    DEFAULT_APS_REDIS_HOST = 'localhost'
    DEFAULT_APS_REDIS_PORT = 6379
    DEFAULT_SERVER_NETWORK_INTERFACE = '[::]'
    DEFAULT_SERVER_NETWORK_PORT = 10000

    def __init__(self,
        uuid,
        minute,
        uri=None,
        registry_service_uri=None,
        ticker_type=None,
        max_schedule_count=None,
        server_network_interface=None,
        server_network_port=None
    ):
        self.uuid = uuid
        self.minute = int(minute)
        self.uri = uri or self.DEFAULT_URI
        self.registry_service_uri = registry_service_uri or self.DEFAULT_REGISTERY_SERVICE_URI
        self.ticker_type = ticker_type or self.DEFAULT_TICKER_TYPE
        self.max_schedule_count = max_schedule_count = self.DEFAULT_MAX_SCHEDULE_COUNT
        self.server_network_interface = server_network_interface or self.DEFAULT_SERVER_NETWORK_INTERFACE
        self.server_network_port = int(server_network_port or self.DEFAULT_SERVER_NETWORK_PORT)

    @classmethod
    def read_from_env(cls):
        uuid = os.environ.get('CLOCKNODE_UUID')
        minute = os.environ.get('CLOCKNODE_MINUTE')
        assert uuid, '"CLOCKNODE_UUID" environment variable is not set.'
        assert minute is not None, '"CLOCKNODE_MINUTE" environment variable is not set.'

        config = cls(
            uuid,
            minute,
            os.environ.get('CLOCK_NODE_URI'),
            os.environ.get('REGISTERY_SERVICE_URI'),
            ticker_type=os.environ.get('TICKER_TYPE'),
            max_schedule_count=os.environ.get('MAX_SCHEDULE_COUNT'),
            server_network_interface=os.environ.get('SERVER_NETWORK_INTERFACE'),
            server_network_port=os.environ.get('SERVER_NETWORK_PORT')
        )
        if config.ticker_type == 'apscheduler_redis':
            config.ticker_config = cls._aps_ticker_config_from_env(config)
        return config

    @classmethod
    def _aps_ticker_config_from_env(cls, server_config):
        return DictModel(
            max_executors=os.environ.get('APS_MAX_EXECUTERS', cls.DEFAULT_APS_MAX_EXECUTERS),
            misfire_grace_time=os.environ.get('APS_MISFIRE_GRACE_TIME', cls.DEFAULT_APS_MISFIRE_GRACE_TIME),
            redis_jobstore_db=int(os.environ.get('APS_REDIS_DB', cls.DEFAULT_APS_REDIS_DB)),
            redis_host=os.environ.get('APS_REDIS_HOST', cls.DEFAULT_APS_REDIS_HOST),
            redist_port=int(os.environ.get('APS_REDIS_PORT', cls.DEFAULT_APS_REDIS_PORT)),
            redis_jobs_key=f'clocknode.jobs.{server_config.uuid}',
            redis_runtimes_key=f'clocknode.runtimes.{server_config.uuid}',
        )

