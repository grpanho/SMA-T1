from Queue import *
from ConfigHandler import *

class Simulator:
    def __init__(self, timer, fila):
        self.timer = timer
        self.fila = fila
        self.estados = [0.0]
        self.losses = 0
        self.rand_numbers = 0
        self.seed = 21
        self.queue = Queue()

    def set_params(self, path):
        arrivals = False
        params = False
        self.rand_numbers = 0
        self.rnd_list = []

        for line in ConfigHandler.read_file(path):
            if line.startswith("rndnumbersPerSeed:"):
                self.rand_numbers = int(line.replace("rndnumbersPerSeed: ", ""))
            if line.startswith("arrivals:"):
                arrivals = True
            elif arrivals:
                if ":" in line:
                    self.arrival_time = float(line[line.index(":") + 2:])
                else:
                    arrivals = False
            if line.startswith("seed:"):
                self.seed = int(line.replace("seed: ", ""))
            if line.startswith("queues:"):
                params = True
            elif params:
                self.configure_queue(line)

    def configure_queue(self, line):
        try:
            value = float(line[line.index(":") + 2:])
            if "servers:" in line:
                self.queue.set_servers(int(value))
            if "capacity:" in line:
                self.queue.set_capacity(int(value))
            if "minArrival:" in line:
                self.queue.set_min_arrival(float(value))
            if "maxArrival:" in line:
                self.queue.set_max_arrival(float(value))
            if "minService:" in line:
                self.queue.set_min_service(float(value))
            if "maxService:" in line:
                self.queue.set_max_service(float(value))
        except ValueError:
            self.queue.set_name(line.replace(':', '').strip())

    def end_n_report(self):
        print("==========================================================")
        print("=----------------------RELATORIO-------------------------=")
        print("Estado  Tempo       Probabilidade")

        for i, state_time in enumerate(self.estados):
            print(f"{i:<6d}  {state_time:<11.4f}  {(state_time * 100) / self.timer:.2f}%")
        
        print("Numero de perdas:", self.losses)
        print("=======================================================")

    def get_min_chegada(self):
        return self.queue.min_arrival

    def get_max_chegada(self):
        return self.queue.max_arrival

    def get_min_saida(self):
        return self.queue.min_service

    def get_max_saida(self):
        return self.queue.max_service

    def get_servidores(self):
        return self.queue.servers

    def get_max_fila(self):
        return self.queue.capacity

    def get_rand_numbers(self):
        return self.rand_numbers

    def get_seed(self):
        return self.seed