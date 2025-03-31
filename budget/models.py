from django.db import models
from django.contrib.auth.models import User




class Note(models.Model):
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.content[:50]



class Category(models.Model):
    TYPE_CHOICES = (
        ('expense', 'Výdaj'),
        ('income', 'Příjem'),
    )
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=10, choices=TYPE_CHOICES)

    def __str__(self):
        return self.name

class Transaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    amount = models.DecimalField(decimal_places=2, max_digits=10)
    date = models.DateField()  # datum transakce (uživatel může vybrat datum)
    note = models.TextField(blank=True, null=True)

    def __str__(self):
        category_name = self.category.name if self.category else "bez kategorie"
        return f"{self.user.username} - {category_name} - {self.amount}"

