
import task as t

def golden_ratio(x_k, eps):
    a = 0
    b = 1

    alpha = (3 - 5 ** 0.5) / 2
    x_1 = a + alpha * (b - a)
    x_2 = b - alpha * (b - a)
    fx_1 = t.f(x_k - x_1 * t.gradf(x_k))
    fx_2 = t.f(x_k - x_2 * t.gradf(x_k))
    while abs(a - b) > eps:
        if fx_1 > fx_2:
            b = x_2
            x_2 = x_1
            fx_2 = fx_1
            x_1 = a + alpha * (b - a)
            fx_1 = t.f(x_k - x_1 * t.gradf(x_k))
        else:
            a = x_1
            x_1 = x_2
            fx_1 = fx_2
            x_2 = b - alpha * (b - a)
            fx_2 = t.f(x_k - x_2 * t.gradf(x_k))
    return (a + b) / 2.0


def secondary_point(x_k, eps):
    a = 0
    b = 1
    while abs(b - a) >= eps:
        c = a + (b - a) / 3
        d = b - (b - a) / 3
        if t.f(x_k - c * t.gradf(x_k)) <= t.f(x_k - d * t.gradf(x_k)):
            b = d
        else:
            a = c
    return (a + b) / 2.0
