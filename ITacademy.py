import pandas as pd
from unidecode import unidecode

distancias = pd.read_csv('DNIT-Distancias.csv', delimiter=';', header=0)

#capacidade máxima de cada caminhão em kg
capacidade_caminhoes = {'P': 1000, 'M': 4000, 'G': 10000}
#custo por km rodado de cada caminhão
custo_caminhoes = {'P': 4.87, 'M': 11.92, 'G': 27.44}

#lista para armazenar os transportes cadastrados na opção 2 do menu
transportes_cadastrados = []

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
    cidades_como_no_input = [cidade.strip() for cidade in input_cidades]
    cidades = [unidecode(cidade).upper() for cidade in cidades_como_no_input]
    
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
    peso_total_carga = 0
    
    while True:
      item = unidecode(input('Digite o nome do item a incluir na carga: ')).upper()
      peso = int(input('Digite o peso do item em kg (número inteiro): '))
      itens[item] = peso
      peso_total_carga += peso
    
      mais_itens = input('Incluir mais itens? (S/N): ')
      if mais_itens.lower() != 's':
        break

    #paradas com retirada de itens durante o trajeto
    paradas = input("Haverão paradas para descarregamento no trajeto? (S/N): ")
    if paradas.lower() == 's':
      input_paradas = input("Em quais cidades haverá paradas com retirada de carga, separe-as com vírgula: ").split(",")
      paradas_cidades_como_no_input = [parada.strip() for parada in input_paradas]
      paradas_cidades = [unidecode(parada).upper() for parada in paradas_cidades_como_no_input]

      paradas_itens = []
      #pra cada cidade, perguntar e armazenar num array quais itens serão descarregados
      for cidade in paradas_cidades:
        input_itens_cidade = input(f"Quais itens serão retirados em {cidade}? Separe-os com vírgula: ").split(",")
        itens_cidade_como_no_input = [item.strip() for item in input_itens_cidade]
        itens_cidade = [unidecode(item).upper() for item in itens_cidade_como_no_input]
        #adicionar cada item ao array como um dict, sendo cidade a chave e itens o valor
        paradas_itens.append({cidade.upper(): [item.upper() for item in itens_cidade]})

      #organiza as paradas como um único dicionário, ao invés de uma lista
      paradas_itens_dict = {}
      for parada in paradas_itens:
        for cidade, item in parada.items():
          paradas_itens_dict[unidecode(cidade)] = item
    
    else:
      paradas_itens_dict = {}
    
        #organiza num dicionário os itens de cada trecho
    itens_por_trecho = {}
    for trecho in distancias_cidades:
      itens_por_trecho[trecho] = []
    itens_ordenados_por_peso = dict(sorted(itens.items(), key=lambda x: x[1], reverse=True))
    #começa primeiro trecho com todos os itens, e os remove conforme as paradas
    itens_por_trecho[list(itens_por_trecho.keys())[0]] = list(itens_ordenados_por_peso.keys())
    
    #se houverem paradas, retira os itens a cada trecho
    if paradas_itens_dict:
      for i in range(len(cidades) - 1):
        trecho = cidades[i] + ' - ' + cidades[i+1]
        itens_trecho = []
        if trecho in itens_por_trecho:
          itens_trecho = itens_por_trecho[trecho]
        for item, peso in itens.items():
          if item not in paradas_itens_dict.get(cidades[i], []) and item not in itens_trecho:
            itens_trecho.append(item)
        itens_por_trecho[trecho] = itens_trecho
    
    else:
      for chave in itens_por_trecho:
        itens_por_trecho[chave] = list(itens_ordenados_por_peso.keys())
    
    #copia o dicionário itens por trecho, porém com os respectivos pesos em cada item
    itens_por_trecho_com_peso = {}
    
    for trecho, itens_trecho in itens_por_trecho.items():
      peso_itens_trecho = {}
      for item in itens_trecho:
        peso_itens_trecho[item] = itens[item]
      itens_por_trecho_com_peso[trecho] = peso_itens_trecho
    
    #função para distribuir os itens da melhor forma entre caminhões
    def distribuir_itens_caminhoes(capacidade_caminhoes, itens):
    
      #identifica quantidade e modelo do(s) caminhão(ões) necessário(s) para o transporte
      caminhoes_necessarios = {'P': 0, 'M': 0, 'G': 0}
      capacidade_atual_caminhoes = {'P': 1000, 'M': 4000, 'G': 10000}
      itens_atual_caminhoes = {'P': [], 'M': [], 'G': []}
    
      itens_na_funcao = itens.copy()
      #começa com o peso total da carga, e depois vai reduzindo conforme alocação em caminhoes
      peso_atual_carga = sum(itens.values())
    
      #verificar se é possível alocar todos os itens em um único caminhão, se sim, pular loop while
      maior_capacidade = [1000, 4000, 10000]
      for capacidade_maxima in maior_capacidade:
        if peso_atual_carga <= capacidade_maxima:
          if capacidade_maxima == 1000:
            caminhoes_necessarios['P'] += 1
            capacidade_atual_caminhoes['P'] = capacidade_caminhoes['P'] - peso_atual_carga
            itens_atual_caminhoes['P'] = list(itens.keys())
          elif capacidade_maxima == 4000:
            caminhoes_necessarios['M'] += 1
            capacidade_atual_caminhoes['M'] = capacidade_caminhoes['M'] - peso_atual_carga
            itens_atual_caminhoes['M'] = list(itens.keys())
          elif capacidade_maxima == 10000:
            caminhoes_necessarios['G'] += 1
            capacidade_atual_caminhoes['G'] = capacidade_caminhoes['G'] - peso_atual_carga
            itens_atual_caminhoes['G'] = list(itens.keys())
          peso_atual_carga = 0
          break
    
      while peso_atual_carga > 0:
        #itera nos itens da carga do maior ao menor peso
        for item, peso in itens.items():
          #tenta colocar o item no maior caminhão que ainda tem capacidade
          for modelo in ['G', 'M', 'P']:
            capacidade = capacidade_atual_caminhoes[modelo]
            if peso <= capacidade:
    
              #adiciona o item no caminhão, e reduz pedo do item da capacidade do caminhão
              capacidade_atual_caminhoes[modelo] -= peso
              itens_atual_caminhoes[modelo].append(item)
    
              if capacidade_atual_caminhoes[modelo] == 0:
                caminhoes_necessarios[modelo] += 1
                capacidade_atual_caminhoes[modelo] = capacidade_caminhoes[modelo]
                itens_atual_caminhoes[modelo] = []
    
              #calcula a capacidade restante em todos os caminhões após a inclusão do item
              capacidades_restantes = {k: v-peso if k!=modelo else v for k,v in capacidade_atual_caminhoes.items()}
    
              #escolhe o caminhão que deixaria a menor capacidade restante, descartando os com capacidade negativa
              modelo_menor_restante = min([modelo for modelo in capacidades_restantes if capacidades_restantes[modelo] >= 0], key=lambda modelo: abs(capacidades_restantes[modelo]))
    
              capacidade_menor_restante = capacidades_restantes[modelo_menor_restante]
              #se a capacidade restante e custo de outro caminhão for menor que o do item colocado, transferir
              #alterar item de caminhão (remove o item do caminhão atual e adiciona no outro)
              custo_caminhoes = {'P': 4.87, 'M': 11.92, 'G': 27.44}
    
              if capacidade_menor_restante < capacidade_atual_caminhoes[modelo]:
                combinacao1_necessarios = {'P': 0, 'M': 0, 'G': 0}
    
                for tamanho in combinacao1_necessarios.keys():
                  if itens_atual_caminhoes[tamanho]:
                    combinacao1_necessarios[tamanho] = caminhoes_necessarios[tamanho]+1
                  else:
                    combinacao1_necessarios[tamanho] = caminhoes_necessarios[tamanho]
                custo_caminhoes_necessarios_atual = sum([custo_caminhoes[tamanho]*combinacao1_necessarios[tamanho] for tamanho in combinacao1_necessarios])
                #simula alterações e se ñ ficar mais barato, desfaz
                itens_atual_caminhoes[modelo_menor_restante].append(item)
                itens_atual_caminhoes[modelo].remove(item)
    
                #forma combinação com as alterações p/ calcular
                combinacao2_necessarios = {'P': 0, 'M': 0, 'G': 0}
    
                for tamanho in combinacao2_necessarios.keys():
                  if itens_atual_caminhoes[tamanho]:
                    combinacao2_necessarios[tamanho] = caminhoes_necessarios[tamanho]+1
                  else:
                    combinacao2_necessarios[tamanho] = caminhoes_necessarios[tamanho]
    
                custo_caminhoes_necessarios_se_item_alterado = sum([custo_caminhoes[modelo_menor_restante]*combinacao2_necessarios[modelo_menor_restante] for modelo_menor_restante in combinacao2_necessarios])
              
                if custo_caminhoes_necessarios_atual > custo_caminhoes_necessarios_se_item_alterado:
                  capacidade_atual_caminhoes[modelo_menor_restante] -= peso
                  capacidade_atual_caminhoes[modelo] += peso    
                  caminhoes_necessarios[modelo_menor_restante] += 1
                  
                else:
                  itens_atual_caminhoes[modelo_menor_restante].remove(item)
                  itens_atual_caminhoes[modelo].append(item)
                  caminhoes_necessarios[modelo] += 1
              
              else:
                if itens_atual_caminhoes[modelo]:
                  caminhoes_necessarios[modelo] += 1
      
              break
    
          if itens_na_funcao:
            #se a capacidade atual de algum caminhão ficar menor que o item restante mais leve, limpá-lo
            item_mais_leve = min(itens_na_funcao.values())
            for tamanho_modelo, capacidade_atual_do_modelo in capacidade_atual_caminhoes.items():
              if capacidade_atual_do_modelo < item_mais_leve > max(capacidade_atual_caminhoes.values()):
                # Limpa a capacidade do caminhão
                capacidade_atual_caminhoes[tamanho_modelo] = capacidade_caminhoes[tamanho_modelo]
                itens_atual_caminhoes[tamanho_modelo] = []
                caminhoes_necessarios[tamanho_modelo] += 1
    
          itens_na_funcao.pop(item)
          if not itens_na_funcao:
            peso_atual_carga = 0
    
      return caminhoes_necessarios
    
    
    #chama função de distribuição e armazena quais caminhões serão usados por trecho
    caminhoes_necessarios_por_trecho = {}
    
    for trecho, itens_trecho in itens_por_trecho_com_peso.items():
      resultado_funcao = distribuir_itens_caminhoes(capacidade_caminhoes, itens_trecho)
      caminhoes_necessarios_por_trecho[trecho] = resultado_funcao
    
    #calcula o custo por trecho e armazena
    custo_por_trecho = {}
    
    for trecho, caminhoes in caminhoes_necessarios_por_trecho.items():
        valor_total_por_km = 0
        for caminhao, quantidade in caminhoes.items():
            valor_total_por_km += quantidade * custo_caminhoes[caminhao]
        valor_total_trecho = valor_total_por_km * distancias_cidades[trecho]
        custo_por_trecho[trecho] = valor_total_trecho
    
    custo_total = sum(custo_por_trecho.values())
    
    #imprime resultado
    print(f'Saindo de {cidades[0]} até {cidades[-1]}, a distância total a ser percorrida na rota é de {km_total} km.')
    if paradas_itens_dict:
      paradas_cidades = [c for c in paradas_itens_dict.keys()] 
      paradas_cidades_string = ', '.join(str(cidade) for cidade in paradas_cidades)
      print(f' - considerando paradas com itens a descarregar em {paradas_cidades_string}.')
    print(f'Para transportar os itens {list(itens.keys())},\n de forma a resultar no menor custo por km rodado, serão necessários:')
    #imprime quantidade de caminhões necessários para transportar a carga
    for trecho, caminhoes in caminhoes_necessarios_por_trecho.items():
      print(f'No trecho {trecho}')
      for caminhao, qtd in caminhoes.items():
        if qtd > 0:
          print(f'{qtd} caminhão(ões) de porte {caminhao}')
    print(f'O valor total do frete é R$ {custo_total:.2f}, sendo R$ {custo_total/len(custo_por_trecho):.2f} o custo médio por trecho.')

  elif opcao == 3:
    print("Dados estatísticos")
  elif opcao == 4:
    print("Finalizando o programa...")
    break
  else:
    print("Opção inválida! Digite um número entre 1 e 4")
