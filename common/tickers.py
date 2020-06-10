import os
from apscheduler.executors.pool import ThreadPoolExecutor
from apscheduler.schedulers.background import BackgroundScheduler


class InMemoryApSchedulerTickerMixin:

    @property
    def ticker(self):
        return self._ticker

    @property
    def ticker_config(self):
        return {
            'max_executors': os.environ.get('MAX_EXCECUTORS', 5),
            'misfire_grace_time': os.environ.get('MISFIRE_GRACE_TIME', 59),
            'scheduler_type': 'background',
        }

    def init_ticker(self):
        config = self.ticker_config
        self._ticker = BackgroundScheduler(
            executors={'default': ThreadPoolExecutor(config['max_executors'])},
            job_defaults={'misfire_grace_time': config['misfire_grace_time']}
        )

    def start_ticker(self):
        self.ticker.start()

    def stop_ticket(self):
        self.ticker.stop()
