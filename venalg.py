def find_optimal_assignment(cost_table):
    size = len(cost_table)
    cost_matrix = [row.copy() for row in cost_table]  # Копируем, чтобы не менять исходную матрицу

    # Этап 1: Редукция строк (вычитаем минимум каждой строки)
    for i in range(size):
        min_val = min(cost_matrix[i])
        for j in range(size):
            cost_matrix[i][j] -= min_val

    # Этап 2: Редукция столбцов (вычитаем минимум каждого столбца)
    for j in range(size):
        min_val = min(cost_matrix[i][j] for i in range(size))
        for i in range(size):
            cost_matrix[i][j] -= min_val

    # Этап 3: Поиск оптимальных назначений
    while True:
        # Матрица назначений (True = назначено)
        assignment = [[False for _ in range(size)] for _ in range(size)]
        marked_rows = set()
        marked_cols = set()

        # Жадный выбор независимых нулей
        for i in range(size):
            for j in range(size):
                if cost_matrix[i][j] == 0 and i not in marked_rows and j not in marked_cols:
                    assignment[i][j] = True
                    marked_rows.add(i)
                    marked_cols.add(j)

        # Если все назначены — завершаем
        if len(marked_rows) == size:
            break

        # Этап 4: Покрытие нулей минимальным числом линий
        # Находим минимальный непокрытый элемент
        min_uncovered = float('inf')
        for i in range(size):
            for j in range(size):
                if i not in marked_rows and j not in marked_cols:
                    if cost_matrix[i][j] < min_uncovered:
                        min_uncovered = cost_matrix[i][j]

        # Корректируем матрицу
        for i in range(size):
            for j in range(size):
                if i not in marked_rows and j not in marked_cols:
                    cost_matrix[i][j] -= min_uncovered
                elif i in marked_rows and j in marked_cols:
                    cost_matrix[i][j] += min_uncovered

    # Собираем результаты
    assignments = []
    total_cost = 0
    for i in range(size):
        for j in range(size):
            if assignment[i][j]:
                assignments.append((i, j))
                total_cost += cost_table[i][j]

    return assignments, total_cost


# Пример использования
if __name__ == "__main__":
    cost_matrix = [
        [5, 3, 2],
        [6, 3, 4],
        [7, 9, 5]
    ]

    assignments, total_cost = find_optimal_assignment(cost_matrix)

    print("Оптимальное распределение:")
    for worker, task in assignments:
        print(f"Исполнитель {worker + 1} → Задача {task + 1} (стоимость: {cost_matrix[worker][task]})")

    print(f"Общая минимальная стоимость: {total_cost}")