def solicitar_numeros():
    numeros = []
    while True:
        try:
            numero = input("Digite um número: ").replace('R$', '').replace(',', '.').strip()
            numero_float = float(numero)
            if numero_float >= 0:  # Ignora números negativos
                numeros.append(numero_float)
        except ValueError:
            if numero == "":
                break
            else:
                print("Entrada inválida. Por favor, digite um número ou pressione Enter para sair.")
    return numeros

def calcular_soma(numeros):
    return sum(numeros)

def calcular_porcentagem(soma, porcentagem = 0.03):
    return soma * porcentagem

def formatar_em_reais(valor):
    return f'R$ {valor:,.2f}'.replace('.', '!').replace(',', '.').replace('!', ',')

def main():
    numeros = solicitar_numeros()
    soma = calcular_soma(numeros)
    print(f"A soma dos números digitados é: --------- {formatar_em_reais(soma)} ---------")
    porcentagem = calcular_porcentagem(soma)
    print(f"A multiplicacao pela porcentagem é de: ------- {formatar_em_reais(porcentagem)} ------- ")

if __name__ == "__main__":
    main()
