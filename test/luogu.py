#a, b = map(int, input().split())
#print(a + b)

#a,b = map(int, input().split())
#print(a*b)

#print(input()[1:][::-1])

#s = input().split()
#a = float(s[0])
#b = int(s[1])
#print(f"{a/b:.3f}\n{b*2}")

#s = input()
#print(s[::-1])

'''
a,b,c = map(float,input().split())
p = (a + b + c)/2
re = (p*(p-a)*(p-b)*(p-c))**0.5
print(f"{re:.1f}")
'''

'''
s,v = map(int,input().split())
costtim = (((s+v-1)//v) + 10)
starttim = ( 480 - costtim + 1440 ) % 1440
if starttim >= 0:
    print(f"{starttim//60:02d}:{starttim%60:02d}")
'''

'''
h,r = map(int,input().split())
botm = h*3.14*r**2
print(int((20000+botm-1)//botm))
'''

'''
a,b = map(int,input().split())
sum = a*10 + b
print(int(sum/19))
'''

'''
A,B,C = map(int,input().split())
print(A*0.2+B*0.3+C*0.5)
'''

'''
nums = int(input())

p1 = (nums % 2 == 0)
p2 = (4 < nums <= 12)

xiaoA = 1 if p1 and p2 else 0
Uim = 1 if p1 or p2 else 0
xiaoB = 1 if p1 != p2 else 0 #!=限制不同时成立
zhengmei = 1 if not p1 and not p2 else 0

print(f"{xiaoA} {Uim} {xiaoB} {zhengmei}")
'''

'''
nums = list(map(int,input().split()))
nums.sort()
a,b,c = nums

if a + b > c:
    if a**2 + b**2 == c**2:
        print("Right triangle")
    elif a**2 + b**2 > c**2:
        print("Acute triangle")
    elif a**2 + b**2 < c**2:
        print("Obtuse triangle")
    if a == b or b == c:
        print("Isosceles triangle")
    if a == c == b:
        print("Equilateral triangle")
else:
    print("Not triangle")
'''

'''
nums = [3,1,4,1,5,9,2,6]
p = [0]*(len(nums)+1)
for i in range(len(nums)):
    p[i+1] = nums[i] + p[i]
print(p[7]-p[2])
'''

'''
N,C = map(int,input().split())
nums = list(map(int,input().split()))

cout = 0
count_dict ={}

for num in nums:
    if num in count_dict:
        count_dict[num] += 1
    else:
        count_dict[num] = 1

for B in nums:
    A = B + C
    if A in count_dict:
        cout += count_dict[A]
print(cout)
'''

'''
cout = 0
for m in range(len(nums)):
    for n in range(len(nums)):
        if m == n:
            pass
        elif nums[m] - nums[n] == C:
            cout += 1
print(cout)
'''

'''
n = int(input())
a = list(map(int,input().split()))
Q = int(input())
for i in range(Q):
    m = int(input())
    for t in range(len(a)):
        if m == a[t]:
            print(t+1)
        elif m < a[t]:
            print(0)
'''

'''
n = int(input())
a = list(map(int,input().split()))

count_dict = {}
for i,num in enumerate(a):
    count_dict[num] = i + 1

Q = int(input())
for i in range(Q):
    m = int(input())
    print(count_dict.get(m,0))
'''

'''
n = int(input())
a = list(map(int,input().split()))

o = 0
count_dict = {}

for num in a:
    count_dict[num] = o
    o += 1

Q = int(input())
for i in range(Q):
    m = int(input())
    if m in count_dict:
        print(count_dict[m]+1)
    else:
        print(0)
'''

'''
import sys

def main():
    input = sys.stdin.readline

    n = int(input())
    a = list(map(int, input().split()))

    count_dict = {}
    
    for i, num in enumerate(a):
        count_dict[num] = i + 1

    ans = []
    Q = int(input())
    for i in range(Q):
        m = int(input())
        ans.append(str(count_dict.get(m, 0)))
    sys.stdout.write("\n".join(ans))

if __name__ == "__main__":
    main()
'''

'''
import sys

def main():
    input = sys.stdin.readline
    Q = int(input())

    xit = {}
    ans = []

    for _ in range(Q):
        P = input().split()
        op = P[0]

        if P[0] == "1":
            name = P[1]
            score = P[2]
            xit[name] = score
            ans.append("OK")
        elif P[0] == "2":
            if P[1] in xit:
                ans.append(xit[P[1]])
            else:
                ans.append("Not found")
        elif P[0] == "3":
            if P[1] in xit:
                xit.pop(P[1])
                ans.append("Deleted successfully")
            else:
                ans.append("Not found")
        elif P[0] == 4:
            ans.append(str(len(xit)))

    sys.stdout.write("\n".join(ans) + "\n")

if __name__ == "__main__":
    main()
'''

'''
import sys, bisect

def main():
    input = sys.stdin.readline
    m = int(input())

    #集合是无序的，列表是有序的，字典是无序但是有索引
    wood_set = set()#创建前台账单，只查找存不
    wood_list = []#创建仓库明细，只进行对比
    ans = []

    for _ in range(m):#进行多少次操作
        p = input().split()
        choic = p[0]
        leng = int(p[1])

        if choic == "1":
            if leng in wood_set:
                ans.append("Already Exist")
            else:
                wood_set.add(leng)#先进前台
                bisect.insort(wood_list, leng)#确认仓库位置

        elif choic == "2":
            if not wood_set:#判断仓库是否为空（此处分为3种情况：为空，有货，有货但不匹配）
                ans.append("Empty")

            elif leng in wood_set:
                remove_idx = bisect.bisect_left(wood_list, leng)#确认取货位置，使用社恐避免超限
                ans.append(str(leng))
                wood_set.remove(leng)#清账单
                del wood_list[remove_idx]#取货

            else:
                idx = bisect.bisect_left(wood_list, leng)#探测仓库位置
                left_idx = idx - 1
                right_idx = idx

                #首先先处理边界值
                if idx == 0:
                    remove_idx = 0
                elif idx == len(wood_list):
                    remove_idx = len(wood_list) - 1
                elif leng - wood_list[left_idx] <= wood_list[right_idx] - leng:
                    remove_idx = left_idx
                else:
                    remove_idx = right_idx

                ans.append(str(wood_list[remove_idx]))
                wood_set.remove(wood_list[remove_idx])#取货
                del wood_list[remove_idx]#清账单

    sys.stdout.write("\n".join(ans)+"\n")

if __name__ == "__main__":
    main()
'''

'''
import sys

def main():  # 双模板对比法
    input = sys.stdin.readline
    T = int(input())

    ans = []

    for _ in range(T):
        n = int(input())
        nums = list(input().strip())

        diff_1 = 0
        diff_2 = 0

        for i, char in enumerate(nums):

            expect_char_1 = "A" if i % 2 == 0 else "B"
            if char != expect_char_1:
                diff_1 += 1

            expect_char_2 = "B" if i % 2 == 0 else "A"
            if char != expect_char_2:
                diff_2 += 1

        ans.append(str(int(min(diff_1, diff_2)/2)))

    sys.stdout.write("\n".join(ans) + "\n")


if __name__ == "__main__":
    main()
'''

'''
import sys

def main():  # 双模板对比法
    input = sys.stdin.readline
    T = int(input())
    ans = []

    for _ in range(T):
        n = int(input())
        nums = input().strip()

        diff_1 = 0
        diff_2 = 0

        for i in range(0, len(nums), 2):
            if nums[i] != "A":
                diff_1 += 1

            if nums[i] != "B":
                diff_2 += 1

        ans.append(str(min(diff_1, diff_2)))
    sys.stdout.write("\n".join(ans) + "\n")

if __name__ == "__main__":
    main()
'''

'''
import sys

def main():
    input = sys.stdin.readline
    n = int(input())
    nums = list(map(int, input().split()))
    ans = []
    num_list = []

    for i in range(n):
        num_list[i + 1] = nums[i] + num_list[i]

    m = int(input())

    for _ in range(m):
        l, r = map(int, input().split())
        ans.append(str(num_list[r] - num_list[l - 1]))

    sys.stdout.write("\n".join(ans) + "\n")

if __name__ == "__main__":
    main()
'''

'''
import sys

def main():
    input_data = sys.stdin.read().split()
    ans = []

    lite = iter(input_data)

    n = int(next(lite))
    k = int(next(lite))
    q = int(next(lite))

    max_temp = 200000
    diff = [0] * (max_temp + 5)

    for _ in range(n):
        l = int(next(lite))
        r = int(next(lite))
        diff[l] += 1
        diff[r + 1] -= 1
        # 标记区间

    valid = [0] * (max_temp + 1)
    current_vote = 0

    for i in range(1, max_temp + 1):
        # 补完区间真实标记
        current_vote += diff[i]
        # 标记后判断是否达标
        is_acceptable = 1 if current_vote >= k else 0
        valid[i] = valid[i - 1] + is_acceptable

    for _ in range(q):
        a = int(next(lite))
        b = int(next(lite))
        count = valid[b] - valid[a - 1]
        ans.append(str(count))

    sys.stdout.write("\n".join(ans) + "\n")


if __name__ == "__main__":
    main()
'''

'''
import sys

def main():
    input = sys.stdin.readline
    N, K = map(int, input().split())
    ans = []

    list = [0] * (N + 5)

    for i in range(1, N + 1):
        list[i] = int(input())

    sum = [0] * (N + 5)
    for i in range(1,N + 1):
        sum[i] = sum[i - 1] + list[i]

    count = 0
    for i in range(1,N + 1):
        for m in range(i,N + 1):
            if (sum[m] - sum[i -1]) % K == 0:
                count += 1
    ans.append(str(count))
    sys.stdout.write("\n".join(ans) + "\n")

if __name__ == "__main__":
    main()    超时了
'''

'''
import sys

def main():
    input = sys.stdin.readline
    n = int(input())

    ans = []
    path = []

    def dfs(depth, current_sum):
        remain = 10 - depth

        if current_sum + remain * 1 > n or current_sum + remain * 3 < n:
            return

        if depth == 10:
            if current_sum == n:
                ans.append(" ".join(map(str, path)))
            return

        for i in range(1, 4):
            path.append(i)
            dfs(depth + 1, current_sum + i)
            path.pop()

    dfs(0, 0)

    sys.stdout.write(str(len(ans)) + "\n")

    if ans:
        sys.stdout.write("\n".join(ans) + "\n")

if __name__ == "__main__":
    main()
'''

'''
import sys

def main():
    input = sys.stdin.readline
    n = int(input())

    ans = []
    path = []

    def dfs(n, depth):
        if depth == n:
            ans.append("\n".join(map(str, path)))
            return

        for j in range(0, n + 1):
            if j in path:
                j += 1

            path.append(j)
            dfs(n, depth + 1)
            path.pop()

    pop(n, 0)

    if ans:
        sys.stdout.write(" ".join(ans) + "\n")


if __name__ == "__main__":
    main()
'''

'''
import sys

def main():
    input = sys.stdin.readline
    n = int(input())

    ans = []
    path = []
    
    def dfs(n,depth):
        if depth == n:
            ans.append(" ".join(map(str,path)))
            return

        for j in range(1,n+1):
            if j in path:
                continue
    
            path.append(j)
            dfs(n,depth+1)
            path.pop()
        
    dfs(n,0)

    if ans:
        sys.stdout.write("\n".join(ans)+"\n")
        
if __name__ == "__main__":
    main()
'''

'''
import sys

def main():
    input = sys.stdin.readline
    n, k = map(int, input().split())

    ans = []
    path = []

    def dfs(depth, k, star_index, n):
        if depth == k:
            ans.append(str(path))
            return

        for i in range(star_index, n + 1):
            path.append(i)
            dfs(depth + 1, k, star_index + 1, n)
            path.pop()

    dfs(0, k, 1, n)

    if ans:
        sys.stdout.write("\n".join(ans) + "\n")


if __name__ == "__main__":
    main()
'''

'''
import sys

def main():
    input = sys.stdin.readline
    N, M = map(int, input().split())
    maze = [input().split() for _ in range(N)]

    ans = 0

    start_x = 0
    start_y = 0

    for i in range(N):
        for j in range(M):
            if maze[i][j] == 'S':
                start_x = i
                start_y = j
                break

    visited = [[False] * M for _ in range(N)]

    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]

    def dfs(x, y):
        nonlocal ans

        if maze[x][y] == "E":
            ans += 1
            return

        if maze[x][y] == "#":
            return

        for dx, dy in directions:
            nx = x + dx
            ny = y + dy

            if 0 <= nx < N and 0 <= ny < M and maze[nx][ny] != "#" and not visited[nx][ny]:
                visited[nx][ny] = True
                dfs(nx, ny)
                visited[nx][ny] = False

    visited[start_x][start_y] = True
    dfs(start_x, start_y)

    sys.stdout.write(f"总共有 {ans} 条路走到终点\n")

if __name__ == "__main__":
    main()
'''
'''
import sys

def main():
    input = sys.stdin.readline
    raw = input().split()
    if not raw:
        return
    a, b, c = map(int, raw)

    ans = []
    d = []
    visited = [False] * 10
    has_answer = False

    def dfs(depth):
        nonlocal has_answer

        if depth == 9:
            num1 = d[0] * 100 + d[1] * 10 + d[2]
            num2 = d[3] * 100 + d[4] * 10 + d[5]
            num3 = d[6] * 100 + d[7] * 10 + d[8]
            if num1 * b == num2 * a and num1 * c == num3 * a:
                ans.append(f"{num1} {num2} {num3}")
                has_answer = True
                return

        for i in range(1, 10):
            if not visited[i]:
                d.append(i)
                visited[i] = True
                dfs(depth + 1)
                d.pop()
                visited[i] = False

    dfs(0)

    if not has_answer:
        ans.append("No!!!")

    sys.stdout.write("\n".join(ans) + "\n")

if __name__ == "__main__":
    main()
'''

'''
import sys

def main():
    input = sys.stdin.readline
    n, k = map(int, input().split())
    list_a = input().split()
    sum_1 = 0
    cout = 0

    def dfs(depth):
        nonlocal cout, sum_1

        if depth == k:
            for i in range(2, sum_1):
                if sum_1 % i == 0:
                    depth -= 1
                    return
                else:
                    cout += 1

        for i in range(n):
            sum_1 += int(list_a[i])
            dfs(depth + 1)
            sum_1 -= int(list_a[i])

    dfs(0)
    sys.stdout.write(str(cout))


if __name__ == "__main__":
    main()
'''
'''
import sys

def main():
    input = sys.stdin.readline
    n, r = map(int, input().split())

    path = []
    ans = []

    def dfs(depth,start_index):
        if depth == r:
            ans.append("".join(f"{x:>3}" for x in path))
            return

        for i in range(start_index, n + 1):
                path.append(i)
                dfs(depth + 1,i+1)
                path.pop()

    dfs(0,1)

    sys.stdout.write("\n".join(ans) + "\n")

if __name__ == "__main__":
    main()
'''

'''
import sys

def main():
    input = sys.stdin.readline
    n = int(input())

    ans = []
    path = []
    visited = [False] * (n + 5)

    def dfs(depth):
        if depth == n:
            ans.append("".join(f"{x:>5}" for x in path))
            return

        for i in range(1, n + 1):
            if not visited[i]:
                path.append(i)
                visited[i] = True
                dfs(depth + 1)
                path.pop()
                visited[i] = False

    dfs(0)

    sys.stdout.write("\n".join(ans) + "\n")

if __name__ == "__main__":
    main()
'''

'''
import sys

def main():
    input = sys.stdin.readline
    n = int(input())
    m = int(input())
    a_list = list(map(int,input().split()))

    ans = []
    path = []
    visited = [False] * (n + 5)

    def dfs(depth):
        if depth == n:
            ans.append("".join(f"{x}" for x in path))
            return

        for i in a_list:
            if not visited[i]:
                path.append(i)
                visited[i] = True
                dfs(depth+1)
                path.pop()
                visited[i] = False

    dfs(0)
    sys.stdout.write(" ".join(ans[m]))

if __name__ == "__main__":
    main()
'''

'''
import sys


def main():
    input = sys.stdin.readline
    n = int(input())

    team = input().split()

    cha = team[:]

    team.sort()

    for item in team:

        pass


if __name__ == "__main__":
    main()
'''

'''
import sys

def main():
    raw_data = sys.stdin.read().split()
    n = int(raw_data[0])

    count, shu = 0, 0
    for i in range(n - 1, 1, -1):
        if int(raw_data[i]) < int(raw_data[i - 1]):
            count = 0
        else:
            count += 1

    shu = (count + 1) / 2
    print(str(shu))

if __name__ == "__main__":
    main()
'''

# 任意两个相邻的盒子中糖的个数之和都不大于 x，至少得吃掉几颗糖
# 1.先吃最多的
# 2.超过指定数值的盒子内的糖果必须降到要求水平
# 3.两两之间不超过要求水平

'''
import sys


def main():
    raw_data = sys.stdin.read().split()
    n = int(raw_data[0])
    x = int(raw_data[1])

    surbox = [int(i) for i in raw_data[2:n+2]]

    count = 0
    for i in range(n-1):#留一个最后一位
        if surbox[i] + surbox[i+1] > x:
            eat = surbox[i] + surbox[i+1] - x
            count += eat

            #优先处理右边
            if surbox[i+1] > eat:
                surbox[i+1] = surbox[i+1] - eat
            else:
                surbox[i+1] = 0
                eat += x - surbox[i+1]

    sys.stdout.write(str(count))


if __name__ == "__main__":
    main()
'''
'''
import sys

def main():
    raw_data = sys.stdin.read().split()
    n = int(raw_data[0])
    s = int(raw_data[1])
    a = int(raw_data[2])
    b = int(raw_data[3])

    idx = 4
    apple = []
    for _ in range(n):
        height = int(raw_data[idx])
        strength = int(raw_data[idx+1])
        apple.append((height,strength))
        idx += 2

    apple.sort(key = lambda x:x[1])
    count = 0

    for height,strength in apple:
        if s != 0 and x <= a + b:
            s -= strength
            count += 1

    sys.stdout.write(str(count))

if __name__ == "__main__":
    main()
'''
'''
import sys


def main():
    raw = sys.stdin.read().split()
    w = int(raw[0])
    n = int(raw[1])

    gift = [int(x) for x in raw[2:n + 2]]
    gift.sort(reverse = True)

    count = 0
    left = 0
    right = n - 1

    while right >= left:
        if right == left:
            count += 1
            break

        if gift[left] + gift[right] <= w:
            count += 1
            left += 1
            right -= 1
        else:
            left += 1
            count += 1

    sys.stdout.write(str(count))

if __name__ == "__main__":
    main()
'''
'''
import sys
import bisect

def main():
    raw = sys.stdin.read().split()
    m,n = map(int,raw[:2])
    school = list(map(int,raw[2:2+m]))
    school.sort()
    score = list(map(int,raw[2+m:]))
    sati = 0

    for s in score:
        pos = bisect.bisect_left(school,s)#该点为插入点
        if pos == 0:
            sati += abs(school[pos] - s)
        if pos == m:
            sati += abs(s - school[pos - 1])
        if 0 < pos < m:
            d1 = abs(school[pos] - s)
            d2 = abs(s - school[pos - 1])
            sati += min(d1, d2)

    sys.stdout.write(str(sati))

if __name__ == "__main__":
    main()
'''
'''
import sys


def main():
    raw = sys.stdin.read().split()
    n, x = map(int, raw[:2])

    idx = 2
    enemy = []

    for _ in range(n):
        lost = int(raw[idx])
        win = int(raw[idx + 1])
        use = int(raw[idx + 2])
        enemy.append((lost, win, use))
        idx += 3

    dp = [0] * n  # 记录经验累积

    for lost, win, use in enemy:
        for i in range(x, use - 1, -1):
            dp[i] = max(dp[i - use] + lost, dp[i - use] + win)

    print(dp[x])


if __name__ == "__main__":
    main()
'''
'''
w,h,v = map(int,input().split())

for i in range(h + w):
    if i <= h:
        print('Q' for _ in range(w))
        print()
    if i > h:
        print('Q' for _ in range(w+v))
        print()
'''
'''
import sys

def main():
    raw = sys.stdin.read().split()
    n = int(raw[0])
    trees = [int(x) for x in raw[1:n + 1]]

    if n == 1:
        print(n)
        return

    top = 0

    for betw in range(n):
        dp = [1] * n

        for i in range(betw, n):
            if trees[i] >= trees[i - betw]:
                dp[i] = dp[i - betw] + 1
            else:
                top = dp[i]

    sys.stdout.write(str(top))

if __name__ == "__main__":
    main()
'''
'''
import sys
from datetime import datetime,timedelta

def main():
    lines = sys.stdin.read().splitlines()
    t = int(lines[0])

    start = datetime(1970,1,1,0,0,0)

    idx = 1
    for _ in range(t):
        time = lines[idx]
        dead_time = datetime.strptime(time[:19],"%Y-%m-%d %H:%M:%S")
        x = int(time[19:].strip())
        idx += 1
        during = (dead_time - start).total_seconds()
        total_min = int(during // 60)
        alarm_min = (total_min // x) * x
        during = timedelta(minutes=alarm_min)
        target_time = start + during

        print(target_time.strftime("%Y-%m-%d %H:%M:%S"))

if __name__ == "__main__":
    main()
'''

'''
import sys

def isgm(x):
    str_1 = str(x)
    if "0" in str_1 or "2" in str_1 or "4" in str_1:
        return True
    return False

def main():
    data = sys.stdin.read().split()
    n = int(data[0])

    s_stones = data[1:n+1]
    t_stones = data[n+1:2 * n+1]

    max_s = 0
    max_t = 0

    for i in range(n):
        valid_s = isgm(s_stones[i])
        valid_t = isgm(t_stones[i])

        next_s = max_s
        next_t = max_t

        if valid_s:
            next_s = max(next_s, max_t + 1)

        if valid_t:
            if max_s > 0:
                next_t = max(next_t, max_s + 1)

        max_s = next_s
        max_t = next_t

    print(max(max_s,max_t))

if __name__ == "__main__":
    main()
'''





