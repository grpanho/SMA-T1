from Queue import Queue
import yaml

class Simulator:
    def __init__(self):
        self.timer = 0
        self.queueList = {}
        self.losses = 0
        self.maxIterations = 0
        self.seed = 21

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