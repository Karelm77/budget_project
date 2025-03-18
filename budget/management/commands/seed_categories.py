from django.core.management.base import BaseCommand
from budget.models import Category

class Command(BaseCommand):
    help = 'Seed default categories'

    def handle(self, *args, **kwargs):
        default_categories = [
            {'name': 'Bydlení', 'type': 'expense'},
            {'name': 'Telefon', 'type': 'expense'},
            {'name': 'Energie', 'type': 'expense'},
            {'name': 'Voda', 'type': 'expense'},
            {'name': 'Potraviny', 'type': 'expense'},
            {'name': 'Doprava', 'type': 'expense'},
            {'name': 'Zdravotnictví', 'type': 'expense'},
            {'name': 'Vzdělání', 'type': 'expense'},
            {'name': 'Oblečení', 'type': 'expense'},
            {'name': 'Zábava', 'type': 'expense'},
            # KATEGORIE PŘÍJMŮ:
            {'name': 'Mzda', 'type': 'income'},
            {'name': 'Dar', 'type': 'income'},
            {'name': 'Investice', 'type': 'income'},
            {'name': 'Prodej', 'type': 'income'},
            # Přidejte další kategorie podle potřeby.
        ]

        created_count = 0
        for data in default_categories:
            obj, created = Category.objects.get_or_create(name=data['name'], type=data['type'])
            if created:
                created_count += 1

        self.stdout.write(self.style.SUCCESS(f'Seeded {created_count} kategorií.'))

