#dados para teste:
itens_trecho = {'LANCHA': 8000, 'SUV': 3500, 'CARRO': 1500, 'MOTO': 900}
peso_total_carga = sum(itens_trecho.values())
capacidade_caminhoes = {'P': 1000, 'M': 4000, 'G': 10000}

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
      peso_atual_carga -= peso
      itens_na_funcao.pop(item)
      #tenta colocar o item no maior caminhão que ainda tem capacidade
      for modelo in ['G', 'M', 'P']:
        capacidade = capacidade_atual_caminhoes[modelo]
        if peso <= capacidade:

          print(' ')

          #adiciona o item no caminhão, e reduz peso do item da capacidade do caminhão
          capacidade_atual_caminhoes[modelo] -= peso
          itens_atual_caminhoes[modelo].append(item)

          #se a capacidade do caminhão zerar, limpá-lo
          if itens_na_funcao and (capacidade_atual_caminhoes[modelo] == 0):
            caminhoes_necessarios[modelo] += 1
            capacidade_atual_caminhoes[modelo] = capacidade_caminhoes[modelo]
            itens_atual_caminhoes[modelo] = []
            break

          #calcula a capacidade restante em todos os caminhões após a inclusão do item
          capacidades_restantes = {k: v-peso if k!=modelo else v for k,v in capacidade_atual_caminhoes.items()}
          #escolhe o caminhão que deixaria a menor capacidade restante, descartando os com capacidade negativa
          modelo_menor_restante = min([modelo for modelo in capacidades_restantes if capacidades_restantes[modelo] >= 0], key=lambda modelo: abs(capacidades_restantes[modelo]))

          #verifica se há um caminhão com espaço que não esteja vazio e prioriza
          modelo_prioridade = None
          for modelo_troca in capacidade_atual_caminhoes.keys():
            if (capacidade_atual_caminhoes[modelo_troca] > 0) and (itens_atual_caminhoes[modelo_troca]) and modelo_troca != modelo:
              modelo_prioridade = modelo_troca
              break
          
          #se houver caminhão com espaço que não esteja vazio, escolhe o modelo com prioridade
          if modelo_prioridade:
            modelo_menor_restante = modelo_prioridade
          #caso contrário, escolhe o modelo com menor capacidade restante, desconsiderando negativas
          else:
            modelo_menor_restante = modelo_menor_restante

          print(f'{item} foi 1º incluso em {modelo},\n capacidades_atualizadas: {capacidade_atual_caminhoes}')

          capacidade_menor_restante = capacidades_restantes[modelo_menor_restante]
          #se a capacidade restante e custo de outro caminhão for menor que o do item colocado, transferir
          #alterar item de caminhão (remove o item do caminhão atual e adiciona no outro)
          custo_caminhoes = {'P': 4.87, 'M': 11.92, 'G': 27.44}

          #calcula o custo da combinação de caminhões como está
          combinacao1_necessarios = {'P': 0, 'M': 0, 'G': 0}
          for tamanho in combinacao1_necessarios.keys():
            if itens_atual_caminhoes[tamanho]:
              combinacao1_necessarios[tamanho] = caminhoes_necessarios[tamanho]+1
            else:
              combinacao1_necessarios[tamanho] = caminhoes_necessarios[tamanho]
          custo_caminhoes_necessarios_atual = sum([custo_caminhoes[tamanho]*combinacao1_necessarios[tamanho] for tamanho in combinacao1_necessarios])

          print(f'combinacao1_necessarios: {combinacao1_necessarios}')

          if capacidade_menor_restante < capacidade_atual_caminhoes[modelo]:
            
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
            custo_caminhoes_necessarios_se_item_alterado = sum([custo_caminhoes[tamanho]*combinacao2_necessarios[tamanho] for tamanho in combinacao2_necessarios])
          
            #se o cuto da troca ficar menor, mantê-la. Se não, desfazer a troca
            if custo_caminhoes_necessarios_atual > custo_caminhoes_necessarios_se_item_alterado:
              capacidade_atual_caminhoes[modelo_menor_restante] -= peso
              capacidade_atual_caminhoes[modelo] += peso
              if not itens_na_funcao:
                caminhoes_necessarios = combinacao2_necessarios

              print(f'{item} passado de {modelo} para modelo_menor_restante: {modelo_menor_restante}')

            else:
              itens_atual_caminhoes[modelo_menor_restante].remove(item)
              itens_atual_caminhoes[modelo].append(item)
              if not itens_na_funcao:
                caminhoes_necessarios = combinacao1_necessarios

          else:
            if not itens_na_funcao:
              caminhoes_necessarios = combinacao1_necessarios
          break 

      if itens_na_funcao:
        #se a capacidade atual de algum caminhão ficar menor que o item restante mais leve, limpá-lo
        item_mais_leve = min(itens_na_funcao.values())
        for tamanho_modelo, capacidade_atual_do_modelo in capacidade_atual_caminhoes.items():
          if capacidade_atual_do_modelo < item_mais_leve:
            if itens_atual_caminhoes[tamanho_modelo]:
              # Limpa a capacidade do caminhão
              print('ENTROU NA LINHA 137!!!!!!!!')
              capacidade_atual_caminhoes[tamanho_modelo] = capacidade_caminhoes[tamanho_modelo]
              itens_atual_caminhoes[tamanho_modelo] = []
              caminhoes_necessarios[tamanho_modelo] += 1
         
  return caminhoes_necessarios

resultado_funcao = distribuir_itens_caminhoes(capacidade_caminhoes, itens_trecho)
print(f'{resultado_funcao}\n')
