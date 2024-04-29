import heapq
from sys import argv
from Event import *
from Randomizer import *
from Simulator import *

def main():
    if len(argv) < 2:
        print("Nenhuma fila foi passada como argumento.")
        exit(1)

    simulacao = Simulator()
    simulacao.set_queues(argv[1])

    CHEGADA = "CHEGADA"
    randomizer = Randomizer(4, simulacao.get_seed(), 240, 1000, simulacao.get_maxIterations(), simulacao)
    event_list = []

#    for queue in simulacao.queueList:
#        simulacao.queueList[queue].set_state(0, 0.0)

    heapq.heappush(event_list, Event(CHEGADA, 0, simulacao.timer))

    while event_list:
        event = heapq.heappop(event_list)

        for queueName in simulacao.queueList:
            queue = simulacao.queueList[queueName]
            if event.event_type == CHEGADA:
                randomizer.chegada(queue, event, simulacao, event_list)
            else:
                randomizer.saida(queue, event, simulacao, event_list)

if __name__ == "__main__":
    main()
