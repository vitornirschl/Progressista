from pathlib import Path
import sys
import argparse


def read_progress(tasks_file: str | Path) -> tuple[int, int]:
    """
    Lê um arquivo de tarefas e retorna uma porcentagem de progresso
    das tarefas concluídas.

    Recebe
        tasks_file : str | Path
        Caminho para o arquivo de tarefas.

    Retorna
        tuple[int, int]
        Tupla com (quantidade de tarefas concluídas, quantidade de tarefas)
    """
    tasks_file = Path(tasks_file)

    tasks = []
    with open(tasks_file, "r", encoding="utf-8") as file:
        for linha in file:
            tasks.append(linha.strip())

    qtd_tasks = 0
    for task in tasks:
        if "[]" in task.replace(" ", "") or "[x]" in task.replace(" ", ""):
            qtd_tasks += 1
    qtd_feita = 0
    for task in tasks:
        if "[x]" in task.replace(" ", ""):
            qtd_feita += 1

    return (qtd_feita, qtd_tasks)


def progress_bar(feita_total: tuple[int, int]) -> str:
    """
    Recebe uma quantidade de tarefas concluídas, dada uma quantidade
    de tarefas totais, e retorna uma barra de progresso.

    Recebe
        feita_total : tuple[int, int]
        Tupla com (quantidade de tarefas concluídas, quantidade de tarefas)

    Retorna
        str
        Bela barra de progresso, apresentando a porcentagem concluída.
    """
    qtd_feita = feita_total[0]
    qtd_tasks = feita_total[1]

    if qtd_tasks != 0:
        pct = qtd_feita / qtd_tasks
    else:
        pct = 100

    tamanho_barra = 40
    preenchido = int(tamanho_barra * pct)

    # --- cores ---
    cor_barra_vazia = "\033[02m"  # cinzinha
    cor_barra_cheia = "\033[32m"  # verde ♦
    cor_texto = "\033[93m"  # amarelo brilhante ♦
    reset_cor = "\033[0m"

    barra = (
        f"{cor_barra_cheia}█{reset_cor}" * preenchido
        + f"{cor_barra_vazia}—{reset_cor}" * (tamanho_barra - preenchido)
    )
    texto = f"[{barra}] {cor_texto}{pct:.1%}\r{reset_cor}"
    return texto


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="Progressista", description="Um gerador de barras de progresso."
    )
    parser.add_argument("tasks_file")

    args = parser.parse_args()
    qtd_feita, qtd_tasks = read_progress(args.tasks_file)
    pb = progress_bar((qtd_feita, qtd_tasks))

    sys.stdout.write(pb)
    print()
