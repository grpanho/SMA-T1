from Queue import Queue
from ConfigHandler import *
import yaml

class Simulator:
    def __init__(self, timer):
        self.timer = timer
        self.queueList = {}
        self.losses = 0
        self.maxIterations = 0
        self.seed = 21

    def set_params(self, queuesYaml):
        with open(queuesYaml, 'r') as file:
            self.queueData = yaml.safe_load(file)
        
        self.configure_queues()

    def configure_queues(self):
        for queue in self.queueData['queues']:
            self.queueList[queue] = Queue()  # Cria uma nova fila com o nome especificado
            self.queueList[queue].set_name(queue)  # Define o nome da fila
            self.queueList[queue].set_servers(int(self.queueData['queues'][queue]['servers']))
            self.queueList[queue].set_capacity(int(self.queueData['queues'][queue]['capacity']))
            self.queueList[queue].start_states()  # Inicializa o estado da fila
#            self.queueList[queue].set_state(0, 0.0)  # Adiciona o tempo inicial ao estado da fila
            self.queueList[queue].set_min_arrival(float(self.queueData['queues'][queue]['minArrival']))
            self.queueList[queue].set_max_arrival(float(self.queueData['queues'][queue]['maxArrival']))
            self.queueList[queue].set_min_service(float(self.queueData['queues'][queue]['minService']))
            self.queueList[queue].set_max_service(float(self.queueData['queues'][queue]['maxService']))
            print(f"Queue {queue} configured")
            print(self.queueList[queue])
        self.maxIterations = int(self.queueData['maxIterations'])
    def end_n_report(self):
        print("==========================================================")
        print("=----------------------RELATORIO-------------------------=")
        for queueName, fila in self.queueList.items():
            queue = self.queueList[queueName]
            print(f"Fila: {queueName}")
            print("Estado  Tempo       Probabilidade")
            for state, state_time in enumerate(queue.get_states()):
                print(f"{state:<6d}  {state_time:<11.4f}  {(state_time * 100) / self.timer:.2f}%")
            print("Numero de perdas:", self.losses)
            print("=======================================================")

    def get_maxIterations(self):
        return self.maxIterations

    def get_seed(self):
        return self.seed