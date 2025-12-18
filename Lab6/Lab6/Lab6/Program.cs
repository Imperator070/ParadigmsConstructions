using System;

// Интерфейс для вывода информации
public interface IPrint
{
    void Print();
}

// Абстрактный класс "Геометрическая фигура"
public abstract class GeometricFigure
{
    public abstract double CalculateArea();
}

// Класс "Прямоугольник"
public class Rectangle : GeometricFigure, IPrint
{
    public double Width { get; set; }
    public double Height { get; set; }

    public Rectangle(double width, double height)
    {
        Width = width;
        Height = height;
    }

    public override double CalculateArea()
    {
        return Width * Height;
    }

    public override string ToString()
    {
        return $"Прямоугольник: ширина={Width}, высота={Height}, площадь={CalculateArea():F2}";
    }

    public void Print()
    {
        Console.WriteLine(this.ToString());
    }
}

// Класс "Квадрат"
public class Square : Rectangle, IPrint
{
    public Square(double side) : base(side, side) { }

    public override string ToString()
    {
        return $"Квадрат: сторона={Width}, площадь={CalculateArea():F2}";
    }

    // Метод Print наследуется от Rectangle, но для явного соответствия интерфейсу
    // можно переопределить его, хотя функционально он останется таким же
    public new void Print()
    {
        Console.WriteLine(this.ToString());
    }
}

// Класс "Круг"
public class Circle : GeometricFigure, IPrint
{
    public double Radius { get; set; }

    public Circle(double radius)
    {
        Radius = radius;
    }

    public override double CalculateArea()
    {
        return Math.PI * Radius * Radius;
    }

    public override string ToString()
    {
        return $"Круг: радиус={Radius}, площадь={CalculateArea():F2}";
    }

    public void Print()
    {
        Console.WriteLine(this.ToString());
    }
}

// Класс для запуска программы
public class Program
{
    public static void Main(string[] args)
    {
        // Создание экземпляров фигур
        Rectangle rectangle = new Rectangle(5.0, 10.0);
        Square square = new Square(7.0);
        Circle circle = new Circle(3.0);

        // Вывод информации с использованием интерфейса IPrint
        Console.WriteLine("Информация о фигурах:");
        rectangle.Print();
        square.Print();
        circle.Print();

        // Демонстрация работы через базовый класс
        Console.WriteLine("\nРабота через базовый класс GeometricFigure:");
        GeometricFigure[] figures = { rectangle, square, circle };
        foreach (var figure in figures)
        {
            Console.WriteLine($"{figure.GetType().Name}: площадь = {figure.CalculateArea():F2}");
        }
    }
}