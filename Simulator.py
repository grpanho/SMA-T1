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

    Q1 = scheduler.queueList["Q1"]
    scheduler.agenda_evento(Event("CHEGADA", 2.0, Q1))

    while not scheduler.end():
        event = scheduler.pop_event()

        for queue in scheduler.queueList.values():
            queue.set_state(queue.get_clients(), (event.get_event_time() - scheduler.get_timer()))
        
        scheduler.set_timer(event.get_event_time())

        if event.destQueue != None:
            print(scheduler.timer, event.event_type, event.event_time, event.get_originQueue().get_name(),event.destQueue.get_name())
        else:
            print(scheduler.timer, event.event_type, event.event_time, event.get_originQueue().get_name())
        #input()

        if event.event_type == "CHEGADA":
            scheduler.chegada(event)
        elif event.event_type == "TRANSICAO":
            scheduler.transicao(event)
        else:
            scheduler.saida(event)

    scheduler.report()

if __name__ == "__main__":
    simulate()
