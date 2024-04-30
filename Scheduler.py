import heapq
import yaml
from PseudoRandom import *
from Event import *
from Queue import Queue

class Scheduler:
    def __init__(self):
        self.maxRndNumbers = 100000
        self.timer = 0
        self.queueList = {}
        self.eventList = []
        self.pseudoRandom = None

    def set_yaml_data(self, queuesYaml):
        with open(queuesYaml, 'r') as file:
            self.queueData = yaml.safe_load(file)

        self.pseudoRandom = PseudoRandom(int(self.queueData['seed']))

        self.maxRndNumbers = int(self.queueData['maxRndNumbers'])
        for queue in self.queueData['queues']:
            self.queueList[queue] = Queue(queue)
            self.queueList[queue].set_servers(int(self.queueData['queues'][queue]['servers']))
            self.queueList[queue].set_capacity(self.queueData['queues'][queue]['capacity'])
            if "minArrival" in self.queueData['queues'][queue] and "maxArrival" in self.queueData['queues'][queue]:
                self.queueList[queue].set_min_arrival(float(self.queueData['queues'][queue]['minArrival']))
                self.queueList[queue].set_max_arrival(float(self.queueData['queues'][queue]['maxArrival']))
            self.queueList[queue].set_min_service(float(self.queueData['queues'][queue]['minService']))
            self.queueList[queue].set_max_service(float(self.queueData['queues'][queue]['maxService']))
            for destQueue in self.queueData['queues'][queue]['output']:
                self.queueList[queue].set_output(destQueue, float(self.queueData['queues'][queue]["output"][destQueue]))

    def saida(self, event):
        queue = event.get_originQueue()
        nextEventTime = self.pseudoRandom.range(queue.get_min_arrival(), queue.get_max_arrival()) + self.timer
        self.maxRndNumbers -= 1

        queue.set_state(queue.get_clients(), (event.arrival_time - self.timer))
        self.timer = event.arrival_time
        queue.set_clients(queue.get_clients() - 1)

        if queue.get_clients() >= queue.get_servers():
            dest = queue.calculate_output(self.pseudoRandom.range(0, 1))
            self.maxRndNumbers -= 1
            print(dest)
            if dest != "OUT":
                event = Event("TRANSICAO", nextEventTime, queue, self.queueList[dest])
                self.agenda_evento(event)
            else:
                event = Event("SAIDA", nextEventTime, queue)
                self.agenda_evento(event)

    def chegada(self, event):
        queue = event.get_originQueue()

        queue.set_state(queue.get_clients(), (event.get_arrival_time() - self.timer))
        self.timer = event.get_arrival_time()

        if queue.get_capacity() == "INFINITE" or queue.get_clients() < queue.get_capacity():
            queue.set_clients(queue.get_clients() + 1)

            if queue.get_clients() <= queue.get_servers():
                dest = queue.calculate_output(self.pseudoRandom.range(0, 1))
                eventTime = self.pseudoRandom.range(queue.get_min_arrival(), queue.get_max_arrival()) + self.timer
                self.maxRndNumbers -= 2
                if dest != "OUT":
                    event = Event("TRANSICAO", eventTime, queue, self.queueList[dest])
                    self.agenda_evento(event)
                else:
                    event = Event("SAIDA", eventTime, queue)
                    self.agenda_evento(event,)
        else:
            queue.set_losses(queue.get_losses() + 1)

        eventTime = self.pseudoRandom.range(queue.get_min_arrival(), queue.get_max_arrival()) + self.timer
        self.maxRndNumbers -= 1
        event = Event("CHEGADA", eventTime, queue)
        self.agenda_evento(event)

    def transicao(self, event):
        originQueue = event.get_originQueue()
        destQueue = event.get_destQueue()

        originQueue.set_state(originQueue.get_clients(), (event.arrival_time - self.timer))
        self.timer = event.arrival_time
        originQueue.set_clients(originQueue.get_clients() - 1)

        if originQueue.get_clients() >= originQueue.get_servers():
            dest = originQueue.calculate_output(self.pseudoRandom.range(0, 1))
            eventTime = self.pseudoRandom.range(originQueue.get_min_arrival(), originQueue.get_max_arrival()) + self.timer
            self.maxRndNumbers -= 2
            if dest != "OUT":
                event = Event("TRANSICAO", eventTime, originQueue, self.queueList[dest])
                self.agenda_evento(event)
            else:
                event = Event("SAIDA", eventTime, originQueue)
                self.agenda_evento(event)

            destQueue.set_clients(destQueue.get_clients() + 1)
            if destQueue.get_clients() <= destQueue.get_servers():
                eventTime = self.pseudoRandom.range(originQueue.get_min_arrival(), originQueue.get_max_arrival()) + self.timer
                self.maxRndNumbers -= 1
                event = Event("SAIDA", eventTime, destQueue)
                self.agenda_evento(event)

    def agenda_evento(self, event):
        heapq.heappush(self.eventList, event)

    def pop_event(self):
        return heapq.heappop(self.eventList)

    def report(self):
        print("==========================================================")
        print("=----------------------RELATORIO-------------------------=")
        for queueName, fila in self.queueList.items():
            queue = self.queueList[queueName]
            print(f"Fila: {queueName}")
            print("Estado  Tempo       Probabilidade")
            for state, state_time in queue.get_states().items():
                print(f"{state:<6d}  {state_time:<11.4f}  {(state_time * 100) / self.timer:.2f}%")
            print("Numero de perdas:", queue.get_losses())
            print("=======================================================")

    def get_maxRndNumbers(self):
        return self.maxRndNumbers