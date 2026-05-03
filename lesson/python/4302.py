#01
## 导入 wordcloud模块
from wordcloud import WordCloud
#02
## 导入 numpy模块
import numpy as np
#03
## 导入 PIL中的Image模块
from PIL import Image
#05
## 用with方式打开文件’Educated.txt’
with open("Educated.txt",'r',encoding='utf-8') as f:
    text = f.read()
#08
# 读取图片
img = Image.open('bird.png').convert('RGBA')
# 提取 Alpha 通道（透明度），透明的地方是 0，有线条的地方 > 0
mask_image = np.array(img.split()[-1])

# 将透明的地方变成 255（不画字），有线条和线条内部变成 0（画字）
# 注意：这需要你的鸟是一个闭合轮廓
mask_final = np.ones(mask_image.shape, dtype=np.uint8) * 255
mask_final[mask_image > 0] = 0 # 线条部分设为可画字区域

# 将处理后的数组传给 mask
mask_image = mask_final
#09
## 2. 创建词云对象
# 测试代码：不使用 mask
wc = WordCloud(
    background_color='white',
    mask=mask_image,
    max_words=100,
)
wc.generate(text)
wc.to_file('educated1.png')