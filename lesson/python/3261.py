data = """
9.30, 9.00, 9.00, 9.00, 10.00, 9.30, 9.60, 9.40
9.90, 9.60, 9.40, 9.00, 9.70, 9.20, 9.40, 9.20
9.30, 10.00, 9.90, 9.50, 10.00, 10.00, 9.80, 9.40
9.00, 9.10, 9.80, 9.30, 9.30, 9.10, 9.90, 9.60
9.90, 9.00, 9.10, 9.80, 10.00, 9.10, 9.50, 9.20
"""

lines = data.strip().split('\n')

for line in lines:
    scores = [float(s) for s in line.split(',')]

    total_score = sum(scores)
    max_score = max(scores)
    min_score = min(scores)

    average = (total_score - max_score - min_score) / 6

    print(f"{average:.2f}")