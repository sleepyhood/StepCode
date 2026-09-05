#include <iostream>
#include <string>
#include <iomanip>

using namespace std;

class Shape
{
public:
	virtual string getName() = 0;
	virtual double getArea() = 0;
	virtual ~Shape() {}
};

class Rectangle : public Shape
{
private:
	double width, height;
public:
	Rectangle(double w, double h) : width(w), height(h) {}
	string getName() override { return "Rectangle"; }
	double getArea() override { return width * height; }
};

class Circle : public Shape
{
private:
	double radius;
public:
	Circle(double r) : radius(r) {}
	string getName() override { return "Circle"; }
	double getArea() override { return 3.14 * radius * radius; }
};

int main()
{
	int t;
	if (!(cin >> t)) return 0;

	// Shape 인터페이스 포인터로 다형적 참조
	Shape* shape = nullptr;

	if (t == 1) {
		double w, h;
		cin >> w >> h;
		shape = new Rectangle(w, h);
	} else if (t == 2) {
		double r;
		cin >> r;
		shape = new Circle(r);
	}

	if (shape != nullptr) {
		cout << shape->getName() << endl;
		cout << fixed << setprecision(2) << shape->getArea() << endl;
		delete shape;
	}

	return 0;
}
