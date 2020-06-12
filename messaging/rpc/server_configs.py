import os
import abc
from urllib.parse import urlparse
from common.util import DictModel


env = os.environ

class ServerConfig(DictModel):
    DEFAULT_URI = 'grpc://localhost:8000'
    DEFAULT_REGISTERY_SERVICE_URI = 'grpc://localhost:50001'
    DEFAULT_SERVER_NETWORK_INTERFACE = '[::]'

    @classmethod
    def from_env(cls):
        assert env.get('NODE_UUID'), '"NODE_UUID" environment variable was not set.'
        config = cls()
        config.uuid = env.get('NODE_UUID')
        config.uri = env.get('NODE_URI') or cls.DEFAULT_URI
        config.server_network_interface = env.get('SERVER_NETWORK_INTERFACE') or cls.DEFAULT_SERVER_NETWORK_INTERFACE
        config.server_network_port = env.get('SERVER_NETWORK_PORT') or (
            int(
                urlparse(config.uri).netloc.split(':')[1]
            )
        )
        config.registry_service_uri = env.get('REGISTERY_SERVICE_URI') or cls.DEFAULT_REGISTERY_SERVICE_URI
        return config


class RegistryServerConfig(ServerConfig):
    DEFAULT_URI = 'grpc://localhost:50001'


class ClockNodeServerConfig(ServerConfig):
    DEFAULT_URI = 'grpc://localhost:10000'
    DEFAULT_TICKER_TYPE = 'apscheduler_redis'
    DEFAULT_MAX_SCHEDULE_COUNT = 10000
    DEFAULT_APS_REDIS_DB = 0
    DEFAULT_APS_MISFIRE_GRACE_TIME = 59
    DEFAULT_APS_MAX_EXECUTERS = 5
    DEFAULT_APS_REDIS_HOST = 'localhost'
    DEFAULT_APS_REDIS_PORT = 6379

    @classmethod
    def from_env(cls):
        config = super(cls, cls).from_env()
        minute = env.get('CLOCK_MINUTE')
        assert minute is not None, '"CLOCK_MINUTE" environment variable was not set.'
        config.minute = int(minute)
        config.ticker_type = env.get('TICKER_TYPE', cls.DEFAULT_TICKER_TYPE)
        config.max_schedule_count = env.get('MAX_SCHEDULE_COUNT') or cls.DEFAULT_MAX_SCHEDULE_COUNT
        if config.ticker_type == 'apscheduler_redis':
            config.ticker_config = cls._aps_ticker_config_from_env(config)
        return config

    @classmethod
    def _aps_ticker_config_from_env(cls, server_config):
        return DictModel(
            max_executors=env.get('APS_MAX_EXECUTERS', cls.DEFAULT_APS_MAX_EXECUTERS),
            misfire_grace_time=env.get('APS_MISFIRE_GRACE_TIME', cls.DEFAULT_APS_MISFIRE_GRACE_TIME),
            redis_jobstore_db=int(env.get('APS_REDIS_DB', cls.DEFAULT_APS_REDIS_DB)),
            redis_host=env.get('APS_REDIS_HOST', cls.DEFAULT_APS_REDIS_HOST),
            redist_port=int(env.get('APS_REDIS_PORT', cls.DEFAULT_APS_REDIS_PORT)),
            redis_jobs_key=f'clocknode.jobs.{server_config.uuid}',
            redis_runtimes_key=f'clocknode.runtimes.{server_config.uuid}',
        )
