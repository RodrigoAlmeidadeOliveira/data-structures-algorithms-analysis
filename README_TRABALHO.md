# TRABALHO 01 - ANÁLISE COMPARATIVA DE ESTRUTURAS DE DADOS

## Descrição
Implementação completa para análise comparativa de estruturas de dados conforme especificado no trabalho da disciplina de Fundamentos de Algoritmos e Estrutura de Dados da PUCPR.

## Arquivo Principal
**`trabalho_completo.py`** - Arquivo único contendo toda a implementação necessária

## Estruturas Implementadas
1. **Array Linear** - Lista com inserção O(1) e busca O(n)
2. **Árvore de Busca Binária (BST)** - Sem balanceamento
3. **Árvore AVL** - Com balanceamento automático
4. **Tabela Hash** - Com 3 funções hash diferentes:
   - Divisão
   - Multiplicação
   - Folding

## Requisitos Atendidos

### ✅ Dados
- Geração de registros fictícios com volumes N = {10.000, 50.000, 100.000}
- Cada registro contém: Matrícula (9 dígitos), Nome, Salário, Código do Setor

### ✅ Estruturas de Dados
- Array Linear implementado
- BST com e sem balanceamento (BST normal e AVL)
- Tabela Hash com 3 funções distintas
- Tratamento de colisões com M = {100, 1000, 5000}
- Avaliação de colisões e load factor

### ✅ Métricas Coletadas
- Tempo de execução para inserção e busca
- Número de iterações
- Altura das árvores
- Taxa de colisão das tabelas hash
- Load factor
- Comprimento de cadeias (hash)
- Uso de memória e CPU (via psutil e tracemalloc)

### ✅ Análise Crítica
- Complexidade teórica vs observada
- Análise assintótica (Big-O)
- Comparação entre estruturas
- Trade-offs identificados
- 5 rodadas independentes por experimento

### ✅ Visualizações
- Gráficos de tempo de inserção
- Gráficos de tempo de busca
- Comparação de iterações
- Análise específica de hash tables
- Altura das árvores BST vs AVL

## Como Executar

### 1. Instalar Dependências
```bash
pip install numpy pandas matplotlib psutil tabulate
```

### 2. Executar o Programa
```bash
python trabalho_completo.py
```

### 3. Tempo de Execução
- Experimento completo: ~10-20 minutos
- O programa mostra progresso durante a execução

## Saídas Geradas

### Arquivos CSV
- **`experiment_results.csv`** - Resumo estatístico com médias e desvios
- **`experiment_details.csv`** - Dados detalhados de cada rodada individual
- **`plots/`** - Diretório com todos os gráficos gerados:
  - `insertion_times.png` - Comparação de tempos de inserção
  - `search_times.png` - Comparação de tempos de busca
  - `iterations_comparison.png` - Análise de iterações
  - `hash_analysis.png` - Análise específica de tabelas hash
  - `tree_heights.png` - Altura das árvores BST e AVL

### Console
- Tabelas resumo com estatísticas
- Análise de complexidade
- Métricas específicas por estrutura
- Comparações diretas

## Estrutura do Código

O arquivo `trabalho_completo.py` está organizado em 7 seções:

1. **MODELOS DE DADOS** - Classe Record e gerador de dados
2. **ESTRUTURAS DE DADOS** - Implementações completas:
   - LinearArray
   - BinarySearchTree
   - AVLTree
   - HashTable
3. **SISTEMA DE MÉTRICAS** - Coleta de métricas de desempenho
4. **EXPERIMENTOS** - Runner para executar todos os testes
5. **ANÁLISE E VISUALIZAÇÃO** - Análise estatística e gráficos
6. **FUNÇÕES DE APRESENTAÇÃO** - Formatação de resultados
7. **FUNÇÃO PRINCIPAL** - Orquestração do experimento

## Complexidade Observada

### Array Linear
- **Inserção**: O(1) - Constante
- **Busca**: O(n) - Linear

### BST (sem balanceamento)
- **Inserção**: O(log n) médio, pode degradar para O(n)
- **Busca**: O(log n) médio, pode degradar para O(n)

### AVL (balanceada)
- **Inserção**: O(log n) garantido
- **Busca**: O(log n) garantido

### Tabela Hash
- **Inserção**: O(1) médio, O(n) pior caso
- **Busca**: O(1) médio, O(n) pior caso
- Performance varia com load factor e função hash

## Observações Importantes

1. **Reprodutibilidade**: Usa seed fixo (42) para garantir resultados reproduzíveis
2. **Múltiplas Rodadas**: 5 rodadas por experimento para confiabilidade estatística
3. **Embaralhamento**: Dados são embaralhados antes de inserir nas árvores
4. **Amostragem**: Busca usa amostra de 1000 registros para eficiência

## Conformidade com Requisitos

Este código atende **TODOS** os requisitos especificados no PDF do trabalho:

- ✅ Implementação sem uso de bibliotecas prontas de estruturas de dados
- ✅ Volumes de dados conforme especificado
- ✅ Todas as estruturas implementadas
- ✅ Métricas de recursos (CPU, memória, iterações)
- ✅ Análise crítica com complexidade teórica vs observada
- ✅ Múltiplas rodadas independentes
- ✅ Código em Python (.py, não Jupyter)
- ✅ Documentação completa

## Para o Relatório IEEE

Use os dados gerados em `experiment_results.csv` e os gráficos em `plots/` para compor o relatório científico no formato IEEE de duas colunas, conforme especificado no trabalho.

### Estrutura dos CSVs Gerados

#### `experiment_results.csv` (Resumo Estatístico)
Contém métricas agregadas com médias e desvios padrão:
- `structure`: Nome da estrutura de dados
- `data_size`: Tamanho do dataset (N)
- `operation`: Tipo de operação (insert/search)
- `mean_time`: Tempo médio de execução (segundos)
- `std_time`: Desvio padrão do tempo
- `mean_memory`: Uso médio de memória (MB)
- `std_memory`: Desvio padrão da memória
- `mean_iterations`: Número médio de iterações
- `std_iterations`: Desvio padrão das iterações
- `avg_cpu_percent`: Uso médio de CPU (%)
- `avg_memory_usage_mb`: Uso médio de memória (MB)
- `avg_peak_memory_mb`: Pico médio de memória (MB)
- `hash_table_size`: Tamanho M (hash tables)
- `hash_function`: Função hash usada
- `balanced`: Se a árvore é balanceada

#### `experiment_details.csv` (Dados por Rodada)
Contém dados brutos de cada rodada individual:
- `structure`: Nome da estrutura
- `data_size`: Tamanho do dataset
- `operation`: Tipo de operação
- `round`: Número da rodada (1-5)
- `execution_time`: Tempo de execução da rodada
- `memory_usage_mb`: Uso de memória da rodada
- `peak_memory_mb`: Pico de memória da rodada
- `cpu_percent`: Uso de CPU da rodada
- `iterations`: Iterações da rodada
- `hash_table_size`: Tamanho M (hash tables)
- `hash_function`: Função hash
- `load_factor`: Load factor (hash tables)
- `collision_rate`: Taxa de colisões
- `avg_chain_length`: Comprimento médio de cadeias
- `max_chain_length`: Comprimento máximo de cadeias
- `balanced`: Árvore balanceada (BST/AVL)
- `tree_height`: Altura da árvore

### Métricas de Recursos Coletadas
- **Tempo de Processamento**: Medido com `time.perf_counter()` para alta precisão
- **Consumo de CPU**: Percentual de uso via `psutil.Process().cpu_percent()`
- **Consumo de Memória**: 
  - Uso de memória RSS (Resident Set Size) em MB
  - Pico de memória durante a operação via `tracemalloc`
- **Iterações**: Contador interno de cada algoritmo

O formato CSV facilita análise em Excel, Google Sheets, R, Python (pandas), etc.