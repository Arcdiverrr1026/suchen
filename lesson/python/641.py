studs= [
    {'sid':'103', 'Chinese': 90, 'Math':95, 'English':92},
    {'sid':'101', 'Chinese': 80, 'Math':85, 'English':82},
    {'sid':'102', 'Chinese': 70, 'Math':75, 'English':72}
]

scores = {}

for s in studs:
    scores[s['sid']] = {'Chinese': s['Chinese'], 'Math': s['Math'], 'English': s['English']}

for s in sorted(scores.keys()):
    print(f"{s} {scores[s]['Chinese']} {scores[s]['Math']} {scores[s]['English']}")


import random

verification_code = ""
for i in range(4):
    num = random.randrange(0, 36)
    if num < 10:
        verification_code += str(num)
    else:
        verification_code += chr(ord('A') + (num - 10))
print(f"验证码：{verification_code}")