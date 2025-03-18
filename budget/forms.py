from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Transaction, Category
from django import forms

class ColoredSelect(forms.Select):
    def create_option(self, name, value, label, selected, index, subindex=None, attrs=None):

        option = super().create_option(name, value, label, selected, index, subindex=subindex, attrs=attrs)

        if value:
            try:
                value_int = int(value)
            except (ValueError, TypeError):
                value_int = None
            if value_int and hasattr(self, 'category_types'):
                category_type = self.category_types.get(value_int)
                if category_type == 'income':
                    option['attrs']['style'] = 'color: green;'
                elif category_type == 'expense':
                    option['attrs']['style'] = 'color: red;'
        return option




class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]


class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ["category", "amount", "date", "note"]
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Získáme dotaz, který je již nastaven u pole category
        qs = self.fields['category'].queryset
        # Vytvoříme slovník, kde klíčem je ID kategorie a hodnotou je její typ ('income' nebo 'expense')
        category_types = {category.id: category.type for category in qs}
        # Nastavíme náš vlastní widget
        self.fields['category'].widget = ColoredSelect()
        # Zkopírujeme choices, aby widget věděl, jaká má být data
        self.fields['category'].widget.choices = self.fields['category'].choices
        # Předáme widgetu slovník s typy kategorií
        self.fields['category'].widget.category_types = category_types
