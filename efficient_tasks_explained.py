from typing import List


def get_max_difficulty(difficulty: List[int]) -> int:
  """Readable version of Efficient Tasks solution."""
  n = len(difficulty)
  if n < 3:
    return 0

  values = sorted(difficulty)
  best = values[-1] - values[0]

  # Case 1: middle group sits on the right (A=smallest block, B=right block start)
  for j in range(2, n):
    candidate = 2 * values[j] - values[0] - values[j - 1]
    if candidate > best:
      best = candidate

  # Case 2: middle group sits on the left (C=largest block, B=left block end)
  prefix_max = float("-inf")
  prefix_gain = [float("-inf")] * n
  for i in range(1, n - 1):
    gain = values[i] - 2 * values[i - 1]
    if gain > prefix_max:
      prefix_max = gain
    prefix_gain[i] = prefix_max

  for j in range(2, n):
    candidate = values[j] + prefix_gain[j - 1]
    if candidate > best:
      best = candidate

  return best
