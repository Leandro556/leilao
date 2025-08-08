numeros = []
while True:
    try:
        numero = float(input("Digite um número: "))
        numeros.append(numero)
    except ValueError:
        break

soma = sum(numeros)

print(f"A soma dos números digitados é: --------- {soma} ---------")

porcentagem = soma * 0.03

print(f"A multiplicacao pela porcentagem é de: ------- {porcentagem} ------- ")
