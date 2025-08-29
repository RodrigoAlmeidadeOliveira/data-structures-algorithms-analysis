# Relatório: Sistema de Cadastro de Matrículas - Análise de Consumo de Recursos

## Resumo Executivo

Este relatório apresenta uma análise detalhada do consumo de recursos em um sistema de cadastro de matrículas de estudantes/funcionários, avaliando diferentes estratégias de armazenamento e busca de dados. O sistema foi testado com registros contendo matrícula (9 dígitos), nome, salário, código do setor, CPF, e outros campos relevantes.

## 1. Estrutura de Dados Implementada

### 1.1 Registro de Matrícula
Cada registro contém os seguintes campos:
- **Matrícula**: 9 dígitos no formato YYYYNNNNN (ano + sequencial)
- **Nome**: Nome completo do estudante/funcionário
- **Salário**: Valor em R$ (salários ou bolsas)
- **Código do Setor**: Identificador numérico do departamento
- **CPF**: CPF no formato XXX.XXX.XXX-XX
- **Data de Ingresso**: Data no formato YYYY-MM-DD
- **Status**: Ativo, Inativo, Afastado, Licença
- **Email**: Email institucional
- **Telefone**: Telefone no formato (XX) XXXXX-XXXX
- **Endereço**: Endereço completo
- **Cargo**: Função/posição (Estudante, Professor, Técnico, etc.)
- **Nível**: Escolaridade (Graduação, Mestrado, Doutorado, etc.)

### 1.2 Estruturas de Armazenamento Testadas
1. **Array Linear**: Armazenamento sequencial simples
2. **Hash Table por Matrícula**: Acesso O(1) por matrícula
3. **Hash Table por CPF**: Acesso O(1) por CPF
4. **Hash Table por Setor**: Agrupamento por departamento

## 2. Metodologia de Testes

### 2.1 Conjuntos de Dados
Foram gerados datasets sintéticos com os seguintes tamanhos:
- 1.000 registros
- 5.000 registros
- 10.000 registros
- 25.000 registros

### 2.2 Operações Avaliadas
1. **Inserção**: Adição de novos registros
2. **Busca por Matrícula (Linear)**: Busca sequencial
3. **Busca por Matrícula (Hash)**: Busca por índice hash
4. **Busca por CPF (Hash)**: Busca alternativa por CPF
5. **Busca por Nome (Parcial)**: Busca textual parcial
6. **Busca por Setor**: Listagem por departamento
7. **Busca por Faixa Salarial**: Consultas por range de valores

### 2.3 Métricas Coletadas
- Tempo de execução (em milissegundos)
- Uso de memória (em MB)
- Utilização de CPU
- Número de operações/comparações

## 3. Resultados de Performance

### 3.1 Performance de Inserção

| Dataset Size | Tempo Médio por Registro |
|-------------|-------------------------|
| 1.000       | 0.0004 ms              |
| 5.000       | 0.0005 ms              |
| 10.000      | 0.0005 ms              |
| 25.000      | 0.0006 ms              |

**Observações:**
- Inserção apresenta complexidade praticamente constante
- Overhead mínimo com aumento do dataset
- Sistema de hash tables mantém eficiência mesmo com datasets grandes

### 3.2 Performance de Busca por Matrícula

#### Comparação Hash vs Linear

| Dataset Size | Busca Hash (ms) | Busca Linear (ms) | Speedup |
|-------------|----------------|------------------|---------|
| 1.000       | 0.0002         | 0.0088          | 36.9x   |
| 5.000       | 0.0003         | 0.0864          | 255.9x  |
| 10.000      | 0.0004         | 0.0845          | 224.6x  |
| 25.000      | 0.0004         | 0.2314          | 545.9x  |

**Análise:**
- Hash table apresenta tempo **quase constante** independente do tamanho
- Busca linear degrada com O(n) conforme esperado
- **Speedup aumenta** com o tamanho do dataset, chegando a 545x para 25.000 registros

### 3.3 Performance por Tipo de Busca (Dataset 25.000 registros)

| Tipo de Busca              | Tempo Médio (ms) | Complexidade |
|---------------------------|------------------|--------------|
| Matrícula (Hash)          | 0.0004          | O(1)         |
| CPF (Hash)                | 0.0005          | O(1)         |
| Matrícula (Linear)        | 0.2314          | O(n)         |
| Nome (Parcial Linear)     | 2.1500          | O(n)         |
| Setor (Hash Agrupado)     | 0.0008          | O(1)         |
| Faixa Salarial (Linear)   | 1.8750          | O(n)         |

## 4. Análise de Consumo de Recursos

### 4.1 Utilização de Memória
- **Inserção**: Crescimento linear com número de registros
- **Hash Tables**: Overhead adicional de ~30-40% para índices
- **Pico de Memória**: Proporcional ao tamanho do dataset
- **Eficiência**: Excelente localidade de referência para buscas hash

### 4.2 Utilização de CPU
- **Inserção**: CPU utilization baixa (operações simples)
- **Busca Hash**: Mínima utilização (acesso direto)
- **Busca Linear**: CPU utilization proporcional ao tamanho da busca
- **Operações Complexas**: Buscas por nome e faixa salarial consomem mais CPU

### 4.3 Eficiência por Operação

#### Throughput (Operações por segundo)
- **Inserção**: ~2.000.000 registros/segundo
- **Busca Hash**: ~2.500.000 buscas/segundo
- **Busca Linear**: ~4.300 buscas/segundo (dataset 25k)

## 5. Cenários de Uso Prático

### 5.1 Sistema Acadêmico - Consultas Frequentes
**Caso:** Consulta de matrícula por funcionários da secretaria
- **Solução Recomendada**: Hash table por matrícula
- **Performance**: 0.0004 ms por consulta
- **Vantagem**: Tempo constante independente do crescimento da base

### 5.2 Sistema RH - Relatórios por Setor
**Caso:** Geração de folha de pagamento por departamento
- **Solução Recomendada**: Hash table agrupada por setor
- **Performance**: 0.0008 ms para localizar setor + tempo linear para listar
- **Vantagem**: Evita varredura completa da base

### 5.3 Sistema Financeiro - Consultas por Faixa Salarial
**Caso:** Análises de distribuição salarial
- **Limitação Atual**: Busca linear (1.875 ms para 25k registros)
- **Recomendação**: Implementar índice por faixa ou árvore balanceada
- **Melhoria Esperada**: Redução de O(n) para O(log n)

### 5.4 Sistema de Apoio - Busca por Nome
**Caso:** Localização de pessoa por nome parcial
- **Performance Atual**: 2.15 ms (busca linear)
- **Recomendação**: Implementar índice invertido ou trie
- **Aplicação**: Sistemas de atendimento e suporte

## 6. Recomendações de Arquitetura

### 6.1 Para Sistemas de Pequeno Porte (< 5.000 registros)
- **Estrutura**: Array linear com hash table para campos principais
- **Justificativa**: Simplicidade de implementação vs. performance
- **Custo-Benefício**: Excelente para a maioria das operações

### 6.2 Para Sistemas de Médio Porte (5.000 - 50.000 registros)
- **Estrutura**: Múltiplas hash tables por campo de busca frequente
- **Índices Recomendados**: Matrícula, CPF, Setor
- **Estratégia**: Índices secundários para consultas menos frequentes

### 6.3 Para Sistemas de Grande Porte (> 50.000 registros)
- **Estrutura**: Hash tables + estruturas auxiliares (árvores, índices compostos)
- **Considerações**: Particionamento por período/setor
- **Otimizações**: Cache de consultas frequentes, compressão de dados

## 7. Trade-offs Identificados

### 7.1 Memória vs. Performance
- **Hash Tables**: Consomem ~40% mais memória que arrays simples
- **Benefício**: Redução drástica no tempo de busca (500x+ speedup)
- **Conclusão**: Trade-off favorável para aplicações com buscas frequentes

### 7.2 Complexidade vs. Flexibilidade
- **Estruturas Simples**: Fáceis de implementar e manter
- **Estruturas Complexas**: Melhor performance para casos específicos
- **Recomendação**: Implementar gradualmente conforme necessidade

### 7.3 Tempo de Inserção vs. Tempo de Busca
- **Observação**: Tempo de inserção praticamente constante para todas as estruturas
- **Conclusão**: Hash tables não introduzem overhead significativo na inserção
- **Vantagem**: Otimização "gratuita" para buscas

## 8. Limitações do Estudo

### 8.1 Dados Sintéticos
- **Limitação**: Dados gerados podem não refletir padrões reais
- **Impacto**: Distribuição de buscas pode ser diferente na prática
- **Recomendação**: Validar com dados reais quando disponíveis

### 8.2 Ambiente de Teste
- **Contexto**: Testes em ambiente controlado, single-threaded
- **Considerações**: Performance pode variar com concorrência
- **Sugestão**: Testes de carga com múltiplos usuários simultâneos

### 8.3 Tipos de Consulta
- **Escopo**: Foco em consultas exatas e ranges simples
- **Não Avaliado**: Consultas complexas com JOINs, agregações
- **Expansão**: Avaliar performance com consultas SQL-like

## 9. Conclusões e Próximos Passos

### 9.1 Principais Descobertas
1. **Hash tables oferecem speedup excepcional** (36x a 545x) para buscas por chave
2. **Inserção mantém performance constante** independente da estrutura
3. **Overhead de memória é compensado** pelo ganho em tempo de resposta
4. **Escalabilidade excelente** para datasets de até 25.000 registros testados

### 9.2 Aplicabilidade Imediata
- **Sistemas Acadêmicos**: Implementar hash por matrícula como prioridade
- **Sistemas RH**: Adicionar índice por setor para relatórios
- **Sistemas de Atendimento**: Considerar otimizações para busca por nome

### 9.3 Trabalhos Futuros
1. **Avaliar estruturas híbridas** (B-trees, LSM-trees) para casos específicos
2. **Implementar cache inteligente** para consultas frequentes
3. **Testar com datasets maiores** (100k+ registros)
4. **Avaliar impacto de atualizações** frequentes nos índices
5. **Desenvolver métricas de qualidade de dados** e sua relação com performance

### 9.4 Retorno sobre Investimento
- **Implementação de Hash Tables**: Esforço baixo, retorno alto
- **Tempo de Desenvolvimento**: 1-2 semanas para implementação básica
- **Benefício Esperado**: Redução de 95%+ no tempo de resposta para buscas
- **Escalabilidade**: Suporta crescimento orgânico da base de dados

---

**Nota**: Este relatório baseia-se em experimentos controlados com dados sintéticos. Recomenda-se validação com dados reais e cenários específicos de cada aplicação antes da implementação em produção.