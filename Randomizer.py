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

def saida(event, estados, simulacao, randomizador, event_list):
    fila = simulacao.fila

    estados[simulacao.fila] += event.arrival_time - simulacao.timer
    simulacao.timer = event.arrival_time
    simulacao.fila -= 1

    if simulacao.fila >= simulacao.get_servidores():
        agend_saida(randomizador.range(simulacao.get_min_saida(), simulacao.get_max_saida()), simulacao, event_list)

def chegada(event, estados, simulacao, randomizador, event_list):
    fila = simulacao.fila

    estados[simulacao.fila] += event.arrival_time - simulacao.timer
    simulacao.timer = event.arrival_time

    if fila < simulacao.get_max_fila():
        simulacao.fila += 1
        if simulacao.fila <= simulacao.get_servidores():
            agend_saida(randomizador.range(simulacao.get_min_saida(), simulacao.get_max_saida()), simulacao, event_list)
    else:
        simulacao.losses += 1

    agend_chegada(randomizador.range(simulacao.get_min_chegada(), simulacao.get_max_chegada()), simulacao, event_list)

def agend_saida(range_val, simulacao, event_list):
    heapq.heappush(event_list, Event("SAIDA", range_val, simulacao.timer))

def agend_chegada(range_val, simulacao, event_list):
    heapq.heappush(event_list, Event("CHEGADA", range_val, simulacao.timer))