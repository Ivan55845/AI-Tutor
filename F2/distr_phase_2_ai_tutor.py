"""
Распределение задач (Фаза 2) для проекта AI Tutor.

Требования:
- 2 участника;
- каждая задача назначается ровно одному участнику;
- суммарная нагрузка участников должна быть примерно равной;
- максимизировать суммарную предпочтительность.

Решение: полный перебор (2^N), так как N=11 и это быстро/надежно без внешних ILP-библиотек.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import List, Tuple


@dataclass(frozen=True)
class Task:
    code: str
    effort_hours: float
    pref_p1: int
    pref_p2: int


def solve(tasks: List[Task], min_load: float, max_load: float) -> Tuple[int, List[Task], List[Task], float, float]:
    """
    Возвращает:
    - лучший суммарный score (int)
    - список задач участника 1
    - список задач участника 2
    - нагрузка участника 1
    - нагрузка участника 2
    """
    n = len(tasks)
    total_effort = sum(t.effort_hours for t in tasks)

    best_score = None
    best_mask = None
    best_load1 = None

    # mask bit=1 => task -> participant 1; bit=0 => participant 2
    for mask in range(1 << n):
        load1 = 0.0
        score = 0

        for i, task in enumerate(tasks):
            if (mask >> i) & 1:
                load1 += task.effort_hours
                score += task.pref_p1
            else:
                score += task.pref_p2

        load2 = total_effort - load1

        if not (min_load <= load1 <= max_load and min_load <= load2 <= max_load):
            continue

        if best_score is None or score > best_score:
            best_score = score
            best_mask = mask
            best_load1 = load1

    if best_score is None or best_mask is None or best_load1 is None:
        raise RuntimeError("Не найдено допустимого распределения при заданных ограничениях по нагрузке.")

    p1_tasks: List[Task] = []
    p2_tasks: List[Task] = []
    for i, task in enumerate(tasks):
        if (best_mask >> i) & 1:
            p1_tasks.append(task)
        else:
            p2_tasks.append(task)

    load1 = best_load1
    load2 = total_effort - load1
    return best_score, p1_tasks, p2_tasks, load1, load2


def main() -> None:
    # Данные (слегка изменены относительно тестовых, чтобы сохранить общий объём 31.6 ч)
    tasks = [
        Task("T3.1", 6.2, 5, 2),
        Task("T3.2", 1.8, 2, 5),
        Task("T3.3", 3.1, 3, 4),
        Task("T3.4", 2.1, 2, 4),
        Task("T3.5", 2.9, 3, 5),
        Task("T3.6", 2.0, 5, 3),
        Task("T3.7", 2.1, 4, 4),
        Task("T3.8", 1.3, 4, 3),
        Task("T3.9", 3.0, 5, 4),
        Task("T3.10", 3.1, 4, 5),
        Task("T3.11", 4.0, 3, 4),
    ]

    total_effort = sum(t.effort_hours for t in tasks)
    avg = total_effort / 2.0

    # Требование "суммарная нагрузка +- равна": задаём допуск ±0.6 часа от среднего.
    tol = 0.6
    min_load = avg - tol
    max_load = avg + tol

    score, p1, p2, load1, load2 = solve(tasks, min_load=min_load, max_load=max_load)

    print("Проект: AI Tutor")
    print(f"Всего задач: {len(tasks)}")
    print(f"Общий объём: {total_effort:.1f} ч (средняя нагрузка: {avg:.1f} ч)")
    print(f"Допустимый диапазон нагрузки: {min_load:.1f}–{max_load:.1f} ч")
    print(f"Итоговый score (сумма предпочтений): {score}")
    print()

    def fmt_task_list(ts: List[Task]) -> str:
        return ", ".join(t.code for t in ts) if ts else "-"

    print("Участник 1:")
    print(f"  Задачи: {fmt_task_list(p1)}")
    print(f"  Нагрузка: {load1:.1f} ч")
    print()

    print("Участник 2:")
    print(f"  Задачи: {fmt_task_list(p2)}")
    print(f"  Нагрузка: {load2:.1f} ч")
    print()

    print(f"Разница нагрузки: {abs(load1 - load2):.1f} ч")


if __name__ == "__main__":
    main()
