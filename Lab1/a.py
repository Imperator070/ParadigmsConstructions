import sys
import math

def get_coef(index, prompt):
    try:
        coef_str = sys.argv[index]
    except:
        print(prompt)
        coef_str = input()
    coef = float(coef_str)
    return coef

def solve_quadratic(a, b, c):
    if a == 0:
        if b == 0:
            if c == 0:
                return ('InfRoots',)
            else:
                return ('NoRoots',)
        else:
            root = -c / b
            if root >= 0:
                r1 = math.sqrt(root)
                r2 = -r1
                return ('TwoRoots', r1, r2) if r1 != 0 else ('OneRoot', 0.0)
            else:
                return ('NoRoots',)

    D = b*b - 4*a*c
    if D < 0:
        return ('NoRoots',)
    elif D == 0:
        t = -b / (2.0*a)
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
        t1 = (-b + sqD) / (2.0*a)
        t2 = (-b - sqD) / (2.0*a)
        roots = []
        for t in [t1, t2]:
            if t > 0:
                r1 = math.sqrt(t)
                r2 = -r1
                roots.extend([r1, r2])
            elif t == 0:
                roots.append(0.0)
        if len(roots) == 0:
            return ('NoRoots',)
        elif len(roots) == 1:
            return ('OneRoot', roots[0])
        elif len(roots) == 2:
            return ('TwoRoots', roots[0], roots[1])
        elif len(roots) == 3:
            unique = sorted(list(set(roots)))
            if len(unique) == 2:
                return ('TwoRoots', unique[0], unique[1])
        unique = sorted(list(set(roots)))
        if len(unique) == 4:
            return ('FourRoots', unique[0], unique[1], unique[2], unique[3])
        return tuple(['MultiRoots'] + unique)

def get_roots(a, b, c):
    result = solve_quadratic(a, b, c)
    return result

def print_roots(roots_tuple):
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

def main():
    a = get_coef(1, 'Введите коэффициент A:')
    b = get_coef(2, 'Введите коэффициент B:')
    c = get_coef(3, 'Введите коэффициент C:')
    roots = get_roots(a, b, c)
    print_roots(roots)

if __name__ == "__main__":
    main()
