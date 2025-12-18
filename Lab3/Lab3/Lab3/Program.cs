using System;

public class BiQuadraticEquationSolver
{
    public static double GetCoef(int index, string prompt)
    {
        string coefStr;
        if (index < Environment.GetCommandLineArgs().Length)
        {
            coefStr = Environment.GetCommandLineArgs()[index];
        }
        else
        {
            Console.WriteLine(prompt);
            coefStr = Console.ReadLine();
        }
        return Convert.ToDouble(coefStr);
    }

    public static object[] SolveQuadratic(double a, double b, double c)
    {
        if (a == 0)
        {
            if (b == 0)
            {
                if (c == 0)
                {
                    return new object[] { "InfRoots" };
                }
                else
                {
                    return new object[] { "NoRoots" };
                }
            }
            else
            {
                double root = -c / b;
                if (root >= 0)
                {
                    if (Math.Abs(root) < 1e-9) // root == 0
                    {
                        return new object[] { "OneRoot", 0.0 };
                    }
                    else
                    {
                        double r1 = Math.Sqrt(root);
                        double r2 = -r1;
                        return new object[] { "TwoRoots", r1, r2 };
                    }
                }
                else
                {
                    return new object[] { "NoRoots" };
                }
            }
        }

        double D = b * b - 4 * a * c;
        if (D < 0)
        {
            return new object[] { "NoRoots" };
        }
        else if (D == 0)
        {
            double t = -b / (2.0 * a);
            if (t < 0)
            {
                return new object[] { "NoRoots" };
            }
            else if (Math.Abs(t) < 1e-9) // t == 0
            {
                return new object[] { "OneRoot", 0.0 };
            }
            else
            {
                double r1 = Math.Sqrt(t);
                double r2 = -r1;
                return new object[] { "TwoRoots", r1, r2 };
            }
        }
        else
        {
            double sqD = Math.Sqrt(D);
            double t1 = (-b + sqD) / (2.0 * a);
            double t2 = (-b - sqD) / (2.0 * a);

            var roots = new System.Collections.Generic.List<double>();

            foreach (double t in new double[] { t1, t2 })
            {
                if (t > 0)
                {
                    double r1 = Math.Sqrt(t);
                    double r2 = -r1;
                    roots.Add(r1);
                    roots.Add(r2);
                }
                else if (Math.Abs(t) < 1e-9) // t == 0
                {
                    roots.Add(0.0);
                }
            }

            var uniqueRoots = new System.Collections.Generic.SortedSet<double>(roots);
            var uniqueList = new System.Collections.Generic.List<double>(uniqueRoots);

            switch (uniqueList.Count)
            {
                case 0:
                    return new object[] { "NoRoots" };
                case 1:
                    return new object[] { "OneRoot", uniqueList[0] };
                case 2:
                    return new object[] { "TwoRoots", uniqueList[0], uniqueList[1] };
                case 4:
                    return new object[] { "FourRoots", uniqueList[0], uniqueList[1], uniqueList[2], uniqueList[3] };
                default:
                    var result = new object[uniqueList.Count + 1];
                    result[0] = "MultiRoots";
                    for (int i = 0; i < uniqueList.Count; i++)
                    {
                        result[i + 1] = uniqueList[i];
                    }
                    return result;
            }
        }
    }

    public static object[] GetRoots(double a, double b, double c)
    {
        return SolveQuadratic(a, b, c);
    }

    public static void PrintRoots(object[] rootsTuple)
    {
        switch (rootsTuple[0])
        {
            case "FourRoots":
                Console.WriteLine($"Четыре корня: {rootsTuple[1]}, {rootsTuple[2]}, {rootsTuple[3]}, {rootsTuple[4]}");
                break;
            case "TwoRoots":
                Console.WriteLine($"Два корня: {rootsTuple[1]} и {rootsTuple[2]}");
                break;
            case "OneRoot":
                Console.WriteLine($"Один корень: {rootsTuple[1]}");
                break;
            case "NoRoots":
                Console.WriteLine("Нет корней");
                break;
            case "InfRoots":
                Console.WriteLine("Бесконечно много корней");
                break;
            default:
                Console.WriteLine("Неизвестный тип результата");
                break;
        }
    }

    public static void Main(string[] args)
    {
        double a = GetCoef(1, "Введите коэффициент A:");
        double b = GetCoef(2, "Введите коэффициент B:");
        double c = GetCoef(3, "Введите коэффициент C:");

        object[] roots = GetRoots(a, b, c);
        PrintRoots(roots);
    }
}
