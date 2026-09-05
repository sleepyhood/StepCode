#include <iostream>
#include <string>

using namespace std;

class Printable
{
public:
	virtual void printDoc(string doc) = 0;
	virtual ~Printable() {}
};

class Scannable
{
public:
	virtual void scanDoc(string doc) = 0;
	virtual ~Scannable() {}
};

// Printable과 Scannable을 다중 상속받아 규격을 확장한 SmartOffice
class SmartOffice : public Printable, public Scannable
{
public:
	virtual void faxDoc(string doc, string phone) = 0;
};

class MultiFunctionPrinter : public SmartOffice
{
public:
	void printDoc(string doc) override
	{
		cout << "Printing: " << doc << endl;
	}

	void scanDoc(string doc) override
	{
		cout << "Scanning: " << doc << endl;
	}

	void faxDoc(string doc, string phone) override
	{
		cout << "Faxing: " << doc << " to " << phone << endl;
	}
};

int main()
{
	string doc, phone;
	if (!(cin >> doc >> phone)) return 0;

	MultiFunctionPrinter mfp;
	mfp.printDoc(doc);
	mfp.scanDoc(doc);
	mfp.faxDoc(doc, phone);

	return 0;
}
