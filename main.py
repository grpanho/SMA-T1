import heapq
from sys import argv
from Event import *
from Randomizer import *
from Simulator import *

def main():
    if len(argv) < 2:
        print("Nenhuma fila foi passada como argumento.")
        exit(1)

    simulacao = Simulator(0, 0)
    simulacao.set_params(argv[1])

    CHEGADA = "CHEGADA"
    randomizer = Randomizer(4, simulacao.get_seed(), 240, 1000, simulacao.get_rand_numbers(), simulacao)
    event_list = []

    for i in range(simulacao.get_max_fila() + 1):
        simulacao.estados.append(0.0)

    heapq.heappush(event_list, Event(CHEGADA, 0, simulacao.timer))

    while event_list:
        event = heapq.heappop(event_list)
        if event.event_type == CHEGADA:
            chegada(event, simulacao.estados, simulacao, randomizer, event_list)
        else:
            saida(event, simulacao.estados, simulacao, randomizer, event_list)

if __name__ == "__main__":
    main()
