from django.db import models

class Transacao(models.Model):
    # Dados da transação
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    location = models.CharField(max_length=255)
    merchant = models.CharField(max_length=255)
    card_type = models.CharField(max_length=50)
    transaction_date = models.DateTimeField(auto_now_add=True)
    
    # Resultado do Machine Learning
    is_fraud = models.BooleanField()
    probability = models.FloatField()

    def __str__(self):
        status = 'Fraud' if self.is_fraud else 'Safe'
        return f"Sale {self.id} - ${self.amount} ({status})"