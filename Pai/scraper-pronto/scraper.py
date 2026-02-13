import requests
from bs4 import BeautifulSoup
from datetime import datetime
import pandas as pd
import os
import unicodedata
from urllib.parse import urljoin
from urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter

LEILAO_SITES = [
    "https://www.serpaleiloes.com.br/?tipo=leilao",
    "https://www.portalzuk.com.br/leilao-de-imoveis/u/todos-imoveis/sc",
    "https://www.brasilsulleiloes.com.br/",
]

BENS_INTERESSE = [
    "imovel urbano", "imoveis urbanos",
    "imovel rural", "imoveis rurais",
    "trator", "tratores",
    "carregadeira", "escavadeira",
    "leilao", "leiloes"
]

def normalize(s: str) -> str:
    if not s:
        return ""
    s = unicodedata.normalize("NFKD", s)
    s = "".join(ch for ch in s if not unicodedata.combining(ch))
    return s.lower()

def build_session():
    session = requests.Session()
    retries = Retry(
        total=4,                # 1 tentativa + 4 retries = 5 no total
        backoff_factor=1,       # 1s, 2s, 4s, 8s...
        status_forcelist=[429, 500, 502, 503, 504],
        allowed_methods=["GET", "HEAD"]
    )
    adapter = HTTPAdapter(max_retries=retries, pool_connections=10, pool_maxsize=20)
    session.mount("http://", adapter)
    session.mount("https://", adapter)
    session.headers.update({
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                      "AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/124.0 Safari/537.36"
    })
    return session

def link_interessante(texto_norm: str) -> bool:
    # precisa conter algum bem de interesse e alguma forma de "leilao"
    return any(bem in texto_norm for bem in BENS_INTERESSE) and "leil" in texto_norm

def buscar_editais_em_site(session: requests.Session, url: str):
    editais = []
    try:
        resp = session.get(url, timeout=15)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, "html.parser")

        vistos = set()
        for a in soup.find_all("a", href=True):
            texto = a.get_text(strip=True)
            texto_norm = normalize(texto)
            if not texto_norm:
                continue

            href = a["href"].strip()
            full_url = urljoin(url, href)

            if link_interessante(texto_norm):
                key = (texto_norm, full_url)
                if key in vistos:
                    continue
                vistos.add(key)
                editais.append({
                    "titulo": texto,
                    "link": full_url,
                    "site_origem": url,
                    "data_coleta": datetime.now().strftime("%Y-%m-%d %H:%M")
                })
        return editais, None

    except requests.exceptions.RequestException as e:
        # Erros de rede/HTTP
        return [], {"site": url, "erro": str(e), "tipo": type(e).__name__}
    except Exception as e:
        return [], {"site": url, "erro": str(e), "tipo": type(e).__name__}

def salvar_csv(base_nome: str, dados: list[dict]):
    if not dados:
        return None
    pasta = "resultados_leiloes"
    os.makedirs(pasta, exist_ok=True)
    arquivo = os.path.join(pasta, f"{base_nome}_{datetime.now().strftime('%Y%m%d_%H%M')}.csv")
    pd.DataFrame(dados).to_csv(arquivo, index=False, encoding="utf-8-sig")
    return arquivo

def main():
    session = build_session()
    todos_editais = []
    erros = []

    for site in LEILAO_SITES:
        resultados, erro = buscar_editais_em_site(session, site)
        if resultados:
            todos_editais.extend(resultados)
        if erro:
            erros.append(erro)

    arq_ok = salvar_csv("editais", todos_editais)
    arq_err = salvar_csv("erros", erros)

    if arq_ok:
        print(f"[OK] Editais salvos em: {arq_ok}")
    else:
        print("[!] Nenhum edital coletado.")

    if arq_err:
        print(f"[INFO] Erros salvos em: {arq_err}")

if __name__ == "__main__":
    main()
