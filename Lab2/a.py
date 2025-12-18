import sys
import math

class BiQuadraticEquationSolver:
    def __init__(self):
        self.a = None
        self.b = None
        self.c = None

    def get_coef(self, index, prompt):
        try:
            coef_str = sys.argv[index]
        except IndexError:
            print(prompt)
            coef_str = input()
        return float(coef_str)

    def solve_quadratic_sub(self, a, b, c):
        if a == 0:
            if b == 0:
                if c == 0:
                    return ('InfRoots',)
                else:
                    return ('NoRoots',)
            else:
                root = -c / b
                if root >= 0:
                    if root == 0:
                        return ('OneRoot', 0.0)
                    else:
                        r1 = math.sqrt(root)
                        r2 = -r1
                        return ('TwoRoots', r1, r2)
                else:
                    return ('NoRoots',)

        D = b * b - 4 * a * c
        if D < 0:
            return ('NoRoots',)
        elif D == 0:
            t = -b / (2.0 * a)
            if t < 0:
                return ('NoRoots',)
            elif t == 0:
                return ('OneRoot', 0.0)
            else:
                r1 = math.sqrt(t)
                r2 = -r1
                return ('TwoRoots', r1, r2)
        else:
            sqD = math.sqrt(D)
            t1 = (-b + sqD) / (2.0 * a)
            t2 = (-b - sqD) / (2.0 * a)
            roots = []
            for t in [t1, t2]:
                if t > 0:
                    r1 = math.sqrt(t)
                    r2 = -r1
                    roots.extend([r1, r2])
                elif t == 0:
                    roots.append(0.0)

            unique_roots = sorted(list(set(roots)))

            if len(unique_roots) == 0:
                return ('NoRoots',)
            elif len(unique_roots) == 1:
                return ('OneRoot', unique_roots[0])
            elif len(unique_roots) == 2:
                return ('TwoRoots', unique_roots[0], unique_roots[1])
            elif len(unique_roots) == 4:
                return ('FourRoots', unique_roots[0], unique_roots[1], unique_roots[2], unique_roots[3])
            else:
                # Handle edge cases like three distinct roots
                return tuple(['MultiRoots'] + unique_roots)

    def get_roots(self, a, b, c):
        return self.solve_quadratic_sub(a, b, c)

    def print_roots(self, roots_tuple):
        match roots_tuple:
            case ('FourRoots', r1, r2, r3, r4):
                print(f'Четыре корня: {r1}, {r2}, {r3}, {r4}')
            case ('TwoRoots', r1, r2):
                print(f'Два корня: {r1} и {r2}')
            case ('OneRoot', r):
                print(f'Один корень: {r}')
            case ('NoRoots',):
                print('Нет корней')
            case ('InfRoots',):
                print('Бесконечно много корней')
            case _:
                print('Неизвестный тип результата')

    def main(self):
        self.a = self.get_coef(1, 'Введите коэффициент A:')
        self.b = self.get_coef(2, 'Введите коэффициент B:')
        self.c = self.get_coef(3, 'Введите коэффициент C:')
        roots = self.get_roots(self.a, self.b, self.c)
        self.print_roots(roots)

if __name__ == "__main__":
    solver = BiQuadraticEquationSolver()
    solver.main()
