import heapq
from Event import *

class Randomizer:
    def __init__(self, a, seed, c, m, max_rand_num, simulator):
        self.a = a
        self.seed = seed
        self.c = c
        self.m = m
        self.max_rand_num = max_rand_num
        self.simulator = simulator
        self.count = 0
        self.list_mode = False
        self.rnd_list = []

    def set_list_mode(self, rnd_list):
        self.list_mode = True
        self.rnd_list = rnd_list

    def rand(self):
        if self.count == self.max_rand_num - 1:
            self.simulator.end_n_report()
            exit(0)

        self.count += 1
        self.seed = (self.a * self.seed + self.c) % self.m

        if self.list_mode:
            return self.rnd_list[self.count - 1]

        return self.seed / self.m

    def range(self, a, b):
        return (b - a) * self.rand() + a

    def saida(self, queue, event, simulacao, event_list):

        print(queue.get_states())
        print(queue.get_clients())

        queue.set_state(queue.get_clients(), (event.arrival_time - simulacao.timer))
        simulacao.timer = event.arrival_time
        queue.set_clients(queue.get_clients() - 1)

        if queue.get_clients() >= queue.get_servers():
            self.agend_saida(self.range(queue.get_min_service(), queue.get_max_service()), simulacao, event_list)

    def chegada(self, queue, event, simulacao, event_list):
        queue.set_state(queue.get_clients(), (event.arrival_time - simulacao.timer))
        simulacao.timer = event.arrival_time

        if queue.get_clients() < queue.get_capacity():
            queue.set_clients(queue.get_clients() + 1)

            if queue.get_clients() <= queue.get_servers():
                self.agend_saida(self.range(queue.get_min_service(), queue.get_max_service()), simulacao, event_list)
        else:
            simulacao.losses += 1

        self.agend_chegada(self.range(queue.get_min_arrival(), queue.get_max_arrival()), simulacao, event_list)

    def agend_saida(self, range_val, simulacao, event_list):
        heapq.heappush(event_list, Event("SAIDA", range_val, simulacao.timer))

    def agend_chegada(self, range_val, simulacao, event_list):
        heapq.heappush(event_list, Event("CHEGADA", range_val, simulacao.timer))