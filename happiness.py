import sys


def main() -> None:
  tokens = sys.stdin.read().strip().split()
  if not tokens:
    return

  it = iter(tokens)
  n = int(next(it))
  m = int(next(it))

  arr = [int(next(it)) for _ in range(n)]
  liked = {int(next(it)) for _ in range(m)}
  disliked = {int(next(it)) for _ in range(m)}

  happiness = 0
  for value in arr:
    if value in liked:
      happiness += 1
    elif value in disliked:
      happiness -= 1

  print(happiness)


if __name__ == "__main__":
  main()
