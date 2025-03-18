import json
from django import template

register = template.Library()

@register.filter
def tojson(value):
    """
    Převádí hodnotu na JSON řetězec.
    Použijete ve vaší šabloně např.: {{ monthly_totals|tojson|safe }}
    """
    return json.dumps(value)
