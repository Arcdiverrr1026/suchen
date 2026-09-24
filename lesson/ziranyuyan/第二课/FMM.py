# ==================================
# 前向最大匹配算法 FMM
# 输出候选匹配过程
# ==================================

# 词典
dictionary = {
    "生成式",
    "生成",
    "人工智能",
    "人工",
    "智能",
    "正在",
    "改变",
    "大学课堂",
    "大学",
    "课堂"
}


# Set the maximum length of words in the dictionary
max_len = max(len(word) for word in dictionary)

def FMM(sentence, dictionary, max_len):

    result = []
    start = 0

    while start < len(sentence):
        # 从当前位置开始，优先尝试最长的候选词。
        candidate_length = min(max_len, len(sentence) - start)

        while candidate_length > 0:
            candidate = sentence[start:start + candidate_length]

            if candidate in dictionary:
                result.append(candidate)
                start += candidate_length
                break

            candidate_length -= 1
        else:
            # 没有候选词匹配时，保留当前字符，避免无法继续向前扫描。
            result.append(sentence[start])
            start += 1

    return result



# ===================
# 测试
# ===================

sentence = "生成式人工智能正在改变大学课堂"


print("原文本：", sentence)


result = FMM(
    sentence,
    dictionary,
    max_len
)


print("\n===================")
print("最终分词结果：")

print(" / ".join(result))
