
from app.database.models import save_edital

def scrape_rs():
    edital = {
        'estado': 'RS',
        'municipio': 'Porto Alegre',
        'descricao': 'Leilão de terras rurais e carregadeiras',
        'data': '2025-08-15',
        'url': 'https://www.prefeitura.rs.gov.br/leilao2.pdf',
    }
    save_edital(edital)
