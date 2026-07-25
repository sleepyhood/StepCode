import sys

case_num = int(sys.argv[1]) if len(sys.argv) > 1 else 1

test_cases = {
    1: ("doing", "coding"),
    2: ("doing", "korea"),
    3: ("coding", "computer"),
    4: ("banana", "band"),
    5: ("app", "apple"),
    6: ("caterpillar", "cat"),
    7: ("zz", "aaaaa"),
    8: ("bbbbb", "a"),
    9: ("a", "b"),
    10: ("z", "y"),
    11: ("algorithm", "alphabet"),
    12: ("python", "python"),
    13: ("stepcode", "stepcoding"),
    14: ("a" * 100, "b" * 100),
    15: ("z" * 100, "z" * 99 + "a")
}

data1, data2 = test_cases.get(case_num, ("doing", "coding"))
print(f"{data1} {data2}")
