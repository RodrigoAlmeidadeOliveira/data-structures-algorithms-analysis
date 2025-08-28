#!/usr/bin/env python3
"""
Análise Comparativa de Estruturas de Dados
PUCPR - Fundamentos de Algoritmos e Estrutura de Dados
Autor: Sistema de Análise de Estruturas de Dados
"""

import sys
import os
import json
import math
import pandas as pd
import matplotlib.pyplot as plt
from tabulate import tabulate
from experiments import ExperimentRunner
from analysis import ResultAnalyzer


def print_header():
    print("=" * 80)
    print(" ANÁLISE COMPARATIVA DE ESTRUTURAS DE DADOS ".center(80))
    print("=" * 80)
    print("\nEstruturas avaliadas:")
    print("  1. Array Linear")
    print("  2. Árvore de Busca Binária (BST)")
    print("  3. Árvore AVL (BST Balanceada)")
    print("  4. Tabela Hash (3 funções, múltiplos M)")
    print("\nTamanhos de dados: 10.000, 50.000, 100.000 registros")
    print("Rodadas por experimento: 5")
    print("-" * 80)


def print_summary_table(results):
    print("\n" + "=" * 80)
    print(" RESUMO DOS RESULTADOS ".center(80))
    print("=" * 80)

    summary_data = []
    for result in results:
        stats = result.get_statistics()
        row = {
            'Estrutura': result.structure_name,
            'N': result.data_size,
            'Operação': result.operation,
            'Tempo Médio (s)': f"{stats.get('mean_time', 0):.6f}",
            'Desvio Tempo': f"{stats.get('std_time', 0):.6f}",
            'Iterações Médias': f"{stats.get('mean_iterations', 0):.1f}"
        }
        if result.structure_name == "HashTable":
            row['Parâmetros'] = f"M={result.parameters.get('M', '?')}, {result.parameters.get('hash_function', '?')}"
        elif result.structure_name in ["BST", "AVL"]:
            row['Parâmetros'] = f"balanced={result.parameters.get('balanced', False)}"
        else:
            row['Parâmetros'] = "-"
        summary_data.append(row)

    df = pd.DataFrame(summary_data)
    for operation in ['insert', 'search']:
        print(f"\n### Operação: {operation.upper()} ###")
        op_df = df[df['Operação'] == operation]
        if not op_df.empty:
            print(tabulate(op_df, headers='keys', tablefmt='grid', showindex=False))


def print_hash_analysis(results):
    print("\n" + "=" * 80)
    print(" ANÁLISE ESPECÍFICA - TABELA HASH ".center(80))
    print("=" * 80)

    hash_results = [r for r in results if r.structure_name == "HashTable" and r.operation == "insert"]
    if not hash_results:
        return

    analysis_data = []
    for result in hash_results:
        metrics = getattr(result, "metrics", {}) or {}
        analysis_data.append({
            'N': result.data_size,
            'M': result.parameters.get('M', None),
            'Função Hash': result.parameters.get('hash_function', None),
            'Load Factor': f"{metrics.get('avg_load_factor', 0):.3f}",
            'Taxa Colisão': f"{metrics.get('avg_collision_rate', 0):.3f}",
            'Comp. Médio Cadeia': f"{metrics.get('avg_avg_chain_length', 0):.2f}",
            'Comp. Máx. Cadeia': f"{metrics.get('avg_max_chain_length', 0):.0f}"
        })

    df = pd.DataFrame(analysis_data)
    print(tabulate(df, headers='keys', tablefmt='grid', showindex=False))


def print_tree_analysis(results):
    print("\n" + "=" * 80)
    print(" ANÁLISE ESPECÍFICA - ÁRVORES ".center(80))
    print("=" * 80)

    tree_results = [r for r in results if r.structure_name in ["BST", "AVL"] and r.operation == "insert"]
    if not tree_results:
        return

    analysis_data = []
    for result in tree_results:
        metrics = getattr(result, "metrics", {}) or {}
        analysis_data.append({
            'Estrutura': result.structure_name,
            'N': result.data_size,
            'Altura Média': f"{metrics.get('avg_height', 0):.1f}",
            'Iterações Inserção': f"{metrics.get('avg_iterations', 0):.1f}",
            'Tempo Inserção (s)': f"{result.get_statistics().get('mean_time', 0):.6f}"
        })

    df = pd.DataFrame(analysis_data)
    print(tabulate(df, headers='keys', tablefmt='grid', showindex=False))


# =========================
#   GERAÇÃO DE GRÁFICOS
# =========================

def _results_to_dataframe(results) -> pd.DataFrame:
    """Converte a lista de resultados em um DataFrame plano com colunas úteis."""
    rows = []
    for r in results:
        stats = r.get_statistics()
        params = getattr(r, "parameters", {}) or {}
        metrics = getattr(r, "metrics", {}) or {}

        rows.append({
            "structure": r.structure_name,
            "operation": r.operation,
            "N": r.data_size,
            "mean_time_s": stats.get("mean_time", 0.0),
            "std_time_s": stats.get("std_time", 0.0),
            "mean_iterations": stats.get("mean_iterations", 0.0),
            # parâmetros comuns
            "M": params.get("M"),
            "hash_function": params.get("hash_function"),
            "balanced": params.get("balanced"),
            # métricas específicas
            "avg_load_factor": metrics.get("avg_load_factor"),
            "avg_collision_rate": metrics.get("avg_collision_rate"),
            "avg_avg_chain_length": metrics.get("avg_avg_chain_length"),
            "avg_max_chain_length": metrics.get("avg_max_chain_length"),
            "avg_height": metrics.get("avg_height"),
            "avg_iterations_metric": metrics.get("avg_iterations")
        })
    df = pd.DataFrame(rows)
    return df


def _ensure_plots_dir(path="plots"):
    os.makedirs(path, exist_ok=True)
    return path


def _save_and_show(fig, filepath: str):
    fig.tight_layout()
    fig.savefig(filepath, bbox_inches="tight")
    plt.show()
    plt.close(fig)


def plot_summary(df: pd.DataFrame, outdir="plots"):
    """Gráficos de resumo comparando estruturas por operação."""
    for op in sorted(df["operation"].dropna().unique()):
        op_df = df[df["operation"] == op].copy()
        if op_df.empty:
            continue

        # Tempo médio por estrutura ao variar N
        fig, ax = plt.subplots(figsize=(8, 5))
        for struct in sorted(op_df["structure"].dropna().unique()):
            s_df = op_df[op_df["structure"] == struct].sort_values("N")
            ax.plot(s_df["N"], s_df["mean_time_s"], marker="o", label=struct)
        ax.set_title(f"Resumo: Tempo médio por estrutura (operação: {op})")
        ax.set_xlabel("Tamanho N")
        ax.set_ylabel("Tempo médio (s)")
        ax.legend()
        _save_and_show(fig, os.path.join(outdir, f"resumo_tempo_{op}.png"))

        # Iterações médias por estrutura
        fig, ax = plt.subplots(figsize=(8, 5))
        for struct in sorted(op_df["structure"].dropna().unique()):
            s_df = op_df[op_df["structure"] == struct].sort_values("N")
            ax.plot(s_df["N"], s_df["mean_iterations"], marker="s", label=struct)
        ax.set_title(f"Resumo: Iterações médias por estrutura (operação: {op})")
        ax.set_xlabel("Tamanho N")
        ax.set_ylabel("Iterações médias")
        ax.legend()
        _save_and_show(fig, os.path.join(outdir, f"resumo_iter_{op}.png"))


def plot_hash(df: pd.DataFrame, outdir="plots"):
    """Gráficos exclusivos da HashTable: tempo, load factor, colisões e tamanho de cadeia."""
    h = df[(df["structure"] == "HashTable") & (df["operation"] == "insert")].copy()
    if h.empty:
        return
    # Por função hash, séries separadas por M
    for func in sorted(h["hash_function"].dropna().unique()):
        fdf = h[h["hash_function"] == func]
        # Tempo por N (linhas separadas por M)
        fig, ax = plt.subplots(figsize=(8, 5))
        for M in sorted(fdf["M"].dropna().unique()):
            mdf = fdf[fdf["M"] == M].sort_values("N")
            ax.plot(mdf["N"], mdf["mean_time_s"], marker="o", label=f"M={M}")
        ax.set_title(f"Hash ({func}): Tempo médio vs N (inserção)")
        ax.set_xlabel("Tamanho N")
        ax.set_ylabel("Tempo médio (s)")
        ax.legend(title="Tamanho da Tabela")
        _save_and_show(fig, os.path.join(outdir, f"hash_{func}_tempo.png"))

        # Load factor vs N
        fig, ax = plt.subplots(figsize=(8, 5))
        for M in sorted(fdf["M"].dropna().unique()):
            mdf = fdf[fdf["M"] == M].sort_values("N")
            ax.plot(mdf["N"], mdf["avg_load_factor"], marker="s", label=f"M={M}")
        ax.set_title(f"Hash ({func}): Load factor vs N (inserção)")
        ax.set_xlabel("Tamanho N")
        ax.set_ylabel("Load factor médio")
        ax.legend(title="Tamanho da Tabela")
        _save_and_show(fig, os.path.join(outdir, f"hash_{func}_loadfactor.png"))

        # Taxa de colisão vs N
        if fdf["avg_collision_rate"].notna().any():
            fig, ax = plt.subplots(figsize=(8, 5))
            for M in sorted(fdf["M"].dropna().unique()):
                mdf = fdf[fdf["M"] == M].sort_values("N")
                ax.plot(mdf["N"], mdf["avg_collision_rate"], marker="^", label=f"M={M}")
            ax.set_title(f"Hash ({func}): Taxa de colisão vs N (inserção)")
            ax.set_xlabel("Tamanho N")
            ax.set_ylabel("Taxa de colisão média")
            ax.legend(title="Tamanho da Tabela")
            _save_and_show(fig, os.path.join(outdir, f"hash_{func}_colisoes.png"))

        # Comprimento médio e máximo de cadeias vs N (se houver)
        if fdf["avg_avg_chain_length"].notna().any():
            fig, ax = plt.subplots(figsize=(8, 5))
            for M in sorted(fdf["M"].dropna().unique()):
                mdf = fdf[fdf["M"] == M].sort_values("N")
                ax.plot(mdf["N"], mdf["avg_avg_chain_length"], marker="o", label=f"Médio | M={M}")
                if mdf["avg_max_chain_length"].notna().any():
                    ax.plot(mdf["N"], mdf["avg_max_chain_length"], marker="x", linestyle="--", label=f"Máx | M={M}")
            ax.set_title(f"Hash ({func}): Comprimento de cadeias vs N (inserção)")
            ax.set_xlabel("Tamanho N")
            ax.set_ylabel("Comprimento das cadeias")
            ax.legend()
            _save_and_show(fig, os.path.join(outdir, f"hash_{func}_cadeias.png"))


def plot_trees(df: pd.DataFrame, outdir="plots"):
    """Gráficos exclusivos de BST e AVL: tempo, iterações, altura vs N."""
    for struct in ["BST", "AVL"]:
        sdf = df[(df["structure"] == struct) & (df["operation"] == "insert")].copy()
        if sdf.empty:
            continue
        sdf = sdf.sort_values("N")

        # Tempo médio vs N
        fig, ax = plt.subplots(figsize=(8, 5))
        ax.plot(sdf["N"], sdf["mean_time_s"], marker="o")
        ax.set_title(f"{struct}: Tempo médio vs N (inserção)")
        ax.set_xlabel("Tamanho N")
        ax.set_ylabel("Tempo médio (s)")
        _save_and_show(fig, os.path.join(outdir, f"{struct.lower()}_tempo.png"))

        # Iterações médias vs N
        fig, ax = plt.subplots(figsize=(8, 5))
        ax.plot(sdf["N"], sdf["mean_iterations"], marker="s")
        ax.set_title(f"{struct}: Iterações médias vs N (inserção)")
        ax.set_xlabel("Tamanho N")
        ax.set_ylabel("Iterações médias")
        _save_and_show(fig, os.path.join(outdir, f"{struct.lower()}_iteracoes.png"))

        # Altura média vs N (se disponível)
        if sdf["avg_height"].notna().any():
            fig, ax = plt.subplots(figsize=(8, 5))
            ax.plot(sdf["N"], sdf["avg_height"], marker="^")
            ax.set_title(f"{struct}: Altura média vs N (inserção)")
            ax.set_xlabel("Tamanho N")
            ax.set_ylabel("Altura média")
            _save_and_show(fig, os.path.join(outdir, f"{struct.lower()}_altura.png"))


def _complexity_model(structure: str, operation: str):
    """
    Define a forma teórica esperada apenas para fins de overlay:
    - Array Linear: insert O(n), search O(n)
    - BST: insert/search O(log n) (média)
    - AVL: insert/search O(log n)
    - HashTable: insert/search O(1) (média)
    """
    s = (structure or "").lower()
    op = (operation or "").lower()
    if "hash" in s:
        return "O(1)"
    if "avl" in s or "bst" in s:
        return "O(log n)"
    if "array" in s:
        return "O(n)"
    # fallback conservador
    return "O(n)"


def plot_complexity_overlay(df: pd.DataFrame, outdir="plots"):
    """
    Para cada combinação estrutura-operação, plota a curva experimental (tempo médio vs N)
    e sobrepõe uma curva teórica reescalada (O(1), O(log n) ou O(n)) para comparação visual.
    """
    combos = df[["structure", "operation"]].drop_duplicates()
    for _, row in combos.iterrows():
        struct, op = row["structure"], row["operation"]
        sdf = df[(df["structure"] == struct) & (df["operation"] == op)].dropna(subset=["N", "mean_time_s"]).sort_values("N")
        if sdf.empty or len(sdf) < 2:
            continue

        model = _complexity_model(struct, op)

        # Curva teórica reescalada com base no último ponto
        Ns = sdf["N"].values
        Ts = sdf["mean_time_s"].values
        Nmax, Tmax = Ns[-1], Ts[-1]

        if model == "O(1)":
            theo = [Tmax for _ in Ns]
        elif model == "O(log n)":
            # log2(n), reescala para bater no último ponto
            logs = [math.log2(n) if n > 1 else 1.0 for n in Ns]
            scale = Tmax / logs[-1] if logs[-1] != 0 else 1.0
            theo = [scale * v for v in logs]
        else:  # "O(n)" (fallback)
            scale = Tmax / Nmax if Nmax != 0 else 1.0
            theo = [scale * n for n in Ns]

        fig, ax = plt.subplots(figsize=(8, 5))
        ax.plot(Ns, Ts, marker="o", label=f"{struct} medido ({op})")
        ax.plot(Ns, theo, linestyle="--", label=f"{model} (overlay)")
        ax.set_title(f"Complexidade experimental vs teórica — {struct} [{op}]")
        ax.set_xlabel("Tamanho N")
        ax.set_ylabel("Tempo médio (s)")
        ax.legend()
        _save_and_show(fig, os.path.join(outdir, f"complexidade_{struct.lower()}_{op}.png"))


def generate_all_plots(results):
    """Pipeline de gráficos com dados reais gerados pelos experimentos."""
    outdir = _ensure_plots_dir("plots")
    df = _results_to_dataframe(results)

    # 1) Resumo (todas as estruturas) — por operação
    plot_summary(df, outdir=outdir)

    # 2) HashTable (tempo, load factor, colisões, cadeias)
    plot_hash(df, outdir=outdir)

    # 3) Árvores (BST, AVL): tempo, iterações, altura
    plot_trees(df, outdir=outdir)

    # 4) Complexidade: overlay teórico vs experimental
    plot_complexity_overlay(df, outdir=outdir)


def main():
    print_header()

    # Configuração dos experimentos
    data_sizes = [10000, 50000, 100000]
    num_rounds = 5

    # Executa experimentos
    print("\nIniciando experimentos...")
    runner = ExperimentRunner(data_sizes=data_sizes, num_rounds=num_rounds)

    try:
        results = runner.run_all_experiments()

        # Salva resultados
        runner.save_results("experiment_results.json")

        # Exibe análises em tabela (como já existia)
        print_summary_table(results)
        print_hash_analysis(results)
        print_tree_analysis(results)

        # Análise de complexidade (texto, se existente no seu ResultAnalyzer)
        print("\n" + "=" * 80)
        print(" ANÁLISE DE COMPLEXIDADE ".center(80))
        print("=" * 80)
        try:
            analyzer = ResultAnalyzer(results)
            analyzer.print_complexity_analysis()
        except Exception as e:
            print(f"(Aviso) Falha ao executar análise textual de complexidade: {e}")

        # =========================
        # Gráficos (dados reais)
        # =========================
        print("\nGerando gráficos com dados reais...")
        try:
            generate_all_plots(results)
            print("Gráficos salvos em: plots/ e exibidos na tela.")
        except Exception as e:
            print(f"\nNão foi possível gerar gráficos no main.py: {e}")

        print("\n" + "=" * 80)
        print(" EXPERIMENTO CONCLUÍDO COM SUCESSO ".center(80))
        print("=" * 80)

    except KeyboardInterrupt:
        print("\n\nExperimento interrompido pelo usuário.")
        sys.exit(1)
    except Exception as e:
        print(f"\n\nErro durante execução: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()