#include <iostream>
#include <string>

using namespace std;

class Adjustable
{
public:
	static const int MIN_VOLUME = 0;
	static const int MAX_VOLUME = 100;

	virtual void setVolume(int level) = 0;

	// C++에서는 인터페이스에 기본 구현 함수를 둘 수 있습니다.
	virtual string checkSafety(int level)
	{
		if (level >= MIN_VOLUME && level <= MAX_VOLUME) {
			return "SAFE";
		}
		return "OUT_OF_RANGE";
	}

	virtual ~Adjustable() {}
};

class Speaker : public Adjustable
{
private:
	int volume;
public:
	Speaker() : volume(0) {}

	void setVolume(int level) override
	{
		volume = level;
		cout << "Volume set to " << volume << endl;
	}
};

int main()
{
	int v;
	if (!(cin >> v)) return 0;

	Speaker speaker;
	string safety = speaker.checkSafety(v);
	cout << safety << endl;

	if (safety == "SAFE") {
		speaker.setVolume(v);
	} else {
		cout << "Volume setting failed" << endl;
	}

	return 0;
}
