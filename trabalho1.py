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

# # ENTRA DO NÚMERO DE BOMBEIROS
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
nome_do_arquivo = 'trab1_1.txt'
num_bombeiros = 7


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
vertices_protegidos_lista = []
vertices_queimados_lista = [no_inicial_fogo]
vertices_ilesos_lista = []

while True:
    etapas += 1

    # A PARTIR DE AGORA ENTRA A ESTRATÉGIA DO BOMBEIRO:  
    # DEFINIMOS O ALGORÍTIMO DO MAIOR VIZINHO QUE VAI QUEIMAR.

    candidatos = [] # PODEM RECEBER O BOMBEIRO
    melhores_candidatos = [] # VÃO RECEBER O BOMBEIRO

    # PERCORRE O GRÁFICO PARA VERIFICAR SE O NÓ VAI QUEIMAR.
    for no in grafo:
        if no['estado'] == 0:
            # VERIFICA SE TEM VIZINHO PEGANDO FOGO
            # SE SIM, ESSE NÓ VAI QUEIMAR NA PRÓXIMA ETAPA, PORTANTO, É UM POTENCIAL CANDIDATO
            for vizinho_id in no['vizinhos']:
                if grafo[vizinho_id]['estado'] == 1:
                    # GUARDA O NÚMERO DE VIZINHOS E O ID DO NÓ
                    candidatos.append((len(no['vizinhos']), no['id']))
                    break

    #ORDENANDO A LISTA DE ACORDO COM NÚMERO DE VIZINHOS 
    # (MAIOR PARA O MENOR)
    candidatos.sort(key=lambda x: x[0], reverse=True)

    # DEFININDO O NÚMERO DE NÓS A SEREM PROTEGIDOS
    # MIN -> POIS NÃO SERÁ MAIOR QUE NÚMERO DE BOMBEIROS E NÚMERO DE CANDIDATOS.
    num_proteger = min(num_bombeiros, len(candidatos))

    # PEGAR OS MELHORES ATÉ O "num_proteger"
    for i in range(num_proteger):
    # candidatos[i][1] é o id do nó
        melhores_candidatos.append(candidatos[i][1])

    # BOMBEIRO PROTEGE OS NÓS SELECIONADOS
    for candidato_id in melhores_candidatos:
        vertices_protegidos_lista.append(candidato_id)
        grafo[candidato_id]['estado'] = 2
    
    
     
    # FOGO ESPALHANDO
    queimou = deque()
    
    for no_atual_id in fila_fogo:
        for vizinho_id in grafo[no_atual_id]['vizinhos']:
            if grafo[vizinho_id]['estado'] == 0:
                grafo[vizinho_id]['estado'] = 1
                vertices_queimados_lista.append(vizinho_id)
                queimou.append(vizinho_id)
            
    print(f"\n--- Etapa {etapas} ---")
    if melhores_candidatos:
        print(f"Bombeiros posicionados nos vértices: {sorted(melhores_candidatos)}")
    else:
        print("Nenhum bombeiro acionado. Não há mais nós para proteger.")

    fila_fogo = queimou
    if not fila_fogo:
      break


print("\n--- RESULTADO ---")

# RECUPERA OS VERTICES QUE FICARAM ILESOS
for no in grafo:
    if no['estado'] == 0:
        vertices_ilesos_lista.append(no['id'])

#IMPRIME O RESULTADO
print(f"Total de etapas: {etapas}")
print(f"Quantidade de vértices queimados: {len(vertices_queimados_lista)}")
print(vertices_queimados_lista)
print(f"Quantidade de vértices salvos: {len(vertices_protegidos_lista)}")
print(vertices_protegidos_lista)
print(f"Quantidade de vértices ilesos: {len(vertices_ilesos_lista)}")
print(vertices_ilesos_lista)