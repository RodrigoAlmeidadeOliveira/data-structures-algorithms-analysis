import random

# listas de nomes e sobrenomes (pode expandir)
first_names = ["Lian", "Alice", "Bruno", "Carla", "Diego", "Elisa", "Felipe", "Giovana", "Hugo", "Isabel"]
last_names  = ["Moratti", "Silva", "Costa", "Mendes", "Ferreira", "Oliveira", "Pereira", "Santos", "Rocha", "Lopes"]
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


def random_cadastro():
    return {
        "Nome": random_name(),
        "Idade": random_age(),
        "ID": random_id(),
        "CEP": random_cep(),
        "Setor": random_sector(),
        "E-mail": random_email()
    }

# for i in range(5):
#   print(random_cadastro())
