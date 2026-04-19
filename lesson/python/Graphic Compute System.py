import math

class Shape:
    def __init__(self, name):
        self.name = name

    def area(self):
        raise NotImplementedError("子类必须实现 area() 方法")

    def perimeter(self):
        raise NotImplementedError("子类必须实现 perimeter() 方法")

    def __str__(self):
        return f"{self.name} - 面积: {self.area():.2f}, 周长: {self.perimeter():.2f}"

class Circle(Shape):

    def __init__(self, radius):
        super().__init__("圆形")
        self.radius = radius

    def area(self):
        return math.pi * self.radius ** 2

    def perimeter(self):
        return 2 * math.pi * self.radius

class Rectangle(Shape):

    def __init__(self, length, width):
        super().__init__("矩形")
        self.length = length
        self.width = width

    def area(self):
        return self.length * self.width

    def perimeter(self):
        return 2 * (self.length + self.width)

class Triangle(Shape):

    def __init__(self, a, b, c):
        super().__init__("三角形")
        self.a = a
        self.b = b
        self.c = c

    def area(self):
        s = self.perimeter() / 2
        return math.sqrt(s * (s - self.a) * (s - self.b) * (s - self.c))

    def perimeter(self):
        return self.a + self.b + self.c

if __name__ == "__main__":

    circle = Circle(5)
    rectangle = Rectangle(6, 4)
    triangle = Triangle(3, 4, 5)

    shapes = [circle, rectangle, triangle]

    for shape in shapes:
        print(shape)

    total_area = sum(s.area() for s in shapes)
    total_perimeter = sum(s.perimeter() for s in shapes)
    print(f"所有图形的总面积: {total_area:.2f}")
    print(f"所有图形的总周长: {total_perimeter:.2f}")
