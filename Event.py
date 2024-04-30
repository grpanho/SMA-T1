class Event:
    def __init__(self, event_type, draw, system_time, originQueue, destQueue = None):
        self.arrival_time = system_time + draw
        self.event_type = event_type
        self.originQueue = originQueue
        self.destQueue = destQueue

    def __lt__(self, other):
        return self.arrival_time < other.arrival_time

    def get_originQueue(self):
        return self.originQueue

    def get_destQueue(self):
        return self.destQueue