from typing import Optional, List
from models import Record


class LinearArray:
    def __init__(self):
        self.data: List[Record] = []
        self.iterations = 0
    
    def insert(self, record: Record) -> int:
        self.iterations = 1  # Uma operação de inserção
        self.data.append(record)
        return self.iterations
    
    def search(self, matricula: int) -> tuple[Optional[Record], int]:
        self.iterations = 0
        for i, record in enumerate(self.data):
            self.iterations += 1
            if record.matricula == matricula:
                return record, self.iterations
        return None, self.iterations
    
    def size(self) -> int:
        return len(self.data)
    
    def clear(self):
        self.data.clear()
        self.iterations = 0