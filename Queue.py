class Queue:
    def __init__(self):
        self.name = ""
        self.servers = 0
        self.capacity = 0
        self.min_arrival = 0
        self.max_arrival = 0
        self.min_service = 0
        self.max_service = 0

    def set_name(self, name):
        self.name = name

    def set_servers(self, servers):
        self.servers = servers

    def set_capacity(self, capacity):
        self.capacity = capacity

    def set_min_arrival(self, min_arrival):
        self.min_arrival = min_arrival

    def set_max_arrival(self, max_arrival):
        self.max_arrival = max_arrival

    def set_min_service(self, min_service):
        self.min_service = min_service

    def set_max_service(self, max_service):
        self.max_service = max_service
