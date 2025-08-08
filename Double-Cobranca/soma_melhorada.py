def solicitar_numeros():
    """
    Solicita números ao usuário até que ele pressione Enter sem digitar nada.
    Ignora o sinal negativo dos números digitados.
    """
    numeros = []
    while True:
        try:
            numero = input("Digite um número (ou pressione Enter para sair): ").replace(',', '.')
            if numero == "":  # Encerra ao pressionar Enter.
                break
            # Converte para float e pega o valor absoluto.
            numeros.append(abs(float(numero)))
        except ValueError:
            print("Entrada inválida. Por favor, digite um número ou pressione Enter para sair.")
    return numeros

def calcular_soma(numeros):
    """
    Calcula a soma de uma lista de números.
    """
    return sum(numeros)

def calcular_porcentagem(soma, porcentagem=0.03):
    """
    Calcula um valor com base em uma porcentagem dada.
    Por padrão, a porcentagem é de 5% (0.05).
    """
    return soma * porcentagem

def formatar_em_reais(valor):
    """
    Formata um número como valor monetário em reais.
    """
    return f'R$ {valor:,.2f}'.replace('.', '!').replace(',', '.').replace('!', ',')

def main():
    """
    Função principal que coordena a entrada de dados, cálculo e exibição de resultados.
    """
    numeros = solicitar_numeros()
    if numeros:  # Verifica se a lista contém números.
        soma = calcular_soma(numeros)
        print(f"A soma dos números digitados é: --------- {formatar_em_reais(soma)} ---------")
        porcentagem = calcular_porcentagem(soma)
        print(f"A multiplicação pela porcentagem é de: ------- {formatar_em_reais(porcentagem)} -------")
    else:
        print("Nenhum número foi digitado. Programa encerrado.")

if __name__ == "__main__":
    main()
