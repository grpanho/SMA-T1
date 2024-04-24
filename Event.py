class Event:
    def __init__(self, event_type, draw, system_time):
        self.arrival_time = system_time + draw
        self.event_type = event_type

    def __lt__(self, other):
        return self.arrival_time < other.arrival_time