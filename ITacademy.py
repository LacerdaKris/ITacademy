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
    #cria lista com as cidades digitadas, e passa pra outra removendo os espaços em branco no início/fim
    input_cidades = input("Digite quais cidades serão percorridas, separe-as com vírgula: ").split(",")
    cidades = [cidade.strip() for cidade in input_cidades]
    
    #dicionário p/ armazenar os pares de trecho entre cidades, e um acumulador do total
    distancias_cidades = {}
    km_total = 0
    
    #começa a iterar as cidades pela segunda da lista (indice 1)
    for i in range(1, len(cidades)):
      #retira acentos e deixa todos os caracteres em maiúsculo
      cidade_anterior = unidecode(cidades[i-1]).upper()
      cidade_atual = unidecode(cidades[i]).upper()
    
      origem_posicao = distancias.columns.get_loc(cidade_anterior)
      destino_posicao = distancias.columns.get_loc(cidade_atual)
      distancia = distancias.iloc[origem_posicao, destino_posicao]
      
      #cria chave e valor do par, armazena com a dstancia no dict e soma ao acumulador
      chave = cidade_anterior + " - " + cidade_atual
      valor = distancia
      distancias_cidades[chave] = valor
      km_total += valor
    
      #prepara valor da cidade anterior para próxima iteração
      cidade_anterior = cidade_atual

    #cria dicionário para armazenar os itens e seus respectivos pesos
    itens = {}
    
    while True:
      item = input('Digite o nome do item a incluir na carga: ')
      peso = int(input('Digite o peso do item em kg (número inteiro): '))
      itens[item] = peso
    
      mais_itens = input('Incluir mais itens? (S/N): ')
      if mais_itens.lower() != 's':
        break

    #paradas com retirada de itens durante o trajeto
    paradas = input("Haverão paradas para descarregamento no trajeto? (S/N): ")
    if paradas.lower() == 's':
      input_paradas = input("Em quais cidades haverá paradas com retirada de carga, separe-as com vírgula: ").split(",")
      paradas_cidades = [parada.strip() for parada in input_paradas]
      paradas_itens = []
      #pra cada cidade, perguntar e armazenar num array quais itens serão descarregados
      for cidade in paradas_cidades:
        input_itens_cidade = input(f"Quais itens serão retirados em {cidade}? Separe-os com vírgula: ").split(",")
        itens_cidade = [item.strip() for item in input_itens_cidade]
        #adicionar cada item ao array como um dict, sendo cidade a chave e itens o valor
        paradas_itens.append({cidade.upper(): [item.upper() for item in itens_cidade]})

      #organiza as paradas como um único dicionário, ao invés de uma lista
      paradas_itens_dict = {}
      for parada in paradas_itens:
        for cidade, item in parada.items():
          paradas_itens_dict[unidecode(cidade)] = item
    
    else:
      paradas_itens_dict = {}

      
  elif opcao == 3:
    print("Dados estatísticos")
  elif opcao == 4:
    print("Finalizando o programa...")
    break
  else:
    print("Opção inválida! Digite um número entre 1 e 4")
