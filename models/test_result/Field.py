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
