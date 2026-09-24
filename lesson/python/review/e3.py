import random as r

WORDS = ('easy','during','apple','orange','pink','python','dog')

is_continue = 'Y'
while is_continue in ['y','Y','YES','yes']:
    correct = r.choice(WORDS)
    scrambled_word = ''.join(r.sample(correct,len(correct)))
    print(f"打乱顺序后的单词字母是：{scrambled_word}\n")
    count = 0
    guess = input('请输入你猜测的单词：')
    while guess != correct:
        print('不要灰心，再来一次')
        count = count + 1
        guess = input('请输入你猜测的单词：')
    if guess == correct:
        print('恭喜你，猜对了')
        count = count + 1
        print('一共猜了%d次'%count)
    is_continue= input('\n\n还想再玩一次吗？(Y/N)')
