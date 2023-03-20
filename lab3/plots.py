import numpy as np
import matplotlib.pyplot as plt
import Task as t

task = t.Task()
fig, ax = plt.subplots()
plt.rcParams['text.usetex'] = True
x = np.linspace(task.a, task.b, 10_000)
task = t.Task()
y = [task.func(val) for val in x]
ax.plot(x, y)
ax.set_title(r'$f(x) = \frac{x*\sqrt{1-x}}{1+x}$')
plt.show()