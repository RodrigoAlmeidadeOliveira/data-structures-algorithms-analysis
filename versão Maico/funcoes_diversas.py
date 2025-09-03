import random
import time
import tracemalloc
import csv
import psutil
import os
import matplotlib.pyplot as plt

first_names = ["Luan", "Alice", "Bruno", "Carla", "Diego", "Elisa", "Felipe", "Giovana", "Hugo", "Isabel","Mateus","Daniel","Letícia","Rebeca","Elias","João", "Karen", "Lucas", "Maria", "Nicolas", "Olivia", "Pedro", "Quiteria", "Rafael", "Sofia", "Rodrigo","Solange",]
last_names = ["Silva", "Costa", "Mendes", "Ferreira", "Oliveira", "Pereira", "Santos", "Rocha", "Lopes","Aguiar","Loyola","Correa","Hipona","Aquino",
              "Almeida", "Barbosa", "Cardoso", "Dias", "Esteves", "Fonseca", "Gomes", "Henrique", "Igor","Darc","Oviedo","Alcântara"]

def gerar_matricula():
    return random.randint(100000000, 999999999)

def gerar_nome():
    return f"{random.choice(first_names)} {random.choice(last_names)}"

def gerar_salario():
    return random.randint(1000, 20000)

def gerar_codigo_setor():
    return random.randint(1, 50)

def gerar_registro():
    return {
        "matricula": str(gerar_matricula()),
        "nome": gerar_nome(),
        "salario": gerar_salario(),
        "codigo_setor": gerar_codigo_setor()
    }


class Node:
    #  <-[data]->
    def __init__(self,data):
        self.data = data
        self.left = None
        self.right = None
        self.next = None
        self.height = 1

class StaticLinkedList:
    def __init__(self, size):
        self.size = size
        self.count = 0
        self.head = None

    def push(self, node):
        if self.count >= self.size:
            raise IndexError("Lista está cheia")
        if not isinstance(node, Node):
            raise TypeError("O objeto inserido deve ser do tipo Node")
        node.next = self.head
        self.head = node
        self.count += 1

    def search(self, matricula):
        current = self.head
        index = 0
        while current:
            if isinstance(current.data, dict) and str(current.data.get('matricula')) == str(matricula):
                return index, current
            current = current.next
            index += 1
        return None, None

    def remove(self, matricula):
        prev = None
        current = self.head
        while current:
            if isinstance(current.data, dict) and str(current.data.get('matricula')) == str(matricula):
                if prev:
                    prev.next = current.next
                else:
                    self.head = current.next
                self.count -= 1
                current.next = None
                return current
            prev = current
            current = current.next
        return None

    def display(self):
        current = self.head
        index = 0
        while current:
            print(f"Index {index}: {current.data}")
            current = current.next
            index += 1


class HashTable:
    def __init__(self, size):
        self.size = size
        self.table = [[] for _ in range(size)]
        self.colisoes = 0

    def hash_function1(self, key):
        """Função de hash simples: soma dos valores ASCII dos caracteres."""
        return sum(ord(char) for char in key) % self.size

    def hash_function2(self, key):
        """Função de hash baseada em polinômio."""
        soma = 0
        p_pow = 1
        p = 31  # Número primo para hash polinomial
        for char in key:
            soma = (soma + ord(char) * p_pow) % self.size
            p_pow = (p_pow * p) % self.size
        return soma

    def hash_function3(self, key):
        """Função de hash que soma o quadrado dos valores ASCII dos caracteres."""
        soma = 0
        for c in key:
            soma += pow(ord(c), 2)
        return (soma - ord(key[0])) % self.size

    def insert(self, node, hash_fn_id=1):
        key = str(node.data["matricula"])
        if hash_fn_id == 1:
            index = self.hash_function1(key)
        elif hash_fn_id == 2:
            index = self.hash_function2(key)
        elif hash_fn_id == 3:
            index = self.hash_function3(key)
        else:
            index = self.hash_function1(key)

        if self.table[index]:
            self.colisoes += 1
        self.table[index].append(node)

    def search(self, key, hash_fn_id=1):
        key_str = str(key)
        if hash_fn_id == 1:
            index = self.hash_function1(key_str)
        elif hash_fn_id == 2:
            index = self.hash_function2(key_str)
        elif hash_fn_id == 3:
            index = self.hash_function3(key_str)
        else:
            index = self.hash_function1(key_str)

        for node in self.table[index]:
            if str(node.data.get('matricula')) == key_str:
                return node
        return None

    def display(self):
        for i, bucket in enumerate(self.table):
            print(f"{i}: ", end="")
            for node in bucket:
                print(node.data, end=" | ")
            print()

def inicialize_hash_table(size=0):
    if size <= 0: return None

    hash_table = HashTable(size)
    for i in range(size):
        hash_table.insert(Node(gerar_registro()))
    return hash_table


# --- Classe Árvore Binária Sem Balanceamento---
class BinaryTree:
    def __init__(self, root_node=None):
        self.root = root_node

    def push(self, node):
        def insert(current, node):
            if node.data['matricula'] < current.data['matricula']:
                if current.left is None:
                    current.left = node
                else:
                    insert(current.left, node)
            else:
                if current.right is None:
                    current.right = node
                else:
                    insert(current.right, node)

        if self.root is None:
            self.root = node
        else:
            insert(self.root, node)

    def search(self, matricula):
        def find(current, matricula):
            if current is None:
                return None
            if str(current.data['matricula']) == str(matricula):
                return current
            if str(matricula) < str(current.data['matricula']):
                return find(current.left, matricula)
            else:
                return find(current.right, matricula)
        return find(self.root, matricula)

    def altura(self, node=None):
        if node is None:
            node = self.root
        if node is None:
            return 0
        left_height = self.altura(node.left)
        right_height = self.altura(node.right)
        return max(left_height, right_height) + 1

    def walk_pre_order(self, node=None):
        if node is None:
            node = self.root
        if node is None:
            return
        print(node.data)
        if node.left:
            self.walk_pre_order(node.left)
        if node.right:
            self.walk_pre_order(node.right)

    def walk_in_order(self, node=None):
        if node is None:
            node = self.root
        if node is None:
            return
        if node.left:
            self.walk_in_order(node.left)
        print(node.data)
        if node.right:
            self.walk_in_order(node.right)

    def walk_post_order(self, node=None):
        if node is None:
            node = self.root
        if node is None:
            return
        if node.left:
            self.walk_post_order(node.left)
        if node.right:
            self.walk_post_order(node.right)
        print(node.data)

#--classe AVL Tree--

class AVLTree:
    def __init__(self, node=None):
        self.root = node

    def push(self, node):
        self.root = self._insert(self.root, node)

    def _insert(self, current, new_node):
        if current is None:
            return new_node

        if new_node.data['matricula'] < current.data['matricula']:
            current.left = self._insert(current.left, new_node)
        else:
            current.right = self._insert(current.right, new_node)

        current.height = 1 + max(self._get_height(current.left), self._get_height(current.right))
        balance = self._get_balance(current)

        if balance > 1 and new_node.data['matricula'] < current.left.data['matricula']:
            return self._right_rotate(current)
        if balance < -1 and new_node.data['matricula'] > current.right.data['matricula']:
            return self._left_rotate(current)
        if balance > 1 and new_node.data['matricula'] > current.left.data['matricula']:
            current.left = self._left_rotate(current.left)
            return self._right_rotate(current)
        if balance < -1 and new_node.data['matricula'] < current.right.data['matricula']:
            current.right = self._right_rotate(current.right)
            return self._left_rotate(current)

        return current

    def _get_height(self, node):
        if not node:
            return 0
        return node.height

    def _get_balance(self, node):
        if not node:
            return 0
        return self._get_height(node.left) - self._get_height(node.right)

    def _left_rotate(self, z):
        y = z.right
        T2 = y.left

        y.left = z
        z.right = T2

        z.height = 1 + max(self._get_height(z.left), self._get_height(z.right))
        y.height = 1 + max(self._get_height(y.left), self._get_height(y.right))

        return y

    def _right_rotate(self, z):
        y = z.left
        T3 = y.right

        y.right = z
        z.left = T3

        z.height = 1 + max(self._get_height(z.left), self._get_height(z.right))
        y.height = 1 + max(self._get_height(y.left), self._get_height(y.right))

        return y

    def search(self, matricula):
        def find(current, matricula):
            if current is None:
                return None
            if str(current.data['matricula']) == str(matricula):
                return current
            if str(matricula) < str(current.data['matricula']):
                return find(current.left, matricula)
            else:
                return find(current.right, matricula)
        return find(self.root, matricula)

    # ====== Percursos ======
    def walk_preorder(self, node=None):
        if node is None:
            node = self.root
        if node:
            print(node.data)
            self.walk_preorder(node.left)
            self.walk_preorder(node.right)

    def walk_inorder(self, node=None):
        if node is None:
            node = self.root
        if node:
            self.walk_inorder(node.left)
            print(node.data)
            self.walk_inorder(node.right)

    def walk_postorder(self, node=None):
        if node is None:
            node = self.root
        if node:
            self.walk_postorder(node.left)
            self.walk_postorder(node.right)
            print(node.data)


# --- Funções de Análise de Desempenho ---
def memoria_usada():
    """Imprime o uso de memória do processo atual."""
    process = psutil.Process()
    mem_info = process.memory_info()
    print(f"\nMemória em uso: {mem_info.rss / (1024 * 1024):.2f} MB")
    print(f"Memória privada: {mem_info.vms / (1024 * 1024):.2f} MB")


def tempo_cpu():
    """Imprime o tempo de CPU utilizado pelo processo atual."""
    cpu_time = psutil.Process().cpu_times()
    total_seconds = cpu_time.user + cpu_time.system
    print(f"Tempo de CPU usado: {total_seconds:.2f} segundos")


def capturar_metricas(operacao_a_medir):
    """Captura e retorna métricas de tempo, CPU e memória para uma dada operação."""
    start_time = time.time()
    tracemalloc.start()
    
    operacao_a_medir()
    
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    end_time = time.time()
    
    process = psutil.Process(os.getpid())
    cpu_times = process.cpu_times()
    
    metrics = {
        "tempo_execucao": end_time - start_time,
        "memoria_atual_kb": current / 1024,
        "memoria_pico_kb": peak / 1024,
        "tempo_cpu_user": cpu_times.user,
        "tempo_cpu_system": cpu_times.system
    }
    return metrics

def salvar_metricas(filename, data):
    """Salva as métricas em um arquivo CSV."""
    with open(filename, 'a', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=data.keys())
        if f.tell() == 0:  # Escreve o cabeçalho apenas se o arquivo estiver vazio
            writer.writeheader()
        writer.writerow(data)

def gerar_graficos(titulo, x_label, y_label, series):
    """Gera um gráfico com base nos dados fornecidos."""
    plt.figure(figsize=(10, 6))
    for serie in series:
        plt.plot(serie['x'], serie['y'], marker='o', label=serie['label'])
    plt.title(titulo)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.legend()
    plt.grid(True)
    plt.savefig(f"{titulo.replace(' ', '_').lower()}.png")
    plt.show()