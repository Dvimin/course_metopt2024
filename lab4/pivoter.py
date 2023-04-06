
import task as t

def golden_ratio(x_k, grad, eps):
    a = 0
    b = 1

    alpha = (3 - 5 ** 0.5) / 2
    x_1 = a + alpha * (b - a)
    x_2 = b - alpha * (b - a)
    fx_1 = t.f(x_k - x_1 * grad)
    fx_2 = t.f(x_k - x_2 * grad)
    while abs(a - b) > eps:
        if fx_1 < fx_2:
            b = x_2
            x_2 = x_1
            fx_2 = fx_1
            x_1 = a + alpha * (b - a)
            fx_1 = t.f(x_k - x_1 * grad)
        else:
            a = x_1
            x_1 = x_2
            fx_1 = fx_2
            x_2 = b - alpha * (b - a)
            fx_2 = t.f(x_k - x_2 * grad)
    return (a + b) / 2.0


def secondary_point(x_k, grad, eps):
    a = 0
    b = 1
    while abs(b - a) >= eps:
        c = a + (b - a) / 3
        d = b - (b - a) / 3
        if t.f(x_k - c * grad) <= t.f(x_k - d * grad):
            b = d
        else:
            a = c
    return (a + b) / 2.0
