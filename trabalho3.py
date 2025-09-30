from collections import deque

# ENTRADA DO NOME DO ARQUIVO
# while True:
#     nome_do_arquivo = input("Digite o nome do arquivo do grafo (ex: trab1_1.txt): ")
#     try:
#         # Tenta abrir o arquivo para verificar se ele existe
#         with open(nome_do_arquivo, 'r', encoding='utf-8'):
#             pass # Se não der erro, o arquivo existe
#         break
#     except FileNotFoundError:
#         print(f"Erro: O arquivo '{nome_do_arquivo}' não foi encontrado. Tente novamente.")

# ENTRA DO NÚMERO DE BOMBEIROS
# while True:
#     try:
#         entrada_bombeiros = input("Quantos bombeiros serão utilizados (1 a 10)? ")
#         num_bombeiros = int(entrada_bombeiros)
#         if 1 <= num_bombeiros <= 10:
#             break
#         else:
#             print("Por favor, digite um número entre 1 e 10.")
#     except ValueError:
#         print("Entrada inválida. Por favor, digite um número.")
num_bombeiros = 10
nome_do_arquivo = 'trabTeste.txt'


# VARIÁVEIS DO GRAFO
num_vertices = 0
num_arestas = 0
no_inicial_fogo = 0
grafo = []


#PEGANDO AS INFORMAÇÕES DO ARQUIVO
#CONSTRUINDO A ESTRUTURA DO GRAFO
try:
    with open(nome_do_arquivo, 'r', encoding='utf-8') as linhas:
        for indice, linha in enumerate(linhas):

            linha_limpa = linha.strip()

            if not linha_limpa:
                continue

            if indice == 0:
                num_vertices = int(linha_limpa)
                for i in range(num_vertices):
                    grafo.append({
                        'id': i,
                        'estado': 0, # 0 = não afetado, 1 = em chamas, 2 = protegido
                        'vizinhos': []
                    })
            elif indice == 1:
                num_arestas = int(linha_limpa)
            elif indice == 2:
                no_inicial_fogo = int(linha_limpa)
            else:
                elementos = linha_limpa.split()
                no1 = int(elementos[0])
                no2 = int(elementos[1])
                
                if 0 <= no1 < num_vertices and 0 <= no2 < num_vertices:
                    grafo[no1]['vizinhos'].append(no2)
                    grafo[no2]['vizinhos'].append(no1)

    # O NÓ INICIAL ( 0 ) JÁ COMEÇA COM FOGO
    if 0 <= no_inicial_fogo < num_vertices:
        grafo[no_inicial_fogo]['estado'] = 1

except Exception as e:
    print(f"Ocorreu um erro ao processar o arquivo: {e}")
    exit()

# VARIÁVEIS DE ITERAÇÃO
etapas = 0
fila_fogo = deque([no_inicial_fogo])
vertices_protegidos_lista = set()
vertices_queimados_lista = set()
vertices_ilesos_lista = set()
vertices_queimados_lista.add(no_inicial_fogo)


while True:
    etapas += 1
    
    # ALGORITMO ANÁLISADOR DE DANO FUTURO

    #DEFINIMOS OS CANDIDATOS EM POTENCIAL
    #SÃO OS VERTICES QUE IRÃO QUEIMAR NA PROXIMA
    candidatos = set()
    for no_atual_id in fila_fogo:
        for vizinho_id in grafo[no_atual_id]['vizinhos']:
            if grafo[vizinho_id]['estado'] == 0:  # AINDA ILESO
                candidatos.add(vizinho_id)

    # SE EXISTE CANDIDATOS, ENTÃO VAMOS TRATAR!
    if candidatos:
        melhores_candidatos = []
        #PARA CADA BOMBEIRO DISPONÍVEL POR ETAPA
        for _ in range(num_bombeiros):
            if not candidatos:
                break
            
            #INCIALIZANDO VARIÁVEIS DE AVALIAÇÃO DO MELHOR CASO
            melhor_candidato = None
            melhor_custo = float("inf")

            # TESTA CADA CANDIDATO EM UMA SIMULAÇÃO
            for candidato_id in candidatos:
                # SIMULANDO PROPAGRAÇÃO CONSIDERANDO candidato PROTEGIDO
                grafo_simulado = [dict(no) for no in grafo]  # CÓPIA DO GRAFO PARA SIMULAÇÃO
                grafo_simulado[candidato_id]['estado'] = 2  # NA CÓPIA, candidato ESTA PROTEGIDO PARA A SIMULAÇÃO
                fogo_simulado = deque(fila_fogo) #VERTICES EM CHAMAS PARA A SIMULAÇÃO

                # LISTA DOS QUEIMADOS NA SIMULAÇÃO
                queimados_simulados = set(vertices_queimados_lista) #LISTA DE QUEIMADOS DURANTE SIMULADO
                protegidos_simulado = set()
                protegidos_simulado.add(candidato_id)

                #SIMULANDO
                for _ in range(3):  # RODADAS A SIMULAR 
                    queimou_simulado = deque() # VERTICE QUEIMANDO NESSA RODADA -> IRÃO SER FOGO NA PRÓXIMA
                    for no_atual_id in fogo_simulado:
                        for vizinho_id in grafo_simulado[no_atual_id]['vizinhos']:
                            if grafo_simulado[vizinho_id]['estado'] == 0 and vizinho_id not in protegidos_simulado:
                                grafo_simulado[vizinho_id]['estado'] = 1
                                queimados_simulados.add(vizinho_id)
                                queimou_simulado.append(vizinho_id)
                    fogo_simulado = queimou_simulado

                custo = len(queimados_simulados)

                #AVALIANDO O CUSTO E DEFININDO O MELHOR CANDIDATO
                if custo < melhor_custo:
                    melhor_custo = custo
                    melhor_candidato = candidato_id

            # ALOCANDO O BOMBEIRO NO MELHOR CANDIDATO E CONSEQUENTEMENTE PROTEGENDO O VÉRTICE
            # REMOVENDO O VÉRTICE DA LISTA DE CANDIDATOS
            if melhor_candidato is not None:
                grafo[melhor_candidato]['estado'] = 2
                vertices_protegidos_lista.add(melhor_candidato)
                melhores_candidatos.append(melhor_candidato)
                candidatos.remove(melhor_candidato)

        if melhores_candidatos:
            print(f"Etapa {etapas}: Bombeiros protegeram {melhores_candidatos}")
 
     
    # FOGO ESPALHANDO
    queimou = deque()
    
    for no_atual_id in fila_fogo:
        for vizinho_id in grafo[no_atual_id]['vizinhos']:
            if grafo[vizinho_id]['estado'] == 0:
                grafo[vizinho_id]['estado'] = 1
                vertices_queimados_lista.add(vizinho_id)
                queimou.append(vizinho_id)

    fila_fogo = queimou
    if not fila_fogo:
      break


print("\n--- RESULTADO ---")

# RECUPERA OS VERTICES QUE FICARAM ILESOS
for no in grafo:
    if no['estado'] == 0:
        vertices_ilesos_lista.add(no['id'])

#IMPRIME O RESULTADO
print(f"Total de etapas: {etapas}")
print(f"Quantidade de vértices queimados: {len(list(vertices_queimados_lista))}")
print(vertices_queimados_lista)
print(f"Quantidade de vértices salvos: {len(list(vertices_protegidos_lista))}")
print(vertices_protegidos_lista)
print(f"Quantidade de vértices ilesos: {len(list(vertices_ilesos_lista))}")
print(vertices_ilesos_lista)