#include <iostream>
#include <algorithm>

using namespace std;

class DiscountPolicy
{
public:
	virtual int calculateDiscount(int price) = 0;
	virtual ~DiscountPolicy() {}
};

class FixedDiscountPolicy : public DiscountPolicy
{
private:
	int discountAmount;
public:
	FixedDiscountPolicy(int amount) : discountAmount(amount) {}
	int calculateDiscount(int price) override
	{
		return min(price, discountAmount);
	}
};

class RateDiscountPolicy : public DiscountPolicy
{
private:
	int discountRate;
public:
	RateDiscountPolicy(int rate) : discountRate(rate) {}
	int calculateDiscount(int price) override
	{
		return price * discountRate / 100;
	}
};

class NoDiscountPolicy : public DiscountPolicy
{
public:
	int calculateDiscount(int price) override
	{
		return 0;
	}
};

// 인터페이스에 의존하는 주문 처리기
class OrderProcessor
{
private:
	DiscountPolicy* policy;
public:
	OrderProcessor() : policy(nullptr) {}

	// 전략 객체를 동적으로 교체 주입받습니다.
	void setPolicy(DiscountPolicy* newPolicy)
	{
		this->policy = newPolicy;
	}

	int getDiscount(int price)
	{
		if (policy == nullptr) return 0;
		return policy->calculateDiscount(price);
	}

	int getFinalPrice(int price)
	{
		return price - getDiscount(price);
	}
};

int main()
{
	int price, type, param;
	if (!(cin >> price >> type >> param)) return 0;

	DiscountPolicy* policy = nullptr;
	if (type == 1) policy = new FixedDiscountPolicy(param);
	else if (type == 2) policy = new RateDiscountPolicy(param);
	else if (type == 3) policy = new NoDiscountPolicy();

	OrderProcessor processor;
	processor.setPolicy(policy);

	cout << "Discount: " << processor.getDiscount(price) << endl;
	cout << "Final Price: " << processor.getFinalPrice(price) << endl;

	if (policy != nullptr) delete policy;

	return 0;
}
