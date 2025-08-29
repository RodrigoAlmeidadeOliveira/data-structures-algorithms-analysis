# Sistema Integrado - Estruturas de Dados + Cadastro de Matrículas

## Visão Geral

Este sistema integra a análise comparativa de estruturas de dados com um sistema realístico de cadastro de matrículas de estudantes/funcionários, permitindo experimentos com dados mais próximos da realidade.

## Arquivos Principais

### Núcleo da Integração
- **`models.py`**: Classes `Record` e `DataGenerator` atualizadas para compatibilidade
- **`main.py`**: Interface principal com suporte a dados realísticos
- **`experiments.py`**: Runner de experimentos atualizado

### Módulos de Cadastro
- **`student_registration_data.py`**: Gerador de dados realísticos de estudantes
- **`student_registration_experiments.py`**: Experimentos específicos para cadastro
- **`student_data_analysis.py`**: Análise estatística dos dados

### Arquivos de Teste
- **`test_integration.py`**: Testes de integração entre os sistemas

## Como Usar

### 1. Executar com Dados Realísticos (Padrão)
```bash
python main.py
```
- Usa dados realísticos de estudantes/funcionários
- Tenta carregar de arquivos existentes (student_data_*.json)
- Se não encontrar, gera novos dados

### 2. Executar com Dados Básicos
```bash
python main.py --basic
```
- Usa o gerador básico original (dados sintéticos simples)
- Mais rápido para testes de desenvolvimento

### 3. Forçar Geração de Novos Dados
```bash
python main.py --generate
```
- Gera novos dados realísticos sem usar arquivos existentes
- Útil para experimentos com dados diferentes

### 4. Testar Integração
```bash
python test_integration.py
```
- Executa testes básicos de compatibilidade
- Executa um experimento pequeno para validação

## Estrutura dos Dados

### Campos do Record
```python
class Record:
    matricula: int          # 9 dígitos (chave primária)
    nome: str              # Nome completo
    salario: float         # Salário/bolsa em R$
    codigo_setor: int      # Código do setor/departamento
    cpf: str               # CPF no formato XXX.XXX.XXX-XX
    email: str             # Email institucional
    telefone: str          # Telefone de contato
    cargo: str             # Função/cargo
    status: str            # Status (Ativo, Inativo, etc.)
    # ... outros campos opcionais
```

### Dados Realísticos Gerados
- **Nomes**: Lista de nomes brasileiros realísticos
- **Matrículas**: Formato YYYYNNNNN (ano + sequencial)
- **Setores**: 10 setores predefinidos (1001-1010)
- **Salários**: Baseados no cargo (R$ 400 - R$ 25.000)
- **Cargos**: 16 tipos (estudantes, professores, técnicos, etc.)
- **Dados pessoais**: CPF, telefone, email, endereço fictícios

## Configuração do DataGenerator

### Opções de Configuração
```python
generator = DataGenerator(
    use_realistic_data=True,    # True = dados realísticos, False = dados básicos
    data_source="file"          # "file" = tenta carregar, "generate" = sempre gera
)
```

### Carregar Dados Específicos
```python
# Carrega de arquivo específico
records = generator.load_from_file("student_data_10000.json", 10000)

# Gera dados com seed específica
records = generator.generate_records(1000, seed=42)

# Obtém estatísticas dos dados
stats = generator.get_data_statistics(records)
```

## Compatibilidade

### Estruturas de Dados Suportadas
- **Linear Array**: Compatível com ambos os tipos de dados
- **BST/AVL**: Usa matrícula como chave de ordenação
- **Hash Table**: 
  - Função hash baseada na matrícula
  - Suporta diferentes tamanhos (M=100, 1000, 5000)
  - Três funções hash (division, multiplication, folding)

### Conversão Automática
- `StudentRecord` → `Record`: Conversão automática e transparente
- Todos os campos essenciais são preservados
- Campos adicionais são armazenados como atributos dinâmicos

## Saídas Geradas

### Arquivos de Resultados
- `experiment_results_realistic.json`: Resultados com dados realísticos
- `experiment_results_basic.json`: Resultados com dados básicos

### Gráficos
- `plots/insertion_times_realistic.png`: Tempos de inserção (dados realísticos)
- `plots/search_times_realistic.png`: Tempos de busca (dados realísticos)
- `plots/iterations_comparison_realistic.png`: Comparação de iterações
- Versões `_basic.png` para dados básicos

### Datasets Gerados
- `student_data_1000.json`: 1.000 registros realísticos
- `student_data_5000.json`: 5.000 registros realísticos
- `student_data_10000.json`: 10.000 registros realísticos
- `student_data_25000.json`: 25.000 registros realísticos
- `student_data_50000.json`: 50.000 registros realísticos

## Análises Específicas para Dados Realísticos

### Estatísticas Adicionais
- **Distribuição salarial por cargo**: Análise de faixas salariais realísticas
- **Distribuição por setor**: Contagem de funcionários por departamento
- **Análise temporal**: Distribuição de ingressos por ano (baseado na matrícula)
- **Demografia de cargos**: Proporção de estudantes vs. funcionários vs. professores

### Métricas de Performance Contextualizadas
- **Busca por matrícula**: Cenário mais comum em sistemas acadêmicos
- **Busca por CPF**: Cenário alternativo para identificação
- **Busca por setor**: Relatórios por departamento
- **Consultas por faixa salarial**: Análises de RH

## Casos de Uso Demonstrados

### 1. Sistema Acadêmico
- Consulta de matrícula por funcionários da secretaria
- Performance: Hash table oferece busca em ~1 microsegundo

### 2. Sistema de RH
- Geração de relatórios por setor
- Listagem de funcionários por faixa salarial

### 3. Sistema de Atendimento
- Busca por nome (parcial) para localização de pessoas
- Performance degradada propositalmente para demonstrar limitações

## Vantagens da Integração

### Para Educação
1. **Dados mais realísticos**: Estudantes veem cenários reais de uso
2. **Contexto aplicado**: Estruturas de dados resolvendo problemas reais
3. **Análise comparativa**: Performance com dados representativos

### Para Pesquisa
1. **Datasets consistentes**: Mesmos dados para todos os experimentos
2. **Reprodutibilidade**: Sementes controladas permitem repetição
3. **Escalabilidade**: Fácil ajuste de tamanhos de dataset

### Para Desenvolvimento
1. **Compatibilidade mantida**: Sistema original funciona sem alterações
2. **Extensibilidade**: Novos tipos de dados facilmente adicionados
3. **Modularidade**: Componentes independentes podem ser usados separadamente

## Limitações e Considerações

### Performance
- Dados realísticos podem ser mais lentos de gerar
- Arquivos JSON grandes para datasets maiores
- Recomenda-se usar `--basic` para desenvolvimento rápido

### Memória
- Datasets grandes consomem mais RAM
- StudentRecord tem mais campos que Record básico
- Considere usar datasets menores em máquinas limitadas

### Dependências
- Sistema graciosamente degrada se módulos de estudante não estiverem disponíveis
- Funcionalidade básica sempre disponível

## Troubleshooting

### Erro: "Módulo student_registration_data não encontrado"
- **Solução**: Use `python main.py --basic` ou instale os módulos
- **Causa**: Módulos de cadastro não estão no PYTHONPATH

### Experimentos muito lentos
- **Solução**: Use datasets menores ou `--basic`
- **Causa**: Dados realísticos são mais complexos de processar

### Arquivos não encontrados
- **Solução**: Use `--generate` para criar novos arquivos
- **Causa**: Arquivos de dados não foram gerados ainda

### Erros de importação
- **Solução**: Verifique se todos os arquivos estão no mesmo diretório
- **Instale dependências**: `pandas`, `matplotlib`, `numpy`, `tabulate`

## Próximos Passos

### Melhorias Sugeridas
1. **Interface gráfica**: Dashboard para visualização dos resultados
2. **Mais estruturas**: B-trees, Tries, Skip Lists
3. **Análise de concorrência**: Testes com múltiplas threads
4. **Persistência**: Integração com bancos de dados reais
5. **Cache inteligente**: Otimização de consultas frequentes

### Extensões Possíveis
1. **Outros domínios**: Sistemas de vendas, estoque, etc.
2. **Dados reais**: Integração com APIs de universidades
3. **Análise ML**: Predição de performance baseada em características dos dados
4. **Benchmarking**: Comparação com bibliotecas padrão (dict, list, etc.)