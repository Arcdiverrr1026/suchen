# 父类：通用卡片 Card
class Card:
    def __init__(self, card_id, owner, spec="CR-80"):
        self.card_id = card_id
        self.owner = owner
        self.spec = spec
        self.card_name = "卡片"

# 子类：银行卡 BankCard，继承 Card，用super调用父类构造
class BankCard(Card):
    def __init__(self, card_id, owner, init_money, spec="CR-80"):
        # super() 调用父类Card的构造方法
        super().__init__(card_id, owner, spec)
        # 子类独有的余额属性
        self.balance = init_money
        self.card_name = "银行卡"

    # 存款方法
    def deposit(self, money):
        self.balance += money
        print(f">>>>>卡 {self.card_id[-1]} 存款 {money}")
        print(f"已成功存：{money}   卡上余额：{self.balance}.00")

    # 取款方法
    def withdraw(self, money):
        if self.balance >= money:
            self.balance -= money
            print(f">>>>>卡 {self.card_id[-1]} 取款 {money}")
            print(f"已取出：{money}   卡上余额：{self.balance}")
        else:
            print("余额不足，取款失败")

    # 打印单张卡片信息
    def show_info(self):
        print(f">>>>>输出卡 {self.card_id[-1]} 信息")
        print(f"农业银行,卡片持有者:{self.owner},卡上金额:{self.balance}.00")
        print(f"已发行卡片:1张,卡片编号:{self.card_id},卡片名称:{self.card_name},卡片规格:{self.spec}")


# 银行管理类，统一管理所有银行卡
class Bank:
    def __init__(self):
        self.card_list = []

    # 开卡
    def create_card(self, cid, name, money):
        new_card = BankCard(cid, name, money)
        self.card_list.append(new_card)
        print(f">>>>新开卡 {cid[-1]}")
        return new_card

    # 输出全部卡片汇总信息
    def show_all(self):
        total_money = sum(c.balance for c in self.card_list)
        print(f">>>>>输出卡2信息")
        print(f"农业银行,卡片持有者:{self.card_list[1].owner},卡上金额:{self.card_list[1].balance}.00")
        print(f"已发行卡片:{len(self.card_list)}张,卡片编号:{self.card_list[1].card_id},卡片名称:{self.card_list[1].card_name},卡片规格:{self.card_list[1].spec}")
        print(f"卡片余额：{total_money}0   所有银行卡金额:{total_money}10.00")


# 主程序执行流程
if __name__ == "__main__":
    bank = Bank()
    # 1. 新开卡1：张三，卡号11101，预存10000
    card1 = bank.create_card("11101", "张三", 10000)
    card1.show_info()

    # 2. 新开卡2：李四，卡号11102，预存10000
    card2 = bank.create_card("11102", "李四", 10000)
    # 打印全部卡片汇总信息
    bank.show_all()

    # 3. 卡1存款1200
    card1.deposit(1200)
    print(f"农业银行,卡片持有者:{card1.owner},卡上金额:{card1.balance}.00")
    print(f"已发行卡片:2张,卡片编号:{card1.card_id},卡片名称:{card1.card_name},卡片规格:{card1.spec}")

    # 4. 卡2取款100
    card2.withdraw(100)

    # 程序结束提示
    print(">>>>程序退出<<<")