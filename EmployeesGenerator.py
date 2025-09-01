import random

# listas de nomes e sobrenomes (pode expandir)
first_names = ["Lian", "Alice", "Bruno", "Carla", "Diego", "Elisa", "Felipe", "Giovana", "Hugo", "Isabel"]
last_names  = ["Moratti", "Silva", "Costa", "Mendes", "Ferreira", "Oliveira", "Pereira", "Santos", "Rocha", "Lopes"]

def random_name():
    return f"{random.choice(first_names)} {random.choice(last_names)}"

def random_id():
    return random.randint(100000, 999999)  # ID com 6 dígitos

def random_cep():
    return f"{random.randint(10000, 99999)}-{random.randint(100, 999)}"  # formato 00000-000

def random_name():
    return f"{random.choice(first_names)} {random.choice(last_names)}"

def random_cadastro():
    return {
        "Nome": random_name(),
        "ID": random_id(),
        "CEP": random_cep()
    }

# for i in range(5):
#   print(random_cadastro())