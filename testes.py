#informações apenas para teste
km_total = 1000
itens = {'LANCHA': 10000, 'SUV': 4000, 'CARRO': 500, 'MOTO': 499}
#ordena os itens por peso
itens_ordenados_por_peso = dict(sorted(itens.items(), key=lambda x: x[1], reverse=True))
peso_total_carga = sum(itens.values())
cidades = ['ARACAJU', 'BELEM', 'VITORIA']
distancias_cidades = {'ARACAJU - BELEM': 2079, 'BELEM - VITORIA': 3108}
paradas_itens_dict = {'BELEM': ['CARRO', 'MOTO']}
itens_por_trecho = {'ARACAJU - BELEM': [], 'BELEM - VITORIA': []}

#capacidade máxima de cada caminhão
capacidade_caminhoes = {'P': 1000, 'M': 4000, 'G': 10000}
#custo por km rodado de cada caminhão
custo_caminhoes = {'P': 4.87, 'M': 11.92, 'G': 27.44}

'''       DAQUI PRA BAIXO AINDA NÃO ESTÁ NO CÓDIGO GERAL ! ! ! ! ! ! ! ! ! !      '''

#função para distribuir os itens da melhor forma entre caminhões
def distribuir_itens_caminhoes(capacidade_caminhoes, itens):

  #identifica quantidade e modelo do(s) caminhão(ões) necessário(s) para o transporte
  caminhoes_necessarios = {'P': 0, 'M': 0, 'G': 0}
  capacidade_atual_caminhoes = capacidade_caminhoes
  itens_atual_caminhoes = {'P': [], 'M': [], 'G': []}

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
  

  itens_na_funcao = itens.copy()
  
  while peso_atual_carga > 0:
    
    #itera nos itens da carga do maior ao menor peso
    for item, peso in itens.items():
      #tenta colocar o item no maior caminhão que ainda tem capacidade
      for modelo in ['G', 'M', 'P']:
        capacidade = capacidade_atual_caminhoes[modelo]
        if peso <= capacidade:
          #adiciona o item no caminhão, e atualiza a capacidade restante do caminhão
          peso_atual_carga -= peso
          capacidade_atual_caminhoes[modelo] -= peso
          itens_atual_caminhoes[modelo].append(item)

          #calcula a capacidade restante em todos os caminhões após a inclusão do item
          capacidades_restantes = {k: v-peso if k!=modelo else v for k,v in capacidade_atual_caminhoes.items()}

          print(capacidade_atual_caminhoes)
          print(capacidades_restantes)
          
          #escolhe o caminhão que deixaria a menor capacidade restante, descartando os com capacidade negativa
          modelo_menor_restante = min([modelo for modelo in capacidades_restantes if capacidades_restantes[modelo] >= 0], key=capacidades_restantes.get)

          print(f'{item} no {modelo_menor_restante}')

          capacidade_menor_restante = capacidades_restantes[modelo_menor_restante]
          #se a capacidade restante de outro caminhão for menor que o do em que o item foi colocado, transferir
          #alterar item de caminhão (remove o item do caminhão atual e adiciona no outro)
          if capacidade_menor_restante < capacidade_atual_caminhoes[modelo]:
            itens_atual_caminhoes[modelo_menor_restante].append(item)
            capacidade_atual_caminhoes[modelo_menor_restante] -= peso
            itens_atual_caminhoes[modelo].remove(item)
            capacidade_atual_caminhoes[modelo] += peso

          itens_na_funcao.pop(item)


          #se a capacidade atual do caminhão incluído ficar menor que o item restante mais leve, limpá-lo
          item_mais_leve = min(itens_na_funcao.values())

          if capacidade_atual_caminhoes[modelo] < item_mais_leve:
            if modelo == 'P':
              capacidade_atual_caminhoes['P'] = 1000
            elif modelo == 'M':
              capacidade_atual_caminhoes['M'] = 4000
            elif modelo == 'G':
              capacidade_atual_caminhoes['G'] = 10000
            caminhoes_necessarios[modelo] += 1
            itens_na_funcao.pop(item)

            itens_atual_caminhoes[modelo] = []
            
          #verifica se o item já estava em outro caminhão, se sim, remove do caminhão anterior
          for tamanho, itens_array in itens_atual_caminhoes.items():
            if item in itens_array and tamanho != modelo:
              itens_array.remove(item)
              capacidade_atual_caminhoes[tamanho] += peso
  
          adicionado = True
          break
              

    print(f'itens_na_funcao restantes que devem ser excluídos antes da linha 116):\n{itens_na_funcao}')
      
  
    itens_restantes = list(itens_na_funcao)


    

  
    # função para adicionar a possiveis_combinacoes as diferentes quantidade de cada caminhão para transportar os itens_restantes
    def distribuir_itens_restantes(capacidade_caminhoes, itens_restantes_dict):
      possiveis_combinacoes = []
      # capacidade atual dos caminhões, que deve ser reduzida quando um item for incluso nele
      capacidade_atual_caminhoes = {'P': capacidade_caminhoes['P'], 'M': capacidade_caminhoes['M'], 'G': capacidade_caminhoes['G']}
      n = len(itens_restantes_dict)
      for i in range(n+1):
        for j in range(n+1-i):
          p = i
          m = j
          g = n-i-j
          # verificando se é possível alocar os itens nos caminhões
          for item, peso in itens_restantes_dict.items():
            if peso <= capacidade_atual_caminhoes['P'] and p > 0:
              p -= 1
            elif peso <= capacidade_atual_caminhoes['M'] and m > 0:
              m -= 1
            elif peso <= capacidade_atual_caminhoes['G'] and g > 0:
              g -= 1
          # se todos os itens foram alocados corretamente, adiciona a combinação na lista
          if p == 0 and m == 0 and g == 0:
            possiveis_combinacoes.append({'P': i, 'M': j, 'G': n-i-j})
          # restaura a capacidade dos caminhões para a próxima iteração
          capacidade_atual_caminhoes = {'P': capacidade_caminhoes['P'], 'M': capacidade_caminhoes['M'], 'G': capacidade_caminhoes['G']}
      return possiveis_combinacoes
  
    if itens_restantes:    
      #cria dicionário com as chaves sendo os itens e valores sendo seus pesos em "itens"
      itens_restantes_dict = {} 
      for item_restante in itens_restantes: 
        itens_restantes_dict[item_restante] = itens_na_funcao[item_restante]

      possiveis_combinacoes = distribuir_itens_restantes(capacidade_caminhoes, itens_restantes_dict)
      peso_atual_carga = 0
      itens_restantes = {} 
      # verificando a combinação de menor valor possível para os itens restantes
      total_cada_combinacao_possivel = []
      for combinacao in possiveis_combinacoes:
        total = 0
        for caminhao in custo_caminhoes:
          total += combinacao[caminhao] * custo_caminhoes[caminhao]
        total_cada_combinacao_possivel.append(total)
      combinacao_menor_custo = min(total_cada_combinacao_possivel)
      # atualizando as quantidades necessárias de cada caminhão de acordo com a combinação de menor custo
      for index, combinacao in enumerate(possiveis_combinacoes):
        if total_cada_combinacao_possivel[index] == combinacao_menor_custo:
          for caminhao in caminhoes_necessarios:
            caminhoes_necessarios[caminhao] += combinacao[caminhao]
          break
     


  print(f'{caminhoes_necessarios} \n')



  return caminhoes_necessarios

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

print(itens_por_trecho_com_peso)

#chama função de distribuição e armazena quais caminhões serão usados por trecho
caminhoes_necessarios_por_trecho = {}

for trecho, itens_trecho in itens_por_trecho_com_peso.items():
  resultado_funcao = distribuir_itens_caminhoes(capacidade_caminhoes, itens_trecho)
  caminhoes_necessarios_por_trecho[trecho] = resultado_funcao

print(f'caminhoes necessários por trecho:\n {caminhoes_necessarios_por_trecho}\n')

#calcula o custo por trecho e armazena
custo_por_trecho = {}

for trecho, caminhoes in caminhoes_necessarios_por_trecho.items():
  custo_total_trecho = 0
  for porte, qtd_caminhoes in caminhoes.items():
    custo_total_trecho += qtd_caminhoes * custo_caminhoes[porte]
  custo_total_trecho *= 3 # considerando 3 caminhões por trecho
  custo_total_trecho += distancias_cidades[trecho] * 0.5 # adicionando custo fixo de R$0,50 por km
  custo_por_trecho[trecho] = custo_total_trecho

'''
print(f'custo por trecho: {custo_por_trecho}')

# {'P': 4.87, 'M': 11.92, 'G': 27.44} 9,74
# resultado esperado{'ARACAJU - BELEM': 38848.68, 'BELEM - VITORIA': 185963.52}


custo_total = sum(lista_necessariosXcusto)*km_total


#calcula o custo total pela qtd de cada caminhão X km
lista_necessariosXcusto = []
for tamanho, quantidade in caminhoes_necessarios.items():
    lista_necessariosXcusto.append(custo_caminhoes[tamanho] * quantidade)



#imprime resultado
print(f'Saindo de {cidades[0]} até {cidades[-1]}, a distância total a ser percorrida na rota é de {km_total} km')
print(f'Para transportar os itens {list(itens.keys())},\n de forma a resultar no menor custo por km rodado., serão necessários:')
#imprime quantidade de caminhões necessários para transportar a carga
for modelo, qtd in caminhoes_necessarios.items():
  if qtd > 0:
    print(f'{qtd} caminhão(ões) de porte {modelo}')
print(f'O valor total do frete é R$ {custo_total}, sendo R$ {custo_por_trecho} o custo unitário médio por trecho.')
'''
