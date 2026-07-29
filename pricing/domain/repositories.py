from contextlib import AbstractContextManager
from typing import Protocol

class TransactionManager(Protocol):
    def atomic(self) -> AbstractContextManager: ...
