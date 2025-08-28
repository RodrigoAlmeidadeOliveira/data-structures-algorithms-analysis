# INSTRUÇÕES DE USO

## 1. Instalação das Dependências

Antes de executar o projeto, instale as dependências necessárias:

```bash
pip install -r requirements.txt
```

## 2. Execução dos Experimentos

### Teste Rápido (Verificar se tudo funciona)
```bash
python test_quick.py
```

### Experimento com Datasets Pequenos (Rápido - ~1 minuto)
```bash
python run_small.py
```

### Experimento Completo (Conforme especificação - ~10-20 minutos)
```bash
python main.py
```

## 3. Arquivos Gerados

Após executar os experimentos, os seguintes arquivos serão criados:

- `experiment_results.json` ou `experiment_results_small.json`: Dados brutos em JSON
- `plots/`: Diretório com gráficos de análise
  - `insertion_times.png`: Comparação de tempos de inserção
  - `search_times.png`: Comparação de tempos de busca
  - `iterations_comparison.png`: Análise de iterações
  - `hash_analysis.png`: Análise específica de tabelas hash
  - `tree_heights.png`: Altura das árvores BST e AVL
- `results_tables.tex`: Tabelas em formato LaTeX (se solicitado)

## 4. Estrutura do Código

### Arquivos Principais:
- `models.py`: Define a classe Record e o gerador de dados
- `linear_array.py`: Implementação do Array Linear
- `binary_search_tree.py`: Implementação da BST sem balanceamento
- `avl_tree.py`: Implementação da árvore AVL (BST balanceada)
- `hash_table.py`: Implementação da Tabela Hash com 3 funções
- `metrics.py`: Sistema de coleta de métricas de desempenho
- `experiments.py`: Módulo que executa os experimentos
- `analysis.py`: Análise estatística e geração de gráficos
- `main.py`: Script principal para experimento completo

### Scripts de Execução:
- `test_quick.py`: Teste rápido de funcionalidade
- `run_small.py`: Experimento com datasets menores
- `main.py`: Experimento completo conforme especificação

## 5. Parâmetros dos Experimentos

### Tamanhos de Dados (N):
- Teste rápido: 100 registros
- Experimento pequeno: 1.000, 5.000, 10.000
- Experimento completo: 10.000, 50.000, 100.000

### Tabela Hash - Tamanhos (M):
- 100, 1.000, 5.000

### Tabela Hash - Funções:
- Divisão
- Multiplicação
- Folding

### Rodadas por Experimento:
- Teste rápido: 1 rodada
- Experimento pequeno: 3 rodadas
- Experimento completo: 5 rodadas

## 6. Métricas Coletadas

- **Tempo de execução**: Para cada operação (inserção e busca)
- **Número de iterações**: Contagem de operações internas
- **Altura das árvores**: Para BST e AVL
- **Taxa de colisão**: Para tabelas hash
- **Load factor**: Para tabelas hash
- **Comprimento de cadeias**: Para tabelas hash

## 7. Análises Realizadas

1. **Comparação de desempenho**: Entre todas as estruturas
2. **Análise de complexidade**: Teórica vs. observada
3. **Análise estatística**: Média e desvio padrão
4. **Taxa de crescimento**: Estimativa empírica da complexidade
5. **Visualizações gráficas**: Múltiplos gráficos comparativos

## 8. Observações Importantes

- Os experimentos devem ser executados em máquina local (não em VMs ou Colab)
- Cada experimento é repetido múltiplas vezes para confiabilidade estatística
- Os dados são gerados aleatoriamente com seed fixo para reprodutibilidade
- A ordem de inserção nas árvores é embaralhada em cada rodada
- As buscas são realizadas em uma amostra aleatória dos dados

## 9. Interpretação dos Resultados

### Array Linear:
- Inserção O(1) - muito rápida
- Busca O(n) - lenta para grandes volumes

### BST (sem balanceamento):
- Performance varia com ordem de inserção
- Pode degradar para O(n) em casos ruins

### AVL (balanceada):
- Garantia de O(log n) para todas operações
- Overhead de balanceamento na inserção

### Tabela Hash:
- Performance depende do load factor (N/M)
- Funções hash diferentes têm impactos distintos
- Colisões afetam desempenho

## 10. Para o Relatório

Use os dados gerados em `experiment_results.json` e os gráficos em `plots/` para compor o relatório científico no formato IEEE de duas colunas, conforme especificado.