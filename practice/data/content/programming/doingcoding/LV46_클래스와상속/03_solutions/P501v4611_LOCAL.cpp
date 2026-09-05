#include <iostream>
#include <string>

using namespace std;

// 소리를 내는 순수 규격 클래스 (인터페이스)
class Soundable
{
public:
	virtual void sound(int times) = 0;
	virtual ~Soundable() {}
};

class Dog : public Soundable
{
public:
	void sound(int times) override
	{
		for (int i = 0; i < times; i++) {
			cout << "Bark" << (i == times - 1 ? "" : " ");
		}
		cout << endl;
	}
};

class Cat : public Soundable
{
public:
	void sound(int times) override
	{
		for (int i = 0; i < times; i++) {
			cout << "Meow" << (i == times - 1 ? "" : " ");
		}
		cout << endl;
	}
};

class Duck : public Soundable
{
public:
	void sound(int times) override
	{
		for (int i = 0; i < times; i++) {
			cout << "Quack" << (i == times - 1 ? "" : " ");
		}
		cout << endl;
	}
};

int main()
{
	string type;
	int n;
	if (!(cin >> type >> n)) return 0;

	Soundable* animal = nullptr;
	if (type == "Dog") animal = new Dog();
	else if (type == "Cat") animal = new Cat();
	else if (type == "Duck") animal = new Duck();

	if (animal != nullptr) {
		animal->sound(n);
		delete animal;
	}

	return 0;
}
