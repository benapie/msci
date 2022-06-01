

def print_mat():
    for i in bmat:
        print(i)
    print()

simplices = [[1], [2], [3], [4], [1,2], [1,3], [1,4], [2,3], [2,4], [3,4], [1,2,3], [1,2,4], [1,3,4], [2,3,4]]


m = len(simplices)
bmat = [[0 for i in range(m)] for i in range(m)]

for i, simplex in enumerate(simplices):
    if len(simplex) == 1:
        continue
    for face_index in range(len(simplex)):
        face = list(simplex)
        face.pop(face_index)
        bmat[simplices.index(face)][i] = 1


# m = 7
# bmat = [
#     [0, 0, 0, 1, 0, 1, 0],
#     [0, 0, 0, 1, 1, 0, 0],
#     [0, 0, 0, 0, 1, 1, 0],
#     [0, 0, 0, 0, 0, 0, 1],
#     [0, 0, 0, 0, 0, 0, 1],
#     [0, 0, 0, 0, 0, 0, 1],
#     [0, 0, 0, 0, 0, 0, 0]
# ]


def f2_add(a: int, b: int) -> int:
    return (a + b) % 2


def low(col: int) -> int:
    row = -1
    for i in range(m):
        if bmat[i][col] == 1:
            row = i
    return row


def add_col_to_col(col_in: int, col_out: int) -> int:
    for i in range(0, m):
        bmat[i][col_out] = f2_add(bmat[i][col_out], bmat[i][col_in])


def is_col_reduced(col: int) -> bool:
    for i in range(0, col):
        if low(col) == low(i):
            if low(col) == -1:
                return True
            return False
    return True

def slow_per_hom():
  for i in range(0, len(bmat)):
      if low(i) == -1:
          continue
      flag = True
      while not is_col_reduced(i):
          for j in range(0, i):
              if low(i) == low(j):
                  add_col_to_col(j, i)
                  break




if __name__ == "__main__":
  print_mat()
  slow_per_hom()
  print_mat()

