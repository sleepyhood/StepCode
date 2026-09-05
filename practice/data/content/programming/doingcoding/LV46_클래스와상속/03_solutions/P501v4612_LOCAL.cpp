#include <iostream>

using namespace std;

class Countable
{
public:
	virtual void increment() = 0;
	virtual void add(int val) = 0;
	virtual int getCount() = 0;
	virtual ~Countable() {}
};

class SafeCounter : public Countable
{
private:
	int count;
public:
	SafeCounter(int initial) : count(initial) {}

	void increment() override
	{
		count++;
	}

	void add(int val) override
	{
		count += val;
	}

	int getCount() override
	{
		return count;
	}
};

int main()
{
	int s, k, v;
	if (!(cin >> s >> k >> v)) return 0;

	SafeCounter counter(s);
	for (int i = 0; i < k; i++) {
		counter.increment();
	}
	counter.add(v);

	cout << counter.getCount() << endl;

	return 0;
}
