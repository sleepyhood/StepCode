#include <iostream>
#include <string>

using namespace std;

class Swimmable
{
public:
	virtual void swim(int meter) = 0;
	virtual ~Swimmable() {}
};

class Flyable
{
public:
	virtual void fly(int meter) = 0;
	virtual ~Flyable() {}
};

// Duck은 수영과 비행을 모두 다중 상속(구현)합니다.
class Duck : public Swimmable, public Flyable
{
public:
	void swim(int meter) override { cout << "Duck swims " << meter << "m" << endl; }
	void fly(int meter) override { cout << "Duck flies " << meter << "m" << endl; }
};

class Penguin : public Swimmable
{
public:
	void swim(int meter) override { cout << "Penguin swims " << meter << "m" << endl; }
};

class Sparrow : public Flyable
{
public:
	void fly(int meter) override { cout << "Sparrow flies " << meter << "m" << endl; }
};

int main()
{
	string animal_name, action;
	int d;
	if (!(cin >> animal_name >> action >> d)) return 0;

	if (action == "swim") {
		Swimmable* swimmer = nullptr;
		if (animal_name == "Duck") swimmer = new Duck();
		else if (animal_name == "Penguin") swimmer = new Penguin();

		if (swimmer != nullptr) {
			swimmer->swim(d);
			delete swimmer;
		} else {
			cout << animal_name << " cannot swim!" << endl;
		}
	} else if (action == "fly") {
		Flyable* flyer = nullptr;
		if (animal_name == "Duck") flyer = new Duck();
		else if (animal_name == "Sparrow") flyer = new Sparrow();

		if (flyer != nullptr) {
			flyer->fly(d);
			delete flyer;
		} else {
			cout << animal_name << " cannot fly!" << endl;
		}
	}

	return 0;
}
