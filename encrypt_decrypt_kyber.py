## import numpy as np


def matrix_polyadd(X, Y, q):
    xShape = X.shape
    yShape = Y.shape

    while len(xShape) < 3:
        X = np.expand_dims(X, axis=0)
        xShape = X.shape

    while len(yShape) < 3:
        Y = np.expand_dims(Y, axis=0)
        yShape = Y.shape

    assert (
        xShape == yShape
    ), f"Addition: Invalid matrix dimensions: X[{xShape}], Y[{yShape}]"

    result = []
    row = None

    for i in range(xShape[0]):
        for j in range(xShape[1]):
            if j == 0:
                row = []
                result.append(row)
            el = np.polyadd(X[i][j], Y[i][j])
            el = np.remainder(el, q)
            row.append(el)

    return np.squeeze(np.array(result)).astype(int)

def matrix_polymul(X, Y, f, q):
    xShape = X.shape
    yShape = Y.shape

    if len(xShape) == 2:
        X = np.expand_dims(X, axis=0)
        xShape = X.shape

    if len(yShape) == 2:
        Y = np.expand_dims(Y, axis=1)
        yShape = Y.shape

    assert (
        xShape[1] == yShape[0]
    ), f"Multiplication: Invalid matrix dimensions: X[{xShape}], Y[{yShape}]"

    result = []
    row = None
    s = None

    for i in range(xShape[0]):
        for j in range(yShape[1]):
            if j == 0:
                row = []
                result.append(row)
                s = None
            for k in range(xShape[1]):
                el = np.polymul(X[i][k], Y[k][j])
                el = np.polydiv(el, f)[1]
                el = np.remainder(el, q)
                if k == 0:
                    s = el
                else:
                    s = np.polyadd(s, el)
                    s = np.remainder(s, q)
                if k == xShape[1] - 1:
                    row.append(s)

    return np.squeeze(np.array(result)).astype(int)

# Get user input for q
q = int(input("Enter the value of q: "))

# Get user input for f as a space-separated list of integers
f = np.array(list(map(int, input("Enter the values of f: ").split())))

# Get user input for s as a 2D matrix
s_rows = int(input("Enter the number of rows in matrix s: "))
s_cols = int(input("Enter the number of columns in matrix s: "))
s = np.zeros((s_rows, s_cols), dtype=int)
for i in range(s_rows):
    row_input = input(f"Enter the elements for row {i+1} of matrix s: ").split()
    s[i] = np.array(list(map(int, row_input)))

# Get user input for A as a 3D matrix
A_layers = int(input("Enter the number of layers in matrix A: "))
A_rows = int(input("Enter the number of rows in matrix A: "))
A_cols = int(input("Enter the number of columns in matrix A: "))
A = np.zeros((A_layers, A_rows, A_cols), dtype=int)
for i in range(A_layers):
    print(f"Enter the elements for layer {i+1} of matrix A:")
    for j in range(A_rows):
        row_input = input(f"Enter the elements for row {j+1} of layer {i+1}: ").split()
        A[i, j] = np.array(list(map(int, row_input)))

# Get user input for e as a 2D matrix
e_rows = int(input("Enter the number of rows in matrix e: "))
e_cols = int(input("Enter the number of columns in matrix e: "))
e = np.zeros((e_rows, e_cols), dtype=int)
for i in range(e_rows):
    row_input = input(f"Enter the elements for row {i+1} of matrix e: ").split()
    e[i] = np.array(list(map(int, row_input)))

# Get user input for r as a 2D matrix
r_rows = int(input("Enter the number of rows in matrix r: "))
r_cols = int(input("Enter the number of columns in matrix r: "))
r = np.zeros((r_rows, r_cols), dtype=int)
for i in range(r_rows):
    row_input = input(f"Enter the elements for row {i+1} of matrix r: ").split()
    r[i] = np.array(list(map(int, row_input)))

# Get user input for e1 as a 2D matrix
e1_rows = int(input("Enter the number of rows in matrix e1: "))
e1_cols = int(input("Enter the number of columns in matrix e1: "))
e1 = np.zeros((e1_rows, e1_cols), dtype=int)
for i in range(e1_rows):
    row_input = input(f"Enter the elements for row {i+1} of matrix e1: ").split()
    e1[i] = np.array(list(map(int, row_input)))

# Get user input for e2 as a 1D array
e2_input = input("Enter the elements for array e2: ").split()
e2 = np.array(list(map(int, e2_input)))

# Get user input for m as a space-separated list of integers
m_input = input("Enter the elements for array m: ").split()
m = np.array(list(map(int, m_input)))

# Perform the calculations with user-provided inputs
t = matrix_polyadd(matrix_polymul(A, s, f, q), e, q)
m = m * q // 2
u = matrix_polyadd(matrix_polymul(np.transpose(A, axes=(1, 0, 2)), r, f, q), e1, q)
v = matrix_polyadd(matrix_polyadd(matrix_polymul(t, r, f, q), e2, q), m, q)
m1 = matrix_polyadd(v, matrix_polymul(s, u, f, q) * (-1), q)
m_decrypted = [1 if abs(x - q // 2) < min(x, q - 1 - x) else 0 for x in m1]




# Print the output
print(f"t:\n{t}")
print(f"m:\n{m}")
print(f"u:\n{u}")
print(f"v:\n{v}")
print(f"Decrypted message before rounding:\n{m1}")
print(f"Decrypted message:\n{m_decrypted}")