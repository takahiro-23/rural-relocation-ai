from typing import List


def getMaxDifficulty(difficulty: List[int]) -> int:
  n = len(difficulty)
  if n < 3:
    return 0

  difficulty.sort()
  best = difficulty[-1] - difficulty[0]

  for j in range(2, n):
    candidate = 2 * difficulty[j] - difficulty[0] - difficulty[j - 1]
    if candidate > best:
      best = candidate

  max_prefix = float("-inf")
  prefix_best = [float("-inf")] * n
  for i in range(1, n - 1):
    value = difficulty[i] - 2 * difficulty[i - 1]
    if value > max_prefix:
      max_prefix = value
    prefix_best[i] = max_prefix

  for j in range(2, n):
    candidate = difficulty[j] + prefix_best[j - 1]
    if candidate > best:
      best = candidate

  return best
