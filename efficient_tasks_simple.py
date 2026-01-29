from typing import List


def get_max_difficulty_simple(difficulty: List[int]) -> int:
  """Beginner-friendly version of Efficient Tasks solution."""
  n = len(difficulty)
  if n < 3:
    return 0

  numbers = sorted(difficulty)
  answer = numbers[-1] - numbers[0]

  left_group_min = numbers[0]
  for right_start in range(2, n):
    middle_pick = numbers[right_start]
    prev_middle_value = numbers[right_start - 1]
    current = 2 * middle_pick - left_group_min - prev_middle_value
    if current > answer:
      answer = current

  best_gain = float("-inf")
  best_gain_up_to = [float("-inf")] * n
  for i in range(1, n - 1):
    gain = numbers[i] - 2 * numbers[i - 1]
    if gain > best_gain:
      best_gain = gain
    best_gain_up_to[i] = best_gain

  for right_start in range(2, n):
    gain_for_middle = best_gain_up_to[right_start - 1]
    if gain_for_middle == float("-inf"):
      continue
    current = numbers[right_start] + gain_for_middle
    if current > answer:
      answer = current

  return answer
