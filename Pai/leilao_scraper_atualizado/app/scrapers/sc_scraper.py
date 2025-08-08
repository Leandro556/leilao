
from app.database.models import save_edital

def scrape_sc():
    edital = {
        'estado': 'SC',
        'municipio': 'Florianópolis',
        'descricao': 'Leilão de terrenos urbanos e tratores',
        'data': '2025-08-10',
        'url': 'https://www.detran.sc.gov.br/download/09-renajud-cel-2025-edital-de-leilao/',
    }
    save_edital(edital)
