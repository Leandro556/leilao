import requests
from bs4 import BeautifulSoup
from datetime import datetime
import pandas as pd
import os
import unicodedata
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
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

def enviar_email(dados: list[dict], erros: list[dict], destinatario: str, remetente: str, senha: str):
    msg = MIMEMultipart()
    msg["From"] = remetente
    msg["To"] = destinatario
    msg["Subject"] = "📄 Editais de Leilões - Coleta Automática"

    html = "<h2>Editais Encontrados:</h2>"
    if dados:
        html += "<ul>"
        for item in dados:
            html += f"<li><a href='{item['link']}'>{item['titulo']}</a> — {item['site_origem']} ({item['data_coleta']})</li>"
        html += "</ul>"
    else:
        html += "<p>Nenhum edital encontrado.</p>"

    if erros:
        html += "<h3>⚠️ Erros encontrados:</h3><ul>"
        for erro in erros:
            html += f"<li><strong>{erro['site']}</strong>: {erro['erro']} ({erro['tipo']})</li>"
        html += "</ul>"

    msg.attach(MIMEText(html, "html"))

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as servidor:
            servidor.starttls()
            servidor.login(remetente, senha)
            servidor.send_message(msg)
            print("[✔️] E-mail enviado com sucesso.")
    except Exception as e:
        print(f"[❌] Erro ao enviar e-mail: {e}")

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

    # Defina o remetente e senha (preferencialmente use variáveis de ambiente em produção!)
    remetente = "leilaoscraper@gmail.com"
    senha = "kxac cdlz zkwg qxsi"
    destinatario = "lbpela@gmail.com, "

    enviar_email(todos_editais, erros, destinatario, remetente, senha)

if __name__ == "__main__":
    main()