from django.template import Library
from utils import utils


register = Library()


@register.filter
def formata_preco(val):
    return utils.formata_preco(val)
