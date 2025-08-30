/*
================================================================================
ANÁLISE COMPARATIVA DE ESTRUTURAS DE DADOS - VERSÃO C++
PONTIFÍCIA UNIVERSIDADE CATÓLICA DO PARANÁ
PROGRAMA DE PÓS-GRADUAÇÃO EM INFORMÁTICA APLICADA
FUNDAMENTOS DE ALGORITMOS E ESTRUTURA DE DADOS
PROF. ANDRÉ GUSTAVO HOCHULI

Trabalho 01: Análise Comparativa de Estruturas de Dados
================================================================================

Este código implementa e compara diferentes estruturas de dados em C++:
- Arrays lineares (std::vector)
- Árvores de busca binária (BST)
- Árvores AVL (balanceadas)
- Tabelas hash com três funções diferentes

O objetivo é avaliar o desempenho em operações de inserção e busca,
considerando métricas como tempo de execução, uso de memória e iterações.

Compilação:
g++ -std=c++17 -O2 -o trabalho_completo trabalho_completo.cpp

Execução:
./trabalho_completo

================================================================================
*/

#include <iostream>
#include <vector>
#include <string>
#include <random>
#include <chrono>
#include <fstream>
#include <iomanip>
#include <algorithm>
#include <cmath>
#include <memory>
#include <sstream>
#include <unordered_map>
#include <unordered_set>
#include <iterator>
#include <sys/resource.h>

// ================================================================================
// SEÇÃO 1: ESTRUTURAS AUXILIARES E MÉTRICAS
// ================================================================================

// Função auxiliar para substituir std::sample (C++17)
template<typename InputIt, typename OutputIt, typename Distance, typename URBG>
OutputIt sample_records(InputIt first, InputIt last, OutputIt d_first,
                       Distance n, URBG&& g) {
    using difference_type = typename std::iterator_traits<InputIt>::difference_type;
    
    difference_type unsampled_sz = std::distance(first, last);
    difference_type sample_size = static_cast<difference_type>(n);
    
    for (sample_size = std::min(sample_size, unsampled_sz); sample_size != 0; ++first) {
        if (std::uniform_int_distribution<difference_type>(0, --unsampled_sz)(g) < sample_size) {
            *d_first++ = *first;
            --sample_size;
        }
    }
    return d_first;
}

struct Record {
    int matricula;
    std::string nome;
    double salario;
    int codigo_setor;
    
    Record(int mat, const std::string& n, double sal, int setor) 
        : matricula(mat), nome(n), salario(sal), codigo_setor(setor) {}
    
    bool operator==(const Record& other) const {
        return matricula == other.matricula;
    }
    
    bool operator<(const Record& other) const {
        return matricula < other.matricula;
    }
};

struct PerformanceMetrics {
    double execution_time = 0.0;
    double memory_usage_mb = 0.0;
    long iterations = 0;
    
    // Métricas específicas para árvores
    int tree_height = 0;
    
    // Métricas específicas para hash tables
    double load_factor = 0.0;
    double collision_rate = 0.0;
    double avg_chain_length = 0.0;
    int max_chain_length = 0;
};

class MetricsCollector {
private:
    std::chrono::high_resolution_clock::time_point start_time;
    long start_memory;
    
    long getCurrentMemoryUsage() {
        struct rusage usage;
        getrusage(RUSAGE_SELF, &usage);
        return usage.ru_maxrss; // Em KB no Linux, bytes no macOS
    }
    
public:
    void startMeasurement() {
        start_time = std::chrono::high_resolution_clock::now();
        start_memory = getCurrentMemoryUsage();
    }
    
    PerformanceMetrics stopMeasurement(long iterations = 0) {
        auto end_time = std::chrono::high_resolution_clock::now();
        long end_memory = getCurrentMemoryUsage();
        
        PerformanceMetrics metrics;
        metrics.execution_time = std::chrono::duration<double>(end_time - start_time).count();
        metrics.memory_usage_mb = (end_memory - start_memory) / 1024.0; // MB
        metrics.iterations = iterations;
        
        return metrics;
    }
};

class DataGenerator {
public:
    static std::vector<Record> generateRecords(int n, int seed = 42) {
        std::mt19937 gen(seed);
        std::uniform_int_distribution<int> matricula_dist(100000000, 999999999);
        std::uniform_real_distribution<double> salario_dist(2000.0, 20000.0);
        std::uniform_int_distribution<int> setor_dist(1, 100);
        
        std::vector<Record> records;
        std::unordered_set<int> used_matriculas;
        
        std::cout << "Gerando " << n << " registros fictícios..." << std::endl;
        
        for (int i = 0; i < n; ++i) {
            int matricula;
            do {
                matricula = matricula_dist(gen);
            } while (used_matriculas.count(matricula));
            used_matriculas.insert(matricula);
            
            std::string nome = "FUNC" + std::to_string(i);
            double salario = salario_dist(gen);
            int setor = setor_dist(gen);
            
            records.emplace_back(matricula, nome, salario, setor);
            
            if ((i + 1) % 10000 == 0) {
                std::cout << "  Progresso: " << (i + 1) << "/" << n << " registros..." << std::endl;
            }
        }
        
        std::cout << "✓ " << n << " registros gerados com sucesso" << std::endl;
        return records;
    }
};

// ================================================================================
// SEÇÃO 2: ARRAY LINEAR
// ================================================================================

class LinearArray {
private:
    std::vector<Record> data;
    mutable long iterations;
    
public:
    LinearArray() : iterations(0) {}
    
    long insert(const Record& record) {
        iterations = 1;
        data.push_back(record);
        return iterations;
    }
    
    std::pair<Record*, long> search(int matricula) {
        iterations = 0;
        for (auto& record : data) {
            iterations++;
            if (record.matricula == matricula) {
                return {&record, iterations};
            }
        }
        return {nullptr, iterations};
    }
    
    size_t size() const { return data.size(); }
    void clear() { data.clear(); iterations = 0; }
};

// ================================================================================
// SEÇÃO 3: ÁRVORE DE BUSCA BINÁRIA (BST)
// ================================================================================

class BSTNode {
public:
    Record record;
    std::unique_ptr<BSTNode> left;
    std::unique_ptr<BSTNode> right;
    
    BSTNode(const Record& rec) : record(rec), left(nullptr), right(nullptr) {}
};

class BinarySearchTree {
private:
    std::unique_ptr<BSTNode> root;
    mutable long iterations;
    size_t size_count;
    
    std::unique_ptr<BSTNode>& insertRecursive(std::unique_ptr<BSTNode>& node, const Record& record) {
        iterations++;
        
        if (!node) {
            node = std::make_unique<BSTNode>(record);
            return node;
        }
        
        if (record.matricula < node->record.matricula) {
            insertRecursive(node->left, record);
        } else if (record.matricula > node->record.matricula) {
            insertRecursive(node->right, record);
        }
        
        return node;
    }
    
    Record* searchRecursive(const std::unique_ptr<BSTNode>& node, int matricula) const {
        if (!node) return nullptr;
        
        iterations++;
        
        if (matricula == node->record.matricula) {
            return &node->record;
        } else if (matricula < node->record.matricula) {
            return searchRecursive(node->left, matricula);
        } else {
            return searchRecursive(node->right, matricula);
        }
    }
    
    int heightRecursive(const std::unique_ptr<BSTNode>& node) const {
        if (!node) return 0;
        return 1 + std::max(heightRecursive(node->left), heightRecursive(node->right));
    }
    
public:
    BinarySearchTree() : root(nullptr), iterations(0), size_count(0) {}
    
    long insert(const Record& record) {
        iterations = 0;
        insertRecursive(root, record);
        size_count++;
        return iterations;
    }
    
    std::pair<Record*, long> search(int matricula) {
        iterations = 0;
        Record* result = searchRecursive(root, matricula);
        return {result, iterations};
    }
    
    int height() const {
        return heightRecursive(root);
    }
    
    size_t size() const { return size_count; }
    void clear() { root = nullptr; iterations = 0; size_count = 0; }
};

// ================================================================================
// SEÇÃO 4: ÁRVORE AVL
// ================================================================================

class AVLNode {
public:
    Record record;
    std::unique_ptr<AVLNode> left;
    std::unique_ptr<AVLNode> right;
    int height;
    
    AVLNode(const Record& rec) : record(rec), left(nullptr), right(nullptr), height(1) {}
};

class AVLTree {
private:
    std::unique_ptr<AVLNode> root;
    mutable long iterations;
    size_t size_count;
    
    int getHeight(const std::unique_ptr<AVLNode>& node) const {
        return node ? node->height : 0;
    }
    
    int getBalance(const std::unique_ptr<AVLNode>& node) const {
        return node ? getHeight(node->left) - getHeight(node->right) : 0;
    }
    
    std::unique_ptr<AVLNode> rotateRight(std::unique_ptr<AVLNode> z) {
        iterations++;
        auto y = std::move(z->left);
        z->left = std::move(y->right);
        y->right = std::move(z);
        
        // Atualiza alturas
        y->right->height = 1 + std::max(getHeight(y->right->left), getHeight(y->right->right));
        y->height = 1 + std::max(getHeight(y->left), getHeight(y->right));
        
        return y;
    }
    
    std::unique_ptr<AVLNode> rotateLeft(std::unique_ptr<AVLNode> z) {
        iterations++;
        auto y = std::move(z->right);
        z->right = std::move(y->left);
        y->left = std::move(z);
        
        // Atualiza alturas
        y->left->height = 1 + std::max(getHeight(y->left->left), getHeight(y->left->right));
        y->height = 1 + std::max(getHeight(y->left), getHeight(y->right));
        
        return y;
    }
    
    std::unique_ptr<AVLNode> insertRecursive(std::unique_ptr<AVLNode> node, const Record& record) {
        iterations++;
        
        // Inserção normal BST
        if (!node) {
            return std::make_unique<AVLNode>(record);
        }
        
        if (record.matricula < node->record.matricula) {
            node->left = insertRecursive(std::move(node->left), record);
        } else if (record.matricula > node->record.matricula) {
            node->right = insertRecursive(std::move(node->right), record);
        } else {
            return node; // Duplicata não permitida
        }
        
        // Atualiza altura
        node->height = 1 + std::max(getHeight(node->left), getHeight(node->right));
        
        // Obtém fator de balanceamento
        int balance = getBalance(node);
        
        // Casos de rotação
        // Left Left
        if (balance > 1 && record.matricula < node->left->record.matricula) {
            return rotateRight(std::move(node));
        }
        
        // Right Right
        if (balance < -1 && record.matricula > node->right->record.matricula) {
            return rotateLeft(std::move(node));
        }
        
        // Left Right
        if (balance > 1 && record.matricula > node->left->record.matricula) {
            node->left = rotateLeft(std::move(node->left));
            return rotateRight(std::move(node));
        }
        
        // Right Left
        if (balance < -1 && record.matricula < node->right->record.matricula) {
            node->right = rotateRight(std::move(node->right));
            return rotateLeft(std::move(node));
        }
        
        return node;
    }
    
    Record* searchRecursive(const std::unique_ptr<AVLNode>& node, int matricula) const {
        if (!node) return nullptr;
        
        iterations++;
        
        if (matricula == node->record.matricula) {
            return &node->record;
        } else if (matricula < node->record.matricula) {
            return searchRecursive(node->left, matricula);
        } else {
            return searchRecursive(node->right, matricula);
        }
    }
    
public:
    AVLTree() : root(nullptr), iterations(0), size_count(0) {}
    
    long insert(const Record& record) {
        iterations = 0;
        root = insertRecursive(std::move(root), record);
        size_count++;
        return iterations;
    }
    
    std::pair<Record*, long> search(int matricula) {
        iterations = 0;
        Record* result = searchRecursive(root, matricula);
        return {result, iterations};
    }
    
    int height() const {
        return getHeight(root);
    }
    
    size_t size() const { return size_count; }
    void clear() { root = nullptr; iterations = 0; size_count = 0; }
};

// ================================================================================
// SEÇÃO 5: TABELA HASH
// ================================================================================

class HashTable {
private:
    std::vector<std::vector<Record>> table;
    std::string hash_function_name;
    mutable long iterations;
    int collisions;
    int total_elements;
    int table_size;
    
    int hashDivision(int key) const {
        return key % table_size;
    }
    
    int hashMultiplication(int key) const {
        const double A = 0.6180339887; // (√5 - 1) / 2
        double temp = key * A;
        temp = temp - std::floor(temp); // parte fracionária
        return static_cast<int>(table_size * temp);
    }
    
    int hashFolding(int key) const {
        std::string key_str = std::to_string(key);
        int total = 0;
        int chunk_size = 3;
        
        for (size_t i = 0; i < key_str.length(); i += chunk_size) {
            std::string chunk = key_str.substr(i, chunk_size);
            total += std::stoi(chunk);
        }
        
        return total % table_size;
    }
    
    int hashFunction(int key) const {
        if (hash_function_name == "division") {
            return hashDivision(key);
        } else if (hash_function_name == "multiplication") {
            return hashMultiplication(key);
        } else if (hash_function_name == "folding") {
            return hashFolding(key);
        } else {
            return hashDivision(key);
        }
    }
    
public:
    HashTable(int size, const std::string& hash_func) 
        : table(size), hash_function_name(hash_func), iterations(0), 
          collisions(0), total_elements(0), table_size(size) {}
    
    long insert(const Record& record) {
        iterations = 1;
        int index = hashFunction(record.matricula);
        
        // Verifica colisão
        if (!table[index].empty()) {
            collisions++;
        }
        
        // Verifica se já existe
        for (const auto& existing : table[index]) {
            iterations++;
            if (existing.matricula == record.matricula) {
                return iterations;
            }
        }
        
        table[index].push_back(record);
        total_elements++;
        return iterations;
    }
    
    std::pair<Record*, long> search(int matricula) {
        iterations = 1;
        int index = hashFunction(matricula);
        
        for (auto& record : table[index]) {
            iterations++;
            if (record.matricula == matricula) {
                return {&record, iterations};
            }
        }
        
        return {nullptr, iterations};
    }
    
    double getLoadFactor() const {
        return static_cast<double>(total_elements) / table_size;
    }
    
    double getCollisionRate() const {
        return total_elements == 0 ? 0.0 : static_cast<double>(collisions) / total_elements;
    }
    
    double getAverageChainLength() const {
        int non_empty_buckets = 0;
        for (const auto& bucket : table) {
            if (!bucket.empty()) non_empty_buckets++;
        }
        return non_empty_buckets == 0 ? 0.0 : static_cast<double>(total_elements) / non_empty_buckets;
    }
    
    int getMaxChainLength() const {
        int max_length = 0;
        for (const auto& bucket : table) {
            max_length = std::max(max_length, static_cast<int>(bucket.size()));
        }
        return max_length;
    }
    
    size_t size() const { return total_elements; }
    
    void clear() {
        for (auto& bucket : table) {
            bucket.clear();
        }
        iterations = 0;
        collisions = 0;
        total_elements = 0;
    }
};

// ================================================================================
// SEÇÃO 6: SISTEMA DE EXPERIMENTOS
// ================================================================================

struct ExperimentResult {
    std::string structure_name;
    int data_size;
    std::string operation;
    std::vector<PerformanceMetrics> rounds;
    std::unordered_map<std::string, std::string> parameters;
    
    PerformanceMetrics getStatistics() const {
        if (rounds.empty()) return PerformanceMetrics();
        
        PerformanceMetrics stats;
        double sum_time = 0, sum_memory = 0;
        long sum_iterations = 0;
        
        for (const auto& round : rounds) {
            sum_time += round.execution_time;
            sum_memory += round.memory_usage_mb;
            sum_iterations += round.iterations;
        }
        
        stats.execution_time = sum_time / rounds.size();
        stats.memory_usage_mb = sum_memory / rounds.size();
        stats.iterations = sum_iterations / rounds.size();
        
        return stats;
    }
};

class ExperimentRunner {
private:
    std::vector<int> data_sizes;
    int num_rounds;
    MetricsCollector collector;
    std::vector<ExperimentResult> results;
    std::mt19937 gen;
    
    void runLinearArrayExperiment(const std::vector<Record>& data, int size) {
        std::cout << "  Array Linear..." << std::endl;
        
        ExperimentResult insert_result, search_result;
        insert_result.structure_name = search_result.structure_name = "LinearArray";
        insert_result.data_size = search_result.data_size = size;
        insert_result.operation = "insert";
        search_result.operation = "search";
        
        for (int round = 0; round < num_rounds; ++round) {
            // Inserção
            LinearArray array;
            collector.startMeasurement();
            
            long total_iterations = 0;
            for (const auto& record : data) {
                total_iterations += array.insert(record);
            }
            
            PerformanceMetrics insert_metrics = collector.stopMeasurement(total_iterations);
            insert_result.rounds.push_back(insert_metrics);
            
            // Busca
            std::vector<Record> search_sample;
            sample_records(data.begin(), data.end(), std::back_inserter(search_sample), 
                          std::min(1000, static_cast<int>(data.size())), gen);
            
            collector.startMeasurement();
            total_iterations = 0;
            
            for (const auto& record : search_sample) {
                auto result = array.search(record.matricula);
                total_iterations += result.second;
            }
            
            PerformanceMetrics search_metrics = collector.stopMeasurement(total_iterations / search_sample.size());
            search_result.rounds.push_back(search_metrics);
        }
        
        results.push_back(insert_result);
        results.push_back(search_result);
    }
    
    void runBSTExperiment(const std::vector<Record>& data, int size) {
        std::cout << "  Árvore de Busca Binária (BST)..." << std::endl;
        
        ExperimentResult insert_result, search_result;
        insert_result.structure_name = search_result.structure_name = "BST";
        insert_result.data_size = search_result.data_size = size;
        insert_result.operation = "insert";
        search_result.operation = "search";
        insert_result.parameters["balanced"] = "false";
        search_result.parameters["balanced"] = "false";
        
        for (int round = 0; round < num_rounds; ++round) {
            // Embaralha dados
            std::vector<Record> shuffled_data = data;
            std::shuffle(shuffled_data.begin(), shuffled_data.end(), gen);
            
            // Inserção
            BinarySearchTree bst;
            collector.startMeasurement();
            
            long total_iterations = 0;
            for (const auto& record : shuffled_data) {
                total_iterations += bst.insert(record);
            }
            
            PerformanceMetrics insert_metrics = collector.stopMeasurement(total_iterations);
            insert_metrics.tree_height = bst.height();
            insert_result.rounds.push_back(insert_metrics);
            
            // Busca
            std::vector<Record> search_sample;
            sample_records(data.begin(), data.end(), std::back_inserter(search_sample), 
                          std::min(1000, static_cast<int>(data.size())), gen);
            
            collector.startMeasurement();
            total_iterations = 0;
            
            for (const auto& record : search_sample) {
                auto result = bst.search(record.matricula);
                total_iterations += result.second;
            }
            
            PerformanceMetrics search_metrics = collector.stopMeasurement(total_iterations / search_sample.size());
            search_result.rounds.push_back(search_metrics);
        }
        
        results.push_back(insert_result);
        results.push_back(search_result);
    }
    
    void runAVLExperiment(const std::vector<Record>& data, int size) {
        std::cout << "  Árvore AVL..." << std::endl;
        
        ExperimentResult insert_result, search_result;
        insert_result.structure_name = search_result.structure_name = "AVL";
        insert_result.data_size = search_result.data_size = size;
        insert_result.operation = "insert";
        search_result.operation = "search";
        insert_result.parameters["balanced"] = "true";
        search_result.parameters["balanced"] = "true";
        
        for (int round = 0; round < num_rounds; ++round) {
            // Embaralha dados
            std::vector<Record> shuffled_data = data;
            std::shuffle(shuffled_data.begin(), shuffled_data.end(), gen);
            
            // Inserção
            AVLTree avl;
            collector.startMeasurement();
            
            long total_iterations = 0;
            for (const auto& record : shuffled_data) {
                total_iterations += avl.insert(record);
            }
            
            PerformanceMetrics insert_metrics = collector.stopMeasurement(total_iterations);
            insert_metrics.tree_height = avl.height();
            insert_result.rounds.push_back(insert_metrics);
            
            // Busca
            std::vector<Record> search_sample;
            sample_records(data.begin(), data.end(), std::back_inserter(search_sample), 
                          std::min(1000, static_cast<int>(data.size())), gen);
            
            collector.startMeasurement();
            total_iterations = 0;
            
            for (const auto& record : search_sample) {
                auto result = avl.search(record.matricula);
                total_iterations += result.second;
            }
            
            PerformanceMetrics search_metrics = collector.stopMeasurement(total_iterations / search_sample.size());
            search_result.rounds.push_back(search_metrics);
        }
        
        results.push_back(insert_result);
        results.push_back(search_result);
    }
    
    void runHashTableExperiment(const std::vector<Record>& data, int size, int m_size, const std::string& hash_func) {
        std::cout << "  • M=" << m_size << ", função=" << hash_func << std::endl;
        
        ExperimentResult insert_result, search_result;
        insert_result.structure_name = search_result.structure_name = "HashTable";
        insert_result.data_size = search_result.data_size = size;
        insert_result.operation = "insert";
        search_result.operation = "search";
        insert_result.parameters["M"] = std::to_string(m_size);
        insert_result.parameters["hash_function"] = hash_func;
        search_result.parameters["M"] = std::to_string(m_size);
        search_result.parameters["hash_function"] = hash_func;
        
        for (int round = 0; round < num_rounds; ++round) {
            // Inserção
            HashTable hash_table(m_size, hash_func);
            collector.startMeasurement();
            
            long total_iterations = 0;
            for (const auto& record : data) {
                total_iterations += hash_table.insert(record);
            }
            
            PerformanceMetrics insert_metrics = collector.stopMeasurement(total_iterations);
            insert_metrics.load_factor = hash_table.getLoadFactor();
            insert_metrics.collision_rate = hash_table.getCollisionRate();
            insert_metrics.avg_chain_length = hash_table.getAverageChainLength();
            insert_metrics.max_chain_length = hash_table.getMaxChainLength();
            insert_result.rounds.push_back(insert_metrics);
            
            // Busca
            std::vector<Record> search_sample;
            sample_records(data.begin(), data.end(), std::back_inserter(search_sample), 
                          std::min(1000, static_cast<int>(data.size())), gen);
            
            collector.startMeasurement();
            total_iterations = 0;
            
            for (const auto& record : search_sample) {
                auto result = hash_table.search(record.matricula);
                total_iterations += result.second;
            }
            
            PerformanceMetrics search_metrics = collector.stopMeasurement(total_iterations / search_sample.size());
            search_result.rounds.push_back(search_metrics);
        }
        
        results.push_back(insert_result);
        results.push_back(search_result);
    }
    
public:
    ExperimentRunner(const std::vector<int>& sizes, int rounds) 
        : data_sizes(sizes), num_rounds(rounds), gen(42) {}
    
    void runAllExperiments() {
        std::cout << "\n" << std::string(80, '=') << std::endl;
        std::cout << std::setw(40) << "INICIANDO EXPERIMENTOS" << std::endl;
        std::cout << std::string(80, '=') << std::endl;
        
        for (int size : data_sizes) {
            std::cout << "\n" << std::string(60, '=') << std::endl;
            std::cout << std::setw(35) << ("Tamanho do Dataset: " + std::to_string(size) + " registros") << std::endl;
            std::cout << std::string(60, '=') << std::endl;
            
            // Gera dados para este tamanho
            auto data = DataGenerator::generateRecords(size, 42);
            
            // Executa experimentos
            runLinearArrayExperiment(data, size);
            runBSTExperiment(data, size);
            runAVLExperiment(data, size);
            
            // Hash Table com diferentes M e funções
            std::cout << "\n→ Tabela Hash..." << std::endl;
            for (int m_size : {100, 1000, 5000}) {
                for (const std::string& hash_func : {"division", "multiplication", "folding"}) {
                    runHashTableExperiment(data, size, m_size, hash_func);
                }
            }
        }
    }
    
    void saveResults(const std::string& filename = "experiment_results.csv", 
                    const std::string& detailed_filename = "experiment_details.csv") {
        
        // Salva arquivo resumo
        std::ofstream file(filename);
        file << "structure,data_size,operation,mean_time,memory_usage_mb,mean_iterations,";
        file << "hash_table_size,hash_function,load_factor,collision_rate,avg_chain_length,max_chain_length,balanced,tree_height\n";
        
        for (const auto& result : results) {
            PerformanceMetrics stats = result.getStatistics();
            
            file << result.structure_name << ",";
            file << result.data_size << ",";
            file << result.operation << ",";
            file << std::fixed << std::setprecision(6) << stats.execution_time << ",";
            file << std::fixed << std::setprecision(3) << stats.memory_usage_mb << ",";
            file << stats.iterations << ",";
            
            // Parâmetros específicos
            if (result.structure_name == "HashTable") {
                file << result.parameters.at("M") << ",";
                file << result.parameters.at("hash_function") << ",";
                if (!result.rounds.empty()) {
                    file << result.rounds[0].load_factor << ",";
                    file << result.rounds[0].collision_rate << ",";
                    file << result.rounds[0].avg_chain_length << ",";
                    file << result.rounds[0].max_chain_length << ",";
                } else {
                    file << "0,0,0,0,";
                }
                file << ",";
            } else {
                file << ",,,,,,,";
                if (result.structure_name == "BST" || result.structure_name == "AVL") {
                    file << result.parameters.at("balanced") << ",";
                    if (!result.rounds.empty()) {
                        file << result.rounds[0].tree_height;
                    }
                } else {
                    file << ",";
                }
            }
            file << "\n";
        }
        
        // Salva arquivo detalhado
        std::ofstream detailed_file(detailed_filename);
        detailed_file << "structure,data_size,operation,round,execution_time,memory_usage_mb,iterations,";
        detailed_file << "hash_table_size,hash_function,load_factor,collision_rate,avg_chain_length,max_chain_length,balanced,tree_height\n";
        
        for (const auto& result : results) {
            for (size_t i = 0; i < result.rounds.size(); ++i) {
                const auto& round = result.rounds[i];
                
                detailed_file << result.structure_name << ",";
                detailed_file << result.data_size << ",";
                detailed_file << result.operation << ",";
                detailed_file << (i + 1) << ",";
                detailed_file << std::fixed << std::setprecision(6) << round.execution_time << ",";
                detailed_file << std::fixed << std::setprecision(3) << round.memory_usage_mb << ",";
                detailed_file << round.iterations << ",";
                
                // Parâmetros específicos
                if (result.structure_name == "HashTable") {
                    detailed_file << result.parameters.at("M") << ",";
                    detailed_file << result.parameters.at("hash_function") << ",";
                    detailed_file << round.load_factor << ",";
                    detailed_file << round.collision_rate << ",";
                    detailed_file << round.avg_chain_length << ",";
                    detailed_file << round.max_chain_length << ",";
                    detailed_file << ",";
                } else {
                    detailed_file << ",,,,,,,";
                    if (result.structure_name == "BST" || result.structure_name == "AVL") {
                        detailed_file << result.parameters.at("balanced") << ",";
                        detailed_file << round.tree_height;
                    } else {
                        detailed_file << ",";
                    }
                }
                detailed_file << "\n";
            }
        }
        
        std::cout << "\n✓ Resultados salvos em:" << std::endl;
        std::cout << "  • " << filename << " - Resumo estatístico" << std::endl;
        std::cout << "  • " << detailed_filename << " - Dados detalhados por rodada" << std::endl;
    }
};

// ================================================================================
// SEÇÃO 7: FUNÇÃO PRINCIPAL
// ================================================================================

void printHeader() {
    std::cout << std::string(80, '=') << std::endl;
    std::cout << std::setw(50) << "ANÁLISE COMPARATIVA DE ESTRUTURAS DE DADOS" << std::endl;
    std::cout << std::setw(35) << "PUCPR - Fundamentos de Algoritmos" << std::endl;
    std::cout << std::string(80, '=') << std::endl;
    std::cout << "\nEstruturas avaliadas:" << std::endl;
    std::cout << "  1. Array Linear" << std::endl;
    std::cout << "  2. Árvore de Busca Binária (BST)" << std::endl;
    std::cout << "  3. Árvore AVL (BST Balanceada)" << std::endl;
    std::cout << "  4. Tabela Hash (3 funções, múltiplos M)" << std::endl;
    std::cout << "\nTamanhos de dados: 1.000, 5.000, 10.000 registros" << std::endl;
    std::cout << "Rodadas por experimento: 5" << std::endl;
    std::cout << std::string(80, '-') << std::endl;
}

int main() {
    try {
        printHeader();
        
        // Configuração dos experimentos
        std::vector<int> data_sizes = {1000, 5000, 10000};
        int num_rounds = 5;
        
        // Cria executor de experimentos
        ExperimentRunner runner(data_sizes, num_rounds);
        
        // Executa experimentos
        std::cout << "\nIniciando experimentos..." << std::endl;
        std::cout << "(Isso pode levar alguns minutos...)" << std::endl;
        
        runner.runAllExperiments();
        
        // Salva resultados
        runner.saveResults();
        
        std::cout << "\n" << std::string(80, '=') << std::endl;
        std::cout << std::setw(45) << "EXPERIMENTO CONCLUÍDO COM SUCESSO" << std::endl;
        std::cout << std::string(80, '=') << std::endl;
        std::cout << "\nArquivos gerados:" << std::endl;
        std::cout << "  • experiment_results.csv - Resumo estatístico" << std::endl;
        std::cout << "  • experiment_details.csv - Dados detalhados" << std::endl;
        std::cout << "\nMétricas coletadas:" << std::endl;
        std::cout << "  • Tempo de processamento (alta precisão)" << std::endl;
        std::cout << "  • Uso de memória (MB)" << std::endl;
        std::cout << "  • Número de iterações" << std::endl;
        std::cout << "\nPara executar novamente:" << std::endl;
        std::cout << "  ./trabalho_completo" << std::endl;
        
    } catch (const std::exception& e) {
        std::cerr << "\nErro durante execução: " << e.what() << std::endl;
        return 1;
    }
    
    return 0;
}