import logging

class Field:
    def __init__(self):
        self.status = None
        self.log_level = None
        self.message = None
        self.duration = None
    
    def set_status(self, status):
        self.status = status
        return self
    
    def set_log_level(self, log_level):
        self.log_level = log_level
        return self
    
    def set_message(self, message):
        self.message = message
        return self
    
    def set_duration(self, duration):
        self.duration = duration
        return self
    
    def get_log_level(self):
        if self.log_level == logging.DEBUG:
            return "DEBUG"
        elif self.log_level == logging.INFO:
            return "INFO"
        elif self.log_level == logging.WARNING:
            return "WARNING"
        elif self.log_level == logging.ERROR:
            return "ERROR"
        elif self.log_level == logging.CRITICAL:
            return "CRITICAL"
        else:
            return "INFO"
