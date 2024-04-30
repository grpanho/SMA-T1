import heapq
from sys import argv
from Event import *
from Randomizer import *
from Simulator import *

def main():
    if len(argv) < 2:
        print("Nenhuma fila foi passada como argumento.")
        exit(1)

    simulacao  = Simulator()
    randomizer = Randomizer(4, simulacao.get_seed(), 240, 1000, simulacao.get_maxIterations(), simulacao)
    randomizer.set_queues(argv[1])
    event_list = []

    heapq.heappush(event_list, Event("CHEGADA", 0, simulacao.timer, "Q1"))

    while event_list:
        event = heapq.heappop(event_list)
        print(simulacao.timer, event.event_type, event.arrival_time)
        input()

        if event.event_type == "CHEGADA":
            randomizer.chegada(event, event_list)
        elif event.event_type == "TRANSICAO":
            randomizer.transicao(event, event_list)
        else:
            randomizer.saida(event, event_list)

if __name__ == "__main__":
    main()
