import sys

def main():
    raw = sys.stdin.read().split()
    t = int(raw[0])
    m = int(raw[1])

    time = []
    value = []
    idx = 1

    for _ in range(m):
        time.append(int(raw[idx + 1]))
        value.append(int(raw[idx + 2]))
        idx += 2

    dp = [0] * (t + 1)#几个单位时间内所能采到的草药的价值的记录账本
    dp[0] = 0

    for v in range(m):#遍历每种草药
        for i in range(t, time[v] - 1,-1):#剩余时间
            dp[i] = max(dp[i], dp[i - time[v]] + value[v])

    print(max(dp))

if __name__ == '__main__':
    main()








