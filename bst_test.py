import random
import time
import tracemalloc
import csv
import psutil
import os

# dados para gerar registros aleatorios
first_names = ["Luan", "Alice", "Bruno", "Carla", "Diego", "Elisa", "Felipe", "Giovana", "Hugo", "Isabel","Mateus","Daniel","Letícia","Rebeca","Elias","João", "Karen", "Lucas", "Maria", "Nicolas", "Olivia", "Pedro", "Quiteria", "Rafael", "Sofia", "Rodrigo","Solange",]
last_names = ["Silva", "Costa", "Mendes", "Ferreira", "Oliveira", "Pereira", "Santos", "Rocha", "Lopes","Aguiar","Loyola","Correa","Hipona","Aquino", 
              "Almeida", "Barbosa", "Cardoso", "Dias", "Esteves", "Fonseca", "Gomes", "Henrique", "Igor","Darc","Oviedo","Alcântara"]

sectors = ["Setor A", "Setor B", "Setor C", "Setor D", "Setor E"]
domains = ["@bol.com","@aol.com","@hotmail.com","@uol.com","@ig.com","@ibest.com"]
email = ["aux_", "sec_", "sel_", "dir_", "dev_"]

def random_name():
    return f"{random.choice(first_names)} {random.choice(last_names)}"

def random_id():
    return random.randint(100000000, 999999999)  # ID com 6 dígitos

def random_cep():
    return f"{random.randint(10000, 99999)}-{random.randint(100, 999)}"  # formato 00000-000

def random_name():
    return f"{random.choice(first_names)} {random.choice(last_names)}"

def random_sector():
    return f"{random.choice(sectors)}"

def random_age():
    return random.randint(18, 65)

def random_email():
    return f"{random.choice(email)}{random.randint(0, 2025)}{random.choice(domains)}"

# criar um registro completo
def gerar_registro():
    return {
        "Nome": random_name(),
        "Idade": random_age(),
        "ID": random_id(),
        "CEP": random_cep(),
        "Setor": random_sector(),
        "E-mail": random_email()
    }



# BST sem balanceamento - inserir node
def inserir_bst(arvore, registro):
    global iteracoes_insercao
    iteracoes_insercao += 1
    
    if arvore is None:
        return {"registro": registro, "esquerda": None, "direita": None}
    
    if registro["ID"] < arvore["registro"]["ID"]:
        arvore["esquerda"] = inserir_bst(arvore["esquerda"], registro)
    else:
        arvore["direita"] = inserir_bst(arvore["direita"], registro)
    
    return arvore

# BST sem balanceamento - buscar por ID
def buscar_bst(arvore, id_busca):
    global iteracoes_busca
    iteracoes_busca += 1
    
    if arvore is None:
        return None
    
    if id_busca == arvore["registro"]["ID"]:
        return arvore["registro"]
    elif id_busca < arvore["registro"]["ID"]:
        return buscar_bst(arvore["esquerda"], id_busca)
    else:
        return buscar_bst(arvore["direita"], id_busca)

# calcular altura da arvore
def calcular_altura(arvore):
    if arvore is None:
        return 0
    
    altura_esquerda = calcular_altura(arvore["esquerda"])
    altura_direita = calcular_altura(arvore["direita"])
    
    return 1 + max(altura_esquerda, altura_direita)

# BST com balanceamento simples - inserir com rotacao
def inserir_bst_balanceada(arvore, registro):
    global iteracoes_insercao_balanceada
    iteracoes_insercao_balanceada += 1
    
    if arvore is None:
        return {"registro": registro, "esquerda": None, "direita": None, "altura": 1}
    
    if registro["ID"] < arvore["registro"]["ID"]:
        arvore["esquerda"] = inserir_bst_balanceada(arvore["esquerda"], registro)
    else:
        arvore["direita"] = inserir_bst_balanceada(arvore["direita"], registro)
    
    # atualizar altura
    altura_esquerda = arvore["esquerda"]["altura"] if arvore["esquerda"] else 0
    altura_direita = arvore["direita"]["altura"] if arvore["direita"] else 0
    arvore["altura"] = 1 + max(altura_esquerda, altura_direita)
    
    # calcular balance factor
    balance = altura_esquerda - altura_direita
    
    # rotacao direita
    if balance > 1 and registro["ID"] < arvore["esquerda"]["registro"]["ID"]:
        return rotacao_direita(arvore)
    
    # rotacao esquerda
    if balance < -1 and registro["ID"] > arvore["direita"]["registro"]["ID"]:
        return rotacao_esquerda(arvore)
    
    # rotacao esquerda-direita
    if balance > 1 and registro["ID"] > arvore["esquerda"]["registro"]["ID"]:
        arvore["esquerda"] = rotacao_esquerda(arvore["esquerda"])
        return rotacao_direita(arvore)
    
    # rotacao direita-esquerda
    if balance < -1 and registro["ID"] < arvore["direita"]["registro"]["ID"]:
        arvore["direita"] = rotacao_direita(arvore["direita"])
        return rotacao_esquerda(arvore)
    
    return arvore

# rotacao para direita
def rotacao_direita(y):
    x = y["esquerda"]
    T2 = x["direita"]
    
    x["direita"] = y
    y["esquerda"] = T2
    
    # atualizar alturas
    altura_esquerda_y = y["esquerda"]["altura"] if y["esquerda"] else 0
    altura_direita_y = y["direita"]["altura"] if y["direita"] else 0
    y["altura"] = 1 + max(altura_esquerda_y, altura_direita_y)
    
    altura_esquerda_x = x["esquerda"]["altura"] if x["esquerda"] else 0
    altura_direita_x = x["direita"]["altura"] if x["direita"] else 0
    x["altura"] = 1 + max(altura_esquerda_x, altura_direita_x)
    
    return x

# rotacao para esquerda
def rotacao_esquerda(x):
    y = x["direita"]
    T2 = y["esquerda"]
    
    y["esquerda"] = x
    x["direita"] = T2
    
    # atualizar alturas
    altura_esquerda_x = x["esquerda"]["altura"] if x["esquerda"] else 0
    altura_direita_x = x["direita"]["altura"] if x["direita"] else 0
    x["altura"] = 1 + max(altura_esquerda_x, altura_direita_x)
    
    altura_esquerda_y = y["esquerda"]["altura"] if y["esquerda"] else 0
    altura_direita_y = y["direita"]["altura"] if y["direita"] else 0
    y["altura"] = 1 + max(altura_esquerda_y, altura_direita_y)
    
    return y

# buscar na BST balanceada
def buscar_bst_balanceada(arvore, id_busca):
    global iteracoes_busca_balanceada
    iteracoes_busca_balanceada += 1
    
    if arvore is None:
        return None
    
    if id_busca == arvore["registro"]["ID"]:
        return arvore["registro"]
    elif id_busca < arvore["registro"]["ID"]:
        return buscar_bst_balanceada(arvore["esquerda"], id_busca)
    else:
        return buscar_bst_balanceada(arvore["direita"], id_busca)

# main - executar os testes
volumes = [10000, 50000, 100000]
num_rodadas = 5

# arquivo csv para resultados
with open('/Users/rodrigoalmeidadeoliveira/Documents/Doutorado/Disciplinas/FundamentosAlgoritmos/DataStructuresAndAlgorithms/Tarefas/resultados_bst.csv', 'w', newline='') as csvfile:
    fieldnames = ['tipo_bst', 'volume', 'rodada', 'tempo_insercao', 'tempo_busca', 'memoria_pico', 'cpu_percent', 
                  'iteracoes_insercao', 'iteracoes_busca', 'altura_arvore']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    
    for volume in volumes:
        print(f"\nTestando volume: {volume}")
        
        for rodada in range(num_rodadas):
            print(f"Rodada {rodada + 1}")
            
            # gerar dados de teste
            dados_teste = []
            for i in range(volume):
                dados_teste.append(gerar_registro())
            
            # selecionar alguns IDs para busca
            ids_busca = []
            for i in range(min(1000, volume // 10)):  # buscar 1000 ou 10% dos dados
                ids_busca.append(dados_teste[random.randint(0, volume-1)]["ID"])
            
            # TESTE BST SEM BALANCEAMENTO
            print("  Testando BST sem balanceamento...")
            
            # variaveis globais para contar iteracoes
            iteracoes_insercao = 0
            iteracoes_busca = 0
            
            # monitorar memoria
            tracemalloc.start()
            processo = psutil.Process(os.getpid())
            cpu_inicial = processo.cpu_percent()
            
            # inserir dados
            arvore_normal = None
            tempo_inicio_insercao = time.time()
            
            for registro in dados_teste:
                arvore_normal = inserir_bst(arvore_normal, registro)
            
            tempo_fim_insercao = time.time()
            tempo_insercao = tempo_fim_insercao - tempo_inicio_insercao
            
            # buscar dados
            tempo_inicio_busca = time.time()
            
            for id_busca in ids_busca:
                resultado = buscar_bst(arvore_normal, id_busca)
            
            tempo_fim_busca = time.time()
            tempo_busca = tempo_fim_busca - tempo_inicio_busca
            
            # coletar metricas
            memoria_atual, memoria_pico = tracemalloc.get_traced_memory()
            tracemalloc.stop()
            cpu_final = processo.cpu_percent()
            cpu_percent = cpu_final - cpu_inicial
            altura = calcular_altura(arvore_normal)
            
            # salvar resultados
            writer.writerow({
                'tipo_bst': 'sem_balanceamento',
                'volume': volume,
                'rodada': rodada + 1,
                'tempo_insercao': tempo_insercao,
                'tempo_busca': tempo_busca,
                'memoria_pico': memoria_pico,
                'cpu_percent': cpu_percent,
                'iteracoes_insercao': iteracoes_insercao,
                'iteracoes_busca': iteracoes_busca,
                'altura_arvore': altura
            })
            
            # TESTE BST COM BALANCEAMENTO
            print("  Testando BST com balanceamento...")
            
            # resetar variaveis
            iteracoes_insercao_balanceada = 0
            iteracoes_busca_balanceada = 0
            
            # monitorar memoria
            tracemalloc.start()
            processo = psutil.Process(os.getpid())
            cpu_inicial = processo.cpu_percent()
            
            # inserir dados
            arvore_balanceada = None
            tempo_inicio_insercao = time.time()
            
            for registro in dados_teste:
                arvore_balanceada = inserir_bst_balanceada(arvore_balanceada, registro)
            
            tempo_fim_insercao = time.time()
            tempo_insercao = tempo_fim_insercao - tempo_inicio_insercao
            
            # buscar dados
            tempo_inicio_busca = time.time()
            
            for id_busca in ids_busca:
                resultado = buscar_bst_balanceada(arvore_balanceada, id_busca)
            
            tempo_fim_busca = time.time()
            tempo_busca = tempo_fim_busca - tempo_inicio_busca
            
            # coletar metricas
            memoria_atual, memoria_pico = tracemalloc.get_traced_memory()
            tracemalloc.stop()
            cpu_final = processo.cpu_percent()
            cpu_percent = cpu_final - cpu_inicial
            altura = arvore_balanceada["altura"] if arvore_balanceada else 0
            
            # salvar resultados
            writer.writerow({
                'tipo_bst': 'com_balanceamento',
                'volume': volume,
                'rodada': rodada + 1,
                'tempo_insercao': tempo_insercao,
                'tempo_busca': tempo_busca,
                'memoria_pico': memoria_pico,
                'cpu_percent': cpu_percent,
                'iteracoes_insercao': iteracoes_insercao_balanceada,
                'iteracoes_busca': iteracoes_busca_balanceada,
                'altura_arvore': altura
            })

print("\nTestes concluidos! Resultados salvos em resultados_bst.csv")