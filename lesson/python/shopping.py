#01
##定义购物车类
class ShoppingCart:
#02
##构造方法
    def __init__(self):
#03
##初始化购物车列表
        self.items = []
#04
#05
##定义添加商品方法add_item
    def add_item(self, name, price, quantity=1):
#06
##向购物车列表中增加一个商品，字典类型，包含名称、价格、数量
        self.items.append([name, price, quantity])
#07
#08
##定义 __str__ 方法
    def __str__(self):
#09
        if not self.items:
            return "购物车是空的"
#10
        result = "购物车内容:\n"
        total = 0
#11
##遍历购物车
        for item in self.items:
#12
##计算每件商品的金额
            item_total = item[1] * item[2]
#13
##将当前商品信息编辑成字符串“商品名称 × 数量: ￥商品1总价”，添加到结果字符串result中
            result += f"{item[0]} * {item[2]}: ￥{item_total}"
#14
##计算总金额
            total += item_total
#15
#16
## 结果中增加总金额信息
            result += f"总计: ￥{total:.2f}" + "\n"
#17
## 返回result
        return result
#18
#19
##实例化一个购物车对象cart
cart = ShoppingCart()
#20
##往购物车增加商品：Python书籍，价格49.9，数量2本
cart.add_item("Python",49.9,2)
#21
##往购物车增加商品：鼠标，价格52，数量1
cart.add_item("Mouse",52,1)
#22
##输出购物车内容
print(cart.__str__())
