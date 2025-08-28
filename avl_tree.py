from typing import Optional
from models import Record


class AVLNode:
    def __init__(self, record: Record):
        self.record = record
        self.left: Optional[AVLNode] = None
        self.right: Optional[AVLNode] = None
        self.height = 1


class AVLTree:
    def __init__(self):
        self.root: Optional[AVLNode] = None
        self.iterations = 0
        self.size_count = 0
    
    def insert(self, record: Record) -> int:
        self.iterations = 0
        self.root = self._insert_recursive(self.root, record)
        self.size_count += 1
        return self.iterations
    
    def _insert_recursive(self, node: Optional[AVLNode], record: Record) -> AVLNode:
        self.iterations += 1
        
        # Inserção normal BST
        if node is None:
            return AVLNode(record)
        
        if record.matricula < node.record.matricula:
            node.left = self._insert_recursive(node.left, record)
        elif record.matricula > node.record.matricula:
            node.right = self._insert_recursive(node.right, record)
        else:
            return node  # Duplicata não permitida
        
        # Atualiza altura
        node.height = 1 + max(self._get_height(node.left), 
                             self._get_height(node.right))
        
        # Obtém o fator de balanceamento
        balance = self._get_balance(node)
        
        # Casos de desbalanceamento
        # Caso 1 - Left Left
        if balance > 1 and record.matricula < node.left.record.matricula:
            return self._rotate_right(node)
        
        # Caso 2 - Right Right
        if balance < -1 and record.matricula > node.right.record.matricula:
            return self._rotate_left(node)
        
        # Caso 3 - Left Right
        if balance > 1 and record.matricula > node.left.record.matricula:
            node.left = self._rotate_left(node.left)
            return self._rotate_right(node)
        
        # Caso 4 - Right Left
        if balance < -1 and record.matricula < node.right.record.matricula:
            node.right = self._rotate_right(node.right)
            return self._rotate_left(node)
        
        return node
    
    def _rotate_left(self, z: AVLNode) -> AVLNode:
        self.iterations += 1
        y = z.right
        T2 = y.left
        
        # Realiza rotação
        y.left = z
        z.right = T2
        
        # Atualiza alturas
        z.height = 1 + max(self._get_height(z.left), 
                          self._get_height(z.right))
        y.height = 1 + max(self._get_height(y.left), 
                          self._get_height(y.right))
        
        return y
    
    def _rotate_right(self, z: AVLNode) -> AVLNode:
        self.iterations += 1
        y = z.left
        T3 = y.right
        
        # Realiza rotação
        y.right = z
        z.left = T3
        
        # Atualiza alturas
        z.height = 1 + max(self._get_height(z.left), 
                          self._get_height(z.right))
        y.height = 1 + max(self._get_height(y.left), 
                          self._get_height(y.right))
        
        return y
    
    def _get_height(self, node: Optional[AVLNode]) -> int:
        if node is None:
            return 0
        return node.height
    
    def _get_balance(self, node: Optional[AVLNode]) -> int:
        if node is None:
            return 0
        return self._get_height(node.left) - self._get_height(node.right)
    
    def search(self, matricula: int) -> tuple[Optional[Record], int]:
        self.iterations = 0
        return self._search_recursive(self.root, matricula), self.iterations
    
    def _search_recursive(self, node: Optional[AVLNode], matricula: int) -> Optional[Record]:
        if node is None:
            return None
        
        self.iterations += 1
        
        if matricula == node.record.matricula:
            return node.record
        elif matricula < node.record.matricula:
            return self._search_recursive(node.left, matricula)
        else:
            return self._search_recursive(node.right, matricula)
    
    def size(self) -> int:
        return self.size_count
    
    def height(self) -> int:
        return self._get_height(self.root)
    
    def clear(self):
        self.root = None
        self.iterations = 0
        self.size_count = 0