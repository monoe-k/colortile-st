import random

def can_place_no_same_outer(grid, n, m, i, j, tile):
    current_outer = tile[0]
    if i > 0 and grid[i-1][j] is not None and grid[i-1][j][0] == current_outer:
        return False
    if i < n-1 and grid[i+1][j] is not None and grid[i+1][j][0] == current_outer:
        return False
    if j > 0 and grid[i][j-1] is not None and grid[i][j-1][0] == current_outer:
        return False
    if j < m-1 and grid[i][j+1] is not None and grid[i][j+1][0] == current_outer:
        return False
    return True

def backtrack(arr, n, m, grid, used, i=0, j=0):
    if i == n:
        return True

    next_i, next_j = (i, j+1) if (j+1) < m else (i+1, 0)

    for idx, tile in enumerate(arr):
        if used[idx]:
            continue
        if can_place_no_same_outer(grid, n, m, i, j, tile):
            grid[i][j] = tile
            used[idx] = True
            if backtrack(arr, n, m, grid, used, next_i, next_j):
                return True
            grid[i][j] = None
            used[idx] = False

    return False

def arrange_tiles_no_same_outer(arr, n, m):
    if len(arr) < n*m:
        raise ValueError("要素数が不足しています")
    arr = arr[:n*m]
    random.shuffle(arr)

    grid = [[None]*m for _ in range(n)]
    used = [False]*len(arr)

    if backtrack(arr, n, m, grid, used):
        return grid
    else:
        raise RuntimeError("条件を満たす配置が見つかりませんでした")
