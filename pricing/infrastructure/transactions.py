from django.db import transaction

class DjangoTransactionManager:
    def atomic(self):
        return transaction.atomic()
