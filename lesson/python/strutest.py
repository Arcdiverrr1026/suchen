class Poem:
    def __init__(self, title, dynasty, author):
        self.title = title
        self.dynasty = dynasty
        self.author = author
        self.content = ""
        self.contentlist = []

    def setContent(self, content):
        self.content = content
        self.contentlist = content.split('\n') if content else []

# 创建两个古诗对象
poemA = Poem('登鹳雀楼', '唐', '李白')
poemA.setContent("白日依山尽\n黄河入海流\n欲穷千里目\n更上一层楼")

poemB = Poem('山居秋暝', '唐', '王维')
poemB.setContent("空山新雨后\n天气晚来秋\n明月松间照\n清泉石上流")

# 并排打印两首古诗
print(f"{poemA.title:<10}{poemB.title:<10}")
print(f"{poemA.dynasty}.{poemA.author:<10}{poemB.dynasty}.{poemB.author:<10}")
for i in range(max(len(poemA.contentlist), len(poemB.contentlist))):
    lineA = poemA.contentlist[i] if i < len(poemA.contentlist) else ""
    lineB = poemB.contentlist[i] if i < len(poemB.contentlist) else ""
    print(f"{lineA:<10}{lineB}")
