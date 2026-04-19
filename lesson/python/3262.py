import sys
def main():
    raw = sys.stdin.read().split()
    n = int(raw[0])
    m = int(raw[1])
    area = []
    idx = 1

    for _ in range(n):
        area.append("".join(raw[1 + idx] for _ in range(m)))

    print(area)

if __name__ == '__main__':
    main()