#informações apenas para teste
km_total = 1000
itens = {'LANCHA': 10000, 'SUV': 4000, 'CARRO': 500, 'MOTO': 499}
#ordena os itens por peso
itens_ordenados_por_peso = dict(sorted(itens.items(), key=lambda x: x[1], reverse=True))
peso_total_carga = sum(itens.values())
cidades = ['ARACAJU', 'BELEM', 'VITORIA']
distancias_cidades = {'ARACAJU - BELEM': 2079, 'BELEM - VITORIA': 3108}
paradas_itens_dict = {'BELEM': ['CARRO', 'MOTO']}
paradas_cidades = ['BELEM']
itens_por_trecho = {'ARACAJU - BELEM': [], 'BELEM - VITORIA': []}

#capacidade máxima de cada caminhão
capacidade_caminhoes = {'P': 1000, 'M': 4000, 'G': 10000}
#custo por km rodado de cada caminhão
custo_caminhoes = {'P': 4.87, 'M': 11.92, 'G': 27.44}

'''       DAQUI PRA BAIXO AINDA NÃO ESTÁ NO CÓDIGO GERAL ! ! ! ! ! ! ! ! ! !      '''

#começa com primeiro trecho com todos os itens, e os remove conforme as paradas
itens_por_trecho[list(itens_por_trecho.keys())[0]] = list(itens_ordenados_por_peso.keys())

for i in range(len(cidades) - 1):
  trecho = cidades[i] + ' - ' + cidades[i+1]
  itens_trecho = []
  if trecho in itens_por_trecho:
    itens_trecho = itens_por_trecho[trecho]
  for item, peso in itens.items():
    if item not in paradas_itens_dict.get(cidades[i], []) and item not in itens_trecho:
      itens_trecho.append(item)
  itens_por_trecho[trecho] = itens_trecho

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
print(f'Saindo de {cidades[0]} até {cidades[-1]}, a distância total a ser percorrida na rota é de {km_total} km - considerando paradas com itens a descarregar em {paradas_cidades}.')
print(f'Para transportar os itens {list(itens.keys())},\n de forma a resultar no menor custo por km rodado., serão necessários:')
#imprime quantidade de caminhões necessários para transportar a carga
for trecho, caminhoes in caminhoes_necessarios_por_trecho.items():
  print(f'No trecho {trecho}')
  for caminhao, qtd in caminhoes.items():
    if qtd > 0:
      print(f'{qtd} caminhão(ões) de porte {caminhao}')
print(f'O valor total do frete é R$ {custo_total:.2f}, sendo R$ {custo_total/len(custo_por_trecho):.2f} o custo médio por trecho.')
