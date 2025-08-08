
from app.database.models import save_edital

def scrape_pr():
    edital = {
        'estado': 'PR',
        'municipio': 'Curitiba',
        'descricao': 'Leilão de tratores de pneu',
        'data': '2025-08-20',
        'url': 'https://www.prefeitura.pr.gov.br/leilao3.pdf',
    }
    save_edital(edital)
