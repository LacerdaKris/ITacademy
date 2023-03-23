import pandas as pd
from unidecode import unidecode

distancias = pd.read_csv('DNIT-Distancias.csv', index_col=0, delimiter=';')
#custo por km de cada caminhão
custo_caminhoes = {'P': 4.87, 'M': 11.92, 'G': 27.44}

def menu():
  print("Menu:")
  print("1- Consultar trechos e modalidade")
  print("2- Cadastrar um transporte")
  print("3- Dados estatísticos")
  print("4- Finalizar programa")

opcao = 0
while opcao != 4:
  menu()
  opcao = int(input("Digite a opção desejada pelo número: "))

  if opcao == 1:
    de = str(input("Digite a cidade de origem: "))
    origem = unidecode(de).upper()
    if origem not in distancias:
      print(f"Infelizmente ainda não temos coleta em {de}.")
      menu()

    para = str(input("Digite a cidade de destino: "))
    destino = unidecode(para).upper()
    if destino not in distancias:
      print(f"Infelizmente ainda não temos entrega em {para}.")
      menu()
    
    print("Capacidade máxima das opções:\nP- 1 tonelada\nM- 4 toneladas\nG- 10 toneladas")
    tamanho = str(input("Digite o tamanho do caminhão (P, M ou G): ").upper())
    origem_posicao = distancias.index[origem]
    destino_posicao = distancias.iloc[destino]
    distancia = distancias.iloc[origem_posicao, destino_posicao]
    caminhao = custo_caminhoes[tamanho]
  
    print(tamanho, origem_posicao, destino_posicao, caminhao)

  elif opcao == 2:
    print("Cadastro de transporte")
  elif opcao == 3:
    print("Dados estatísticos")
  elif opcao == 4:
    print("Finalizando o programa...")
    break
  else:
    print("Opção inválida! Digite um número entre 1 e 4")


