# Makefile para compilação do trabalho de estruturas de dados
# PUCPR - Fundamentos de Algoritmos e Estrutura de Dados

CXX = g++
CXXFLAGS = -std=c++14 -Wall -Wextra -O2
TARGET = trabalho_completo
SOURCE = trabalho_completo.cpp
CSV_FILES = experiment_results.csv experiment_details.csv

# Regra principal
all: $(TARGET)

# Compilação do executável
$(TARGET): $(SOURCE)
	$(CXX) $(CXXFLAGS) -o $(TARGET) $(SOURCE)
	@echo "✓ Compilação concluída com sucesso!"
	@echo "Execute: ./$(TARGET)"

# Executar experimentos
run: $(TARGET)
	@echo "Iniciando experimentos..."
	./$(TARGET)

# Compilação para debug
debug: CXXFLAGS += -g -DDEBUG
debug: $(TARGET)

# Compilação otimizada para release
release: CXXFLAGS += -O3 -DNDEBUG
release: $(TARGET)

# Limpeza dos arquivos gerados
clean:
	rm -f $(TARGET)
	rm -f $(CSV_FILES)
	@echo "✓ Arquivos limpos"

# Limpeza completa (inclui resultados)
clean-all: clean
	rm -rf plots/
	@echo "✓ Limpeza completa realizada"

# Verificar dependências
check:
	@echo "Verificando compilador..."
	@$(CXX) --version
	@echo "✓ Compilador C++ disponível"

# Executar com tempo
time-run: $(TARGET)
	@echo "Executando experimentos com medição de tempo..."
	time ./$(TARGET)

# Instalar dependências (se necessário)
install-deps:
	@echo "Este projeto não requer dependências externas em C++"
	@echo "Apenas compilador C++17 ou superior é necessário"

# Ajuda
help:
	@echo "Comandos disponíveis:"
	@echo "  make         - Compila o programa"
	@echo "  make run     - Compila e executa os experimentos"
	@echo "  make debug   - Compila versão de debug"
	@echo "  make release - Compila versão otimizada"
	@echo "  make clean   - Remove executável e CSVs"
	@echo "  make clean-all - Remove tudo (incluindo plots)"
	@echo "  make check   - Verifica dependências"
	@echo "  make time-run - Executa com medição de tempo"
	@echo "  make help    - Mostra esta ajuda"

.PHONY: all run debug release clean clean-all check time-run install-deps help