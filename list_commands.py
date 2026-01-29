if __name__ == "__main__":
  N = int(input())
  data = []

  for _ in range(N):
    parts = input().split()
    command = parts[0]
    args = list(map(int, parts[1:]))

    if command == "insert":
      data.insert(args[0], args[1])
    elif command == "print":
      print(data)
    elif command == "remove":
      data.remove(args[0])
    elif command == "append":
      data.append(args[0])
    elif command == "sort":
      data.sort()
    elif command == "pop":
      if data:
        data.pop()
    elif command == "reverse":
      data.reverse()
