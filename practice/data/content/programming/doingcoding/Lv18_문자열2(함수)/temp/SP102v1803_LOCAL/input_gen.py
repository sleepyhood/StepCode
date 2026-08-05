import sys, random

case_num = int(sys.argv[1]) if len(sys.argv) > 1 else 1

random.seed(1803 + case_num)

clean_samples = [
    "Weekly Team Meeting Agenda",
    "Monthly Financial Report Summary",
    "Project Status Update for Oct",
    "System Maintenance Notice for Weekend",
    "Lunch Menu Announcement for Friday",
    "Welcome to the New Team Member",
    "Customer Support Feedback Summary",
    "Security Patch Upgrade Recommended",
    "Quarterly Revenue Review Notes",
    "Holiday Schedule Announcement"
]

spam_templates = [
    "[AD] Special Offer Discount Sale 50%",
    "Get Low Interest Rate LOAN Today Fast",
    "Exclusive VIP AD Member Registration",
    "Urgent LOAN Approval Ready for You",
    "Big Summer AD Promotion Event",
    "Personal LOAN Consultant Direct Line",
    "[AD] Win Free Coupon Code Now",
    "Instant Cash LOAN Approval Service"
]

if case_num == 1:
    print(1)
    print("Clean Mail Title Notice")
elif case_num == 2:
    print(3)
    print("[AD] Special Offer Sale")
    print("Weekly Work Log Report")
    print("Fast Unsecured LOAN Offer")
elif case_num == 3:
    print(2)
    print("Hello Weekly Team Report")
    print("Tomorrow Meeting Schedule")
elif case_num == 15:
    print(10)
    for i in range(10):
        print(spam_templates[i % len(spam_templates)])
else:
    N = random.randint(3, 8)
    print(N)
    for _ in range(N):
        if random.random() < 0.5:
            print(random.choice(spam_templates))
        else:
            print(random.choice(clean_samples))
