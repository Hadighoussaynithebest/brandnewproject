import math
import random

# ----- Data: XOR -----
X = [(0, 0), (0, 1), (1, 0), (1, 1)]
Y = [0, 1, 1, 0]

# ----- Initialize weights -----
random.seed(0)
w_hidden = [[random.uniform(-1, 1) for _ in range(2)] for _ in range(2)]  # 2 hidden neurons, 2 inputs
b_hidden = [0.0, 0.0]
w_out = [random.uniform(-1, 1) for _ in range(2)]  # from 2 hidden -> 1 output
b_out = 0.0
lr = 0.1  # learning rate

def sigmoid(x):
    return 1 / (1 + math.exp(-x))

def forward(x1, x2):
    h = []
    for i in range(2):
        z = w_hidden[i][0]*x1 + w_hidden[i][1]*x2 + b_hidden[i]
        h.append(sigmoid(z))
    y_hat = sigmoid(w_out[0]*h[0] + w_out[1]*h[1] + b_out)
    return h, y_hat

# ----- Training -----
for epoch in range(5000):
    for (x1, x2), y in zip(X, Y):
        # forward
        h, y_hat = forward(x1, x2)
        # loss derivative (MSE): dL/dy_hat = 2*(y_hat - y)
        dL_dy = 2 * (y_hat - y)

        # output layer gradients
        dy_dz_out = y_hat * (1 - y_hat)
        dL_dz_out = dL_dy * dy_dz_out
        for i in range(2):
            w_out[i] -= lr * dL_dz_out * h[i]
        b_out -= lr * dL_dz_out

        # hidden layer gradients
        for i in range(2):
            dz_out_dh = w_out[i]
            dL_dh = dL_dz_out * dz_out_dh
            dh_dz = h[i] * (1 - h[i])
            dL_dz_h = dL_dh * dh_dz
            w_hidden[i][0] -= lr * dL_dz_h * x1
            w_hidden[i][1] -= lr * dL_dz_h * x2
            b_hidden[i] -= lr * dL_dz_h

# ----- Test -----
print("Trained XOR network:")
for x, y in zip(X, Y):
    _, y_hat = forward(*x)
    print(f"Input {x} -> predicted {y_hat:.3f}, target {y}")
