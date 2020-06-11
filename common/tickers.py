import os
from apscheduler.executors.pool import ThreadPoolExecutor
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores import redis
from common.util import DictModel


class BaseTicker:
    def __init__(self, ticker_config):
        self.ticker_config = ticker_config
        self._ticker_instance = None

    @property
    def ticker_instance(self):
        assert self._ticker_instance is not None
        return self._ticker_instance

    def init_ticker(self):
        pass

    def start(self):
        pass

    def stop(self):
        pass

    def add_job(self, *args, **kwargs):
        pass

    def remove_job(self, *args, **kwargs):
        pass


def Ticker(ticker_type, ticker_config):
    if ticker_type == 'apscheduler_redis':
        return ApSchedulerRedisTicker(ticker_config)
    else:
        raise Exception(f'ticker type {ticker_type} is not supported')


class ApSchedulerRedisTicker(BaseTicker):

    def init_ticker(self):
        config = self.ticker_config
        jobstore = redis.RedisJobStore(
            db=config.redis_jobstore_db,
            jobs_key=config.redis_jobs_key,
            run_times_key=config. redis_runtimes_key,
            host=config.redis_host,
            port=config.redist_port,
        )
        self._ticker_instance = BackgroundScheduler(
            executors={'default': ThreadPoolExecutor(config.max_executors)},
            job_defaults={'misfire_grace_time': config.misfire_grace_time},
            jobstores={'default': jobstore} 
        )

    def start_ticker(self):
        self.ticker.start()

    def stop_ticket(self):
        self.ticker.shutdown(wait=False)

