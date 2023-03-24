import pandas as pd
from unidecode import unidecode

distancias = pd.read_csv('DNIT-Distancias.csv', delimiter=';', header=0)

#custo por km rodado de cada caminhão
custo_caminhoes = {'P': 4.87, 'M': 11.92, 'G': 27.44}

def menu():
  print("Menu:")
  print("1- Consultar trechos e modalidade")
  print("2- Cadastrar um transporte")
  print("3- Dados estatísticos")
  print("4- Finalizar programa")

opcao = 0
while opcao !=4:
  menu()
  opcao = int(input("Digite a opção desejada pelo número: "))

  if opcao == 1:

    de = str(input("Digite a cidade de origem: "))
    #retirando os acentos e convertendo todas as letras em maiúsculas 
    origem = unidecode(de).upper()
    if origem not in distancias:
      print(f"Infelizmente ainda não temos coleta em {de}.")
      continue

    para = str(input("Digite a cidade de destino: "))
    #retirando os acentos e convertendo todas as letras em maiúsculas 
    destino = unidecode(para).upper()
    if destino not in distancias:
      print(f"Infelizmente ainda não temos entrega em {para}.")
      continue
    
    print("Capacidade máxima das opções:\nP- 1 tonelada\nM- 4 toneladas\nG- 10 toneladas")
    tamanho = str(input("Digite o tamanho do caminhão (P, M ou G): ").upper())

    #selecionando o índice pelo nome da cidade, e distancia pelos índices linha X coluna 
    origem_posicao = distancias.columns.get_loc(origem)
    destino_posicao = distancias.columns.get_loc(destino)
    distancia = distancias.iloc[origem_posicao, destino_posicao]

    #selecionando no dicionário o custo pelo tamanho digitado do usuário * distancia 
    caminhao = custo_caminhoes[tamanho]
    custo_trecho = caminhao*distancia
  
    print(f"De {origem} para {destino}, utilizando um caminhão de porte {tamanho}, a distância é de {distancia} km, e o custo será de R$ {custo_trecho:.2f}.")

  elif opcao == 2:
    print("Cadastro de transporte")
    cidades = input("Digite quais cidades serão percorridas, separe-as com vírgula: ").split(",")
    itens = {}
    
    while True:
      item = input('Digite o nome do item a incluir na carga: ')
      peso = int(input('Digite o peso do item em kg (número inteiro): '))
      itens[item] = peso
    
      mais_itens = input('Incluir mais itens? (S/N): ')
      if mais_itens.lower() != 's':
        break
      
  elif opcao == 3:
    print("Dados estatísticos")
  elif opcao == 4:
    print("Finalizando o programa...")
    break
  else:
    print("Opção inválida! Digite um número entre 1 e 4")
