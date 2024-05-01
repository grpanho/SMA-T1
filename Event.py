from Queue import Queue
class Event:
    def __init__(self, event_type, event_time, originQueue = None, destQueue = None):
        self.event_time = event_time
        self.event_type = event_type
        self.originQueue = originQueue
        self.destQueue = destQueue

    def __lt__(self, other):
        return self.event_time < other.event_time

    def get_event_time(self):
        return self.event_time
    
    def get_event_type(self):
        return self.event_type

    def get_originQueue(self):
        return self.originQueue

    def get_destQueue(self):
        return self.destQueue