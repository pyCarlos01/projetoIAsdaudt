import csv
import io
from .models import *

def csv_to_list_in_memory(filename: str) -> list:
    '''
    Lê um csv InMemoryUploadedFile e retorna um OrderedDict.
    '''
    file = filename.read().decode('utf-8')
    reader = csv.DictReader(io.StringIO(file))
    # Gerando uma list comprehension
    data = [line for line in reader]
    return data


def save_data(data):
    '''
    Salva os dados no banco.
    '''
    aux = []
    for item in data:
        title = item.get('title')
        price = item.get('price')
        obj = Remessa(
            title=title,
            price=price,
        )
        aux.append(obj)

    Remessa.objects.bulk_create(aux)