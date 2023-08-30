import numpy as np

def generate_poly(n, q):
    p = np.random.randint(0, q, n)
    return p

def generate_poly_matrix(n, q, k):
    result = []
    row = None
    for i in range(k):
        for j in range(k):
            if j == 0:
                row = []
                result.append(row)
            row.append(generate_poly(n, q))
    return np.array(result, dtype=int)

def _cbd(n, eta):
    i = 0
    while i < eta:
        p1 = np.random.randint(0, 2, n)
        if i == 0:
            p = p1
        else:
            p = p + p1
        i += 1
    return p

# centered binomial distribution
def cbd(n, eta):
    a = _cbd(n, eta)
    b = _cbd(n, eta)
    return a - b

def cbd_vector(n, eta, k):
    result = []

    for i in range(k):
        result.append(cbd(n, eta))

    return np.squeeze(np.array(result, dtype=int))

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

def compress(x, q, d):
    q1 = 2**d
    x = np.round(q1 / q * x).astype(int)
    x = np.remainder(x, q1)
    return x

def decompress(x, q, d):
    q1 = 2**d
    x = np.round(q / q1 * x).astype(int)
    x = np.remainder(x, q)
    return x

n = 256
q = 3329
k = 2

eta1 = 3
eta2 = 2

du = 10
dv = 4

f = np.zeros(n + 1)
f[0] = 1
f[n] = 1

s = cbd_vector(n, eta1, k)

print(f"s\n{s}")

A = generate_poly_matrix(n, q, k)

e = cbd_vector(n, eta1, k)

print(f"e:\n{e}")

t = matrix_polyadd(matrix_polymul(A, s, f, q), e, q)

print(f"t:\n{t}")

#Encryption

m = np.array(generate_poly(n, 2))

m_scaled = decompress(m, q, 1)

print(f"m_scaled:\n{m_scaled}")

r = cbd_vector(n, eta1, k)

e1 = cbd_vector(n, eta2, k)

e2 = cbd_vector(n, eta2, 1)

u = matrix_polyadd(matrix_polymul(np.transpose(A, axes=(1, 0, 2)), r, f, q), e1, q)

v = matrix_polyadd(matrix_polyadd(matrix_polymul(t, r, f, q), e2, q), m_scaled, q)

print(f"u:\n{u}")

print(f"v:\n{v}")

u = compress(u, q, du)

v = compress(v, q, dv)

print(f"u:\n{u}")

print(f"v:\n{v}")

# Decryption

u = decompress(u, q, du)

v = decompress(v, q, dv)

m1 = matrix_polyadd(v, matrix_polymul(s, u, f, q) * (-1), q)

print(f"Decrypted message before rounding:\n{m1}")

m_decrypted = compress(m1, q, 1)

print(f"Original message:\n{m}")

print(f"Decrypted message:\n{m_decrypted}")

print(np.array_equal(m, m_decrypted))
