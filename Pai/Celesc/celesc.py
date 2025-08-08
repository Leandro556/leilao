import requests

def buscar_fatura(uc, cpf):
    url = "https://agenciaweb.celesc.com.br/AgenciaWeb/autenticar/loginCliente.do"  # Substitua pela URL correta
    headers = {"Content-Type": "application/json"}  # Substitua pelos cabeçalhos corretos
    data = {
        "codigo_uc": uc,
        "cpf": cpf
    }

    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 200:
        return response.json()
    else:
        return None

uc = "56045929"
cpf = "02691603962"

fatura = buscar_fatura(uc, cpf)
if fatura is not None:
    print(fatura)
else:
    print("Não foi possível buscar a fatura.")
