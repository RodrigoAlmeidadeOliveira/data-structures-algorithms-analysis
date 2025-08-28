from typing import Optional
from models import Record


class BSTNode:
    def __init__(self, record: Record):
        self.record = record
        self.left: Optional[BSTNode] = None
        self.right: Optional[BSTNode] = None


class BinarySearchTree:
    def __init__(self):
        self.root: Optional[BSTNode] = None
        self.iterations = 0
        self.size_count = 0
    
    def insert(self, record: Record) -> int:
        self.iterations = 0
        if self.root is None:
            self.root = BSTNode(record)
            self.iterations = 1
        else:
            self._insert_recursive(self.root, record)
        self.size_count += 1
        return self.iterations
    
    def _insert_recursive(self, node: BSTNode, record: Record) -> BSTNode:
        self.iterations += 1
        
        if record.matricula < node.record.matricula:
            if node.left is None:
                node.left = BSTNode(record)
            else:
                self._insert_recursive(node.left, record)
        elif record.matricula > node.record.matricula:
            if node.right is None:
                node.right = BSTNode(record)
            else:
                self._insert_recursive(node.right, record)
        
        return node
    
    def search(self, matricula: int) -> tuple[Optional[Record], int]:
        self.iterations = 0
        return self._search_recursive(self.root, matricula), self.iterations
    
    def _search_recursive(self, node: Optional[BSTNode], matricula: int) -> Optional[Record]:
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
        return self._height_recursive(self.root)
    
    def _height_recursive(self, node: Optional[BSTNode]) -> int:
        if node is None:
            return 0
        return 1 + max(self._height_recursive(node.left), 
                      self._height_recursive(node.right))
    
    def clear(self):
        self.root = None
        self.iterations = 0
        self.size_count = 0