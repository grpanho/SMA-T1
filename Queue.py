class Queue:
    def __init__(self, name: str):
        self.name = name
        self.servers = 0
        self.capacity = 0
        self.states = {}
        self.clients = 0
        self.losses = 0
        self.min_arrival = 0
        self.max_arrival = 0
        self.min_service = 0
        self.max_service = 0
        self.output = {}

    def set_name(self, name):
        self.name = name

    def set_servers(self, servers):
        self.servers = servers

    def set_capacity(self, capacity):
        self.capacity = capacity

    def set_state(self, state, time):
        if state not in self.states:
            self.states[state] = time
        else:
            self.states[state] += time

    def set_clients(self, clients):
        if clients < 0:
            clients = 0
        self.clients = clients

    def set_losses(self, losses):
        self.losses = losses

    def set_min_arrival(self, min_arrival):
        self.min_arrival = min_arrival

    def set_max_arrival(self, max_arrival):
        self.max_arrival = max_arrival

    def set_min_service(self, min_service):
        self.min_service = min_service

    def set_max_service(self, max_service):
        self.max_service = max_service

    def set_output(self, destQueue, probability):
        self.output[destQueue] = probability

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

    def get_losses(self):
        return self.losses

    def get_min_arrival(self):
        return self.min_arrival

    def get_max_arrival(self):
        return self.max_arrival

    def get_min_service(self):
        return self.min_service

    def get_max_service(self):
        return self.max_service

    def get_output(self):
        return self.output

    def calculate_output(self, rand):
        if self.output == {}:
            return "OUT"
        currProb = 0
        for destQueue in self.output:
            currProb += self.output[destQueue]
            if rand <= currProb:
                return destQueue

    def printQ(self):
        return f"Name: {self.name}\n Servers: {self.servers}\n Capacity: {self.capacity}\n States: {self.states}\n Clients: {self.clients}\n Min Arrival: {self.min_arrival}\n Max Arrival: {self.max_arrival}\n Min Service: {self.min_service}\n Max Service: {self.max_service}\n Output: {self.output}"