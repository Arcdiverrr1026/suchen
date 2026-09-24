import os

# Base Directories
data_dir = './data'

# 1. Custom Stopwords
with open(os.path.join(data_dir, 'stopwordsHIT.txt'), 'r', encoding='utf-8') as f:
    orig_stopwords = f.read().splitlines()
custom_stopwords = orig_stopwords + [
    '天问一号', '天问1号', '天问', '胖5', '时分', '火星', '探测', '任务', '着陆', '我国', '视频', '播放'
]
with open(os.path.join(data_dir, 'stopwords_custom.txt'), 'w', encoding='utf-8') as f:
    f.write('\n'.join(custom_stopwords))

# 2. Custom Positive Words
with open(os.path.join(data_dir, '正面评价词语（中文）.txt'), 'r', encoding='utf-8') as f:
    orig_pos = f.read().splitlines()
custom_pos = orig_pos + [
    '加油', '致敬', '骄傲', '自豪', '牛逼', '厉害', '震撼', '点赞', '厉害了', '起飞', '强盛', '伟大', '英雄', '泪目', '牛', '棒'
]
with open(os.path.join(data_dir, 'pos_custom.txt'), 'w', encoding='utf-8') as f:
    f.write('\n'.join(custom_pos))

# 3. Custom Negative Words
with open(os.path.join(data_dir, '负面评价词语（中文）.txt'), 'r', encoding='utf-8') as f:
    orig_neg = f.read().splitlines()
custom_neg = orig_neg + [
    '失望', '差劲', '垃圾', '不行', '失败', '难过', '伤心', '遗憾', '吐槽', '喷子', '黑子', '键盘侠', '悲哀', '可怜', '落后'
]
with open(os.path.join(data_dir, 'neg_custom.txt'), 'w', encoding='utf-8') as f:
    f.write('\n'.join(custom_neg))

# 4. Custom Negation Words
with open(os.path.join(data_dir, 'not.csv'), 'r', encoding='utf-8') as f:
    orig_not = f.read().splitlines()
custom_not = orig_not + [
    '不怎么', '毫无', '没有', '不是', '并没有', '未尝', '决不'
]
# Remove duplicates and keep order
seen = set()
custom_not = [x for x in custom_not if not (x in seen or seen.add(x))]
with open(os.path.join(data_dir, 'not_custom.csv'), 'w', encoding='utf-8') as f:
    f.write('\n'.join(custom_not))

print("Custom lexicons prepared successfully!")
