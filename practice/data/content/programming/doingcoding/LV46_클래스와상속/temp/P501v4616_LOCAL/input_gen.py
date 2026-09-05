import sys, random

case_num = int(sys.argv[1]) if len(sys.argv) > 1 else 1
random.seed(461600 + case_num)

exts = [".pdf", ".docx", ".xlsx", ".hwp", ".png", ".txt"]
prefixes = ["010", "02", "031", "051", "042"]

if case_num == 1:
    print("a.txt\n010-0000-0000")
elif case_num == 2:
    print("Report.pdf\n010-1234-5678") # 예제 1
elif case_num == 3:
    print("Invoice.docx\n02-987-6543") # 예제 2
elif case_num == 15:
    print("VeryLongDocumentNameFinalV2.pdf\n031-9999-8888")
else:
    doc = f"doc_{case_num}{random.choice(exts)}"
    prefix = random.choice(prefixes)
    p1 = random.randint(100, 9999)
    p2 = random.randint(1000, 9999)
    phone = f"{prefix}-{p1:03d}-{p2:04d}" if prefix == "02" else f"{prefix}-{p1:04d}-{p2:04d}"
    print(f"{doc}\n{phone}")
