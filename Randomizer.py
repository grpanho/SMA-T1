import heapq
from Event import *
from Queue import Queue
import yaml

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
        self.queueList = {}

    def set_queues(self, queuesYaml):
        with open(queuesYaml, 'r') as file:
            self.queueData = yaml.safe_load(file)

        self.maxIterations = int(self.queueData['maxIterations'])
        for queue in self.queueData['queues']:
            self.queueList[queue] = Queue()  # Cria uma nova fila com o nome especificado
            self.queueList[queue].set_name(queue)  # Define o nome da fila
            self.queueList[queue].set_servers(int(self.queueData['queues'][queue]['servers']))
            self.queueList[queue].set_capacity(int(self.queueData['queues'][queue]['capacity']))
#            self.queueList[queue].start_states()  # Inicializa o estado da fila
#            self.queueList[queue].set_state(0, 0.0)  # Adiciona o tempo inicial ao estado da fila
            if "minArrival" in self.queueData['queues'][queue] and "maxArrival" in self.queueData['queues'][queue]:
                self.queueList[queue].set_min_arrival(float(self.queueData['queues'][queue]['minArrival']))
                self.queueList[queue].set_max_arrival(float(self.queueData['queues'][queue]['maxArrival']))
            self.queueList[queue].set_min_service(float(self.queueData['queues'][queue]['minService']))
            self.queueList[queue].set_max_service(float(self.queueData['queues'][queue]['maxService']))
            for destQueue in self.queueData['queues'][queue]['output']:
                self.queueList[queue].set_output(destQueue, float(self.queueData['queues'][queue]["output"][destQueue]))

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

    def saida(self, event, event_list):
        queue = self.queueList.get(event.originQueue)

        queue.set_state(queue.get_clients(), (event.arrival_time - self.simulator.get_timer()))
        self.simulator.set_timer(event.arrival_time)
        queue.set_clients(queue.get_clients() - 1)
        if queue.get_clients() >= queue.get_servers():
            range = self.range(0, 1)
            dest = queue.calculate_output(range)
            if dest != "OUT":
                event = Event("TRANSICAO", self.range(queue.get_min_arrival(), queue.get_max_arrival()), self.simulator.get_timer(), queue, self.queueList[dest])
                self.agenda_evento(event, event_list)
        else:
            event = Event("SAIDA", self.range(queue.get_min_service(), queue.get_max_service()), self.simulator.get_timer(), queue)
            self.agenda_evento(event, event_list)

    def chegada(self, event, event_list):
        print(self.queueList.get(event.get_originQueue()).get_name())
        queue = self.queueList.get(event.get_originQueue())

        queue.set_state(queue.get_clients(), (event.arrival_time - self.simulator.get_timer()))
        self.simulator.set_timer(event.arrival_time)

        if queue.get_clients() < queue.get_capacity():
            queue.set_clients(queue.get_clients() + 1)

            if queue.get_clients() <= queue.get_servers():
                range = self.range(0, 1)
                dest = queue.calculate_output(range)
                if dest != "OUT":
                    event = Event("TRANSICAO", self.range(queue.get_min_arrival(), queue.get_max_arrival()), self.simulator.get_timer(), queue, self.queueList[dest])
                    self.agenda_evento(event, event_list)
                else:
                    event = Event("SAIDA", self.range(queue.get_min_service(), queue.get_max_service()), self.simulator.get_timer(), queue)
                    self.agenda_evento(event, event_list)
        else:
            queue.set_losses(queue.get_losses() + 1)

        event = Event("CHEGADA", self.range(queue.get_min_service(), queue.get_max_service()), self.simulator.get_timer(), queue)
        self.agenda_evento(event, event_list)

    def transicao(self, event, event_list):
        originQueue = event.get_originQueue()
        destQueue = event.get_destQueue()
        originQueue.set_state(originQueue.get_clients(), (event.arrival_time - self.simulator.get_timer()))
        self.simulator.set_timer(event.arrival_time)
        originQueue.set_clients(originQueue.get_clients() - 1)

        if originQueue.get_clients() >= originQueue.get_servers():
            range = self.range(0, 1)
            dest = originQueue.calculate_output(range)
            if dest != "OUT":
                event = Event("TRANSICAO", self.range(destQueue.get_min_arrival(), destQueue.get_max_arrival()), self.simulator.get_timer(), originQueue, self.queueList[dest])
                self.agenda_evento(event, event_list)
            else:
                event = Event("SAIDA", self.range(destQueue.get_min_service(), destQueue.get_max_service()), self.simulator.get_timer(), originQueue)
                self.agenda_evento(event, event_list)

            destQueue.set_clients(destQueue.get_clients() + 1)
            if destQueue.get_clients() <= destQueue.get_servers():
                event = Event("SAIDA", self.range(destQueue.get_min_service(), destQueue.get_max_service()), self.simulator.get_timer(), destQueue)
                self.agenda_evento(event, event_list)

    def agenda_evento(self, event, event_list):
        heapq.heappush(event_list, event)