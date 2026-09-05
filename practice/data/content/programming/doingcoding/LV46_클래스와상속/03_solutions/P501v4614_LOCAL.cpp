#include <iostream>
#include <string>
#include <vector>

using namespace std;

class Device
{
public:
	virtual string getName() = 0;
	virtual int calculatePower(int hour) = 0;
	virtual ~Device() {}
};

class TV : public Device
{
public:
	string getName() override { return "TV"; }
	int calculatePower(int hour) override { return hour * 100; }
};

class AirConditioner : public Device
{
public:
	string getName() override { return "AirConditioner"; }
	int calculatePower(int hour) override { return hour * 800; }
};

class Computer : public Device
{
public:
	string getName() override { return "Computer"; }
	int calculatePower(int hour) override { return hour * 250; }
};

int main()
{
	int n;
	if (!(cin >> n)) return 0;

	// Device 인터페이스 포인터를 담는 벡터
	vector<Device*> devices;
	vector<int> hours(n);

	for (int i = 0; i < n; i++) {
		string type;
		int h;
		cin >> type >> h;
		hours[i] = h;

		if (type == "TV") devices.push_back(new TV());
		else if (type == "AirConditioner") devices.push_back(new AirConditioner());
		else if (type == "Computer") devices.push_back(new Computer());
	}

	int total = 0;
	for (int i = 0; i < n; i++) {
		int power = devices[i]->calculatePower(hours[i]);
		cout << devices[i]->getName() << ": " << power << "W" << endl;
		total += power;
		delete devices[i];
	}
	cout << "Total: " << total << "W" << endl;

	return 0;
}
