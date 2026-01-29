from typing import List


def count_increasing_segments(transaction_values: List[int], k: int) -> int:
  if k <= 0 or not transaction_values:
    return 0
  if k == 1:
    return len(transaction_values)

  inc_len = 1
  result = 0

  for i in range(1, len(transaction_values)):
    if transaction_values[i] > transaction_values[i - 1]:
      inc_len += 1
    else:
      inc_len = 1

    if inc_len >= k:
      result += 1

  return result


if __name__ == "__main__":
  import sys

  data = list(map(int, sys.stdin.read().strip().split()))
  if len(data) < 2:
    print(0)
  else:
    k = data[-1]
    values = data[:-1]
    print(count_increasing_segments(values, k))
