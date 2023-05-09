import task as t
import zoytendeyk as z

true_solution = [-0.42884501393, -0.32163376045, 0]

# какое-то наше нач приближение
x0 = [1, 1, 1]
# найдем валидное начальное приближение
x0 = z.validatex0(x0)

# найдем начальное eta
eta0 = -max([fun(x0) for fun in t.restrictions])

# решим задачу методом Зойдендейка
res = z.zoytendeyk(x0, eta0)
print(x0)

print(f"Answer: {res}")
print(f"f(x) = {t.f(res)}")
print(res[0] - true_solution[0])
print(res[1] - true_solution[1])
print(res[2] - true_solution[2])