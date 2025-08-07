import logging


class MicrosecondFormatter(logging.Formatter):
    def format(self, record):
        record.unix_micro_ts = int(record.created * 1000000)
        return super().format(record)
