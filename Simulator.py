import heapq
from sys import argv
from Event import *
from Scheduler import *
from Simulator import *

def simulate():
    if len(argv) < 2:
        print("Nenhuma fila foi passada como argumento.")
        exit(1)

    scheduler = Scheduler()
    scheduler.set_yaml_data(argv[1])
    count = 0

    Q1 = scheduler.queueList["Q1"]
    scheduler.agenda_evento(Event("CHEGADA", 0, Q1))

    while scheduler.get_maxRndNumbers() != 0:
        nextEvent = scheduler.pop_event()
        print(scheduler.timer, nextEvent.event_type, nextEvent.arrival_time, nextEvent.get_originQueue().get_name())
        #input()

        if nextEvent.event_type == "CHEGADA":
            scheduler.chegada(nextEvent)
        elif nextEvent.event_type == "TRANSICAO":
            scheduler.transicao(nextEvent)
        else:
            scheduler.saida(nextEvent)
        
        count += 1

    scheduler.report()

if __name__ == "__main__":
    simulate()
