def main() -> None:
  n = int(input())
  records = {}
  for _ in range(n):
    parts = input().split()
    name, scores = parts[0], list(map(float, parts[1:]))
    records[name] = scores
  query = input().strip()
  marks = records.get(query, [])
  avg = sum(marks) / len(marks) if marks else 0.0
  print(f"{avg:.2f}")


if __name__ == "__main__":
  main()
