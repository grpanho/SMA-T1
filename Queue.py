class Queue:
    def __init__(self):
        self.name = ""
        self.servers = 0
        self.capacity = 0
        self.states = []
        self.clients = 0
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
    
    def start_states(self):
        if self.capacity == 0:
            print("Capacity must be greater than 0")
            exit(1)
        self.states = [0] * (self.capacity + 1)

    def set_state(self, state, time):
        self.states[state] += time

    def set_clients(self, clients):
        if clients < 0:
            clients = 0
        self.clients = clients

    def set_min_arrival(self, min_arrival):
        self.min_arrival = min_arrival

    def set_max_arrival(self, max_arrival):
        self.max_arrival = max_arrival

    def set_min_service(self, min_service):
        self.min_service = min_service

    def set_max_service(self, max_service):
        self.max_service = max_service

    def get_name(self):
        return self.name

    def get_servers(self):
        return self.servers

    def get_capacity(self):
        return self.capacity
    
    def get_states(self):
        return self.states
    
    def get_clients(self):
        return self.clients

    def get_min_arrival(self):
        return self.min_arrival

    def get_max_arrival(self):
        return self.max_arrival

    def get_min_service(self):
        return self.min_service

    def get_max_service(self):
        return self.max_service
