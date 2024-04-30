from Queue import Queue

class Simulator:
    def __init__(self):
        self.timer = 0
        self.losses = 0
        self.maxIterations = 0
        self.seed = 21

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

    def get_timer(self):
        return self.timer

    def set_timer(self, time):
        self.timer = time

    def add_timer(self, time):
        self.timer += time