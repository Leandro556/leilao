
import streamlit as st
import requests

st.set_page_config(page_title="Leilões SC/RS/PR", layout="wide")

st.title("🚧 Editais de Leilão Vigentes - SC | RS | PR")

res = requests.get("http://localhost:8000/editais")
editais = res.json()

for edital in editais:
    with st.expander(f"{edital['municipio']} - {edital['estado']} ({edital['data']})"):
        st.write(edital['descricao'])
        st.markdown(f"[Acessar Edital]({edital['url']})")
