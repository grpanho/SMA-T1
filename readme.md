# Simulação e Métodos Analíticos - T1
## Execução

Instalar as dependências:
```bash
pip install -r requirements.txt
ou
pip install pyyaml
```
Executar:
```bash
python3 simulator.py <fila.yml>
python3 Simulator.py filas/FilaT1.yml
```

## Lista de Números
Para executar com uma lista fixa de números "aleatórios", altere `listMode` para `True` no arquivo FilaT1.yml.
Caso contrário, os números serão gerados pseudoaleatoriamente.