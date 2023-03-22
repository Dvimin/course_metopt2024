from UniformSearch import UniformSearchSolver
from GoldenRatio import GoldenRatioSolver
from SecondaryPoint import SecondaryPointSolver
from Task import Task

if __name__ == "__main__":
    for eps in 0.1, 0.01, 0.001:
        print('Заданная точность: ', eps)
        print('Метод равномерного поиска')
        task = Task()
        uss = UniformSearchSolver(task)
        print('Найденное значение: ', uss.solve(eps))
        print('Метод золотого сечения')
        task = Task()
        grs = GoldenRatioSolver(task)
        print('Найденное значение: ', grs.solve(eps))
        print('Метод пробных точек')
        task = Task()
        sps = SecondaryPointSolver(task)
        print('Найденное значение: ', sps.solve(eps))
        print('\n-----------------------------------\n')