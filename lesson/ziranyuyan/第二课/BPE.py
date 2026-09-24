# ==================================
# 通过python模拟BPE算法的基本流程
# ==================================

corpus = [
    "play",
    "play",
    "playing",
    "playing",
    "player"
]


# 函数1：将语料中的单词拆分成字符
def split_corpus(corpus):

    result = []

    for word in corpus:

        # 请补全：
        # 将单词拆分成字符列表，并添加到result中
        result.append(list(word))

    return result


# 函数2：合并指定的相邻字符或子词
def merge_pair(tokens, left, right):

    result = []
    i = 0

    while i < len(tokens):

        # 判断当前位置及其后一个位置能否合并
        if (
            i < len(tokens) - 1
            and tokens[i] == left
            and tokens[i + 1] == right
        ):

            # 合并两个相邻字符或子词
            result.append(left + right)

            # 一次处理两个符号
            i += 2

        else:

            # 当前符号不满足合并条件
            result.append(tokens[i])

            i += 1

    return result


# ========================
# 第一步：拆分语料
# ========================

tokenized_corpus = split_corpus(corpus)

print("初始语料：")

for tokens in tokenized_corpus:
    print(tokens)


# ========================
# 第二步：执行一次BPE合并
# ========================

print("\n合并高频字符对：p + l -> pl")

new_corpus = []

for tokens in tokenized_corpus:

    new_tokens = merge_pair(
        tokens,
        "p",
        "l"
    )

    new_corpus.append(new_tokens)


print("\n合并后的语料：")

for tokens in new_corpus:
    print(tokens)
