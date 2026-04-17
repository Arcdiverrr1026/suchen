class KnowledgeBase:
    def __init__(self):
        self.facts = []  # 存储事实，如"属于(合谷, 大肠经)"
        self.rules = []  # 存储规则函数

    def add_fact(self, fact):
        if fact not in self.facts:
            self.facts.append(fact)
            print(f"添加事实: {fact}")

    def add_rule(self, rule_func):
        self.rules.append(rule_func)
        print(f"添加规则: {rule_func.__name__}")

    def infer(self):
        """前向链推理：不断应用规则推导新事实"""
        new_facts_discovered = True
        while new_facts_discovered:
            new_facts_discovered = False
            for rule in self.rules:
                new_fact = rule(self)
                if new_fact and new_fact not in self.facts:
                    self.add_fact(new_fact)
                    new_facts_discovered = True
        print("推理结束。")

    def print_facts(self):
        print("\n当前知识库事实:")
        for fact in self.facts:
            print(f"  - {fact}")
# 初始化针灸知识库
kb = KnowledgeBase()

# 添加已知事实：穴位-经络关系、穴位-症状关系
kb.add_fact("属于(合谷, 大肠经)") # 合谷穴属于手阳明大肠经
kb.add_fact("主治(合谷, 头痛)") # 合谷穴主治头痛
kb.add_fact("属于(足三里, 胃经)") # 足三里属于足阳明胃经\

def rule_colon_meridian_treat_constipation(kb):
    """规则1：所有属于大肠经的穴位可主治便秘"""
    for fact in kb.facts:
        if fact.startswith("属于(") and "大肠经" in fact:
            # 提取穴位名称，如从"属于(合谷, 大肠经)"中提取"合谷"
            acupoint = fact.split(",")[0].split("(")[1]
            new_fact = f"主治({acupoint}, 便秘)"
            if new_fact not in kb.facts:
                return new_fact
    return None

def rule_stomach_meridian_treat_stomachache(kb):
    """规则2：所有属于胃经的穴位可主治胃痛"""
    for fact in kb.facts:
        if fact.startswith("属于(") and "胃经" in fact:
            acupoint = fact.split(",")[0].split("(")[1]
            new_fact = f"主治({acupoint}, 胃痛)"
            if new_fact not in kb.facts:
                return new_fact
    return None

# 添加规则到知识库
kb.add_rule(rule_colon_meridian_treat_constipation)
kb.add_rule(rule_stomach_meridian_treat_stomachache)

print("\n开始推理...")
kb.infer()
kb.print_facts()