class AcupunctureProductionSystem:
    def __init__(self):
        self.facts = {}  # 综合数据库：{症状: 置信度}
        self.rules = []  # 规则库：[{condition: 函数, conclusion: 穴位, confidence: 规则置信度}]

    def add_fact(self, symptom, confidence=1.0):
        """添加患者症状及置信度"""
        self.facts[symptom] = confidence
        print(f"患者症状 => {symptom} (置信度: {confidence})")

    def add_rule(self, condition, acupoint, rule_confidence=1.0):
        """添加规则：condition为症状检查函数，acupoint为推荐穴位"""
        self.rules.append({
            "condition": condition,
            "acupoint": acupoint,
            "rule_confidence": rule_confidence
        })
        print(f"规则库 <= IF {condition.__name__} THEN {acupoint} (规则置信度: {rule_confidence})")

    def run(self):
        """执行推理：计算穴位推荐置信度"""
        print("\n开始推理...")

        # ======== 修改部分 3：冲突消解策略 ========
        # 针对题目3：在遍历执行规则前，按规则本身的置信度（rule_confidence）降序排序，
        # 确保置信度高的规则（如0.95）优先于置信度低的规则（如0.9或0.8）执行。
        self.rules.sort(key=lambda x: x["rule_confidence"], reverse=True)
        # ==========================================

        changed = True
        while changed:
            changed = False
            for rule in self.rules:

                # ======== 修改部分 1：置信度计算优化 ========
                # 针对题目1：原代码在处理多条件（头痛且牙痛）时取最小值逻辑有缺陷。
                # 修改方案：直接让 condition 函数去计算并返回症状最终的置信度（即多个条件中的最小值）。
                # 如果不满足条件，condition 返回 0.0。
                symptom_confidence = rule["condition"](self.facts)

                if symptom_confidence > 0:
                    # 结论置信度 = 规则置信度 × 症状置信度（取最小值逻辑已在条件函数内完成）
                    new_confidence = rule["rule_confidence"] * symptom_confidence
                    current_confidence = self.facts.get(rule["acupoint"], 0)

                    # 若新置信度更高，则更新推荐结果
                    if new_confidence > current_confidence:
                        self.facts[rule["acupoint"]] = new_confidence
                        print(f"推荐穴位 => {rule['acupoint']} (置信度: {new_confidence:.2f})")
                        changed = True
                # ==========================================

        print("推理结束。")

    def print_recommendations(self):
        """打印穴位推荐结果"""
        print("\n最终穴位推荐:")
        for item in self.facts.items():
            # ======== 修改部分：打印过滤逻辑 ========
            # 将新加入的症状（牙痛、鼻塞、流涕）也加入排除列表，保证最后只打印穴位
            if item[0] not in ["头痛", "便秘", "胃痛", "牙痛", "鼻塞", "流涕"]:
                print(f"  - {item[0]}: {item[1]:.2f}")
            # ========================================


# 初始化系统
aps = AcupunctureProductionSystem()


# ======== 修改部分：重写原有的单症状检查函数 ========
# 为了适配优化后的 run 方法，单症状判断也不再返回 True/False，而是直接返回该症状的置信度
def has_headache(facts):
    return facts["头痛"] if "头痛" in facts and facts["头痛"] > 0.5 else 0.0


def has_constipation(facts):
    return facts["便秘"] if "便秘" in facts and facts["便秘"] > 0.5 else 0.0


def has_stomachache(facts):
    return facts["胃痛"] if "胃痛" in facts and facts["胃痛"] > 0.5 else 0.0


# ====================================================

# ======== 修改部分 1：实现多条件（头痛且牙痛）函数 ========
def has_headache_and_toothache(facts):
    """题目1：若同时有头痛和牙痛，返回两者中置信度较小的那个"""
    if "头痛" in facts and "牙痛" in facts and facts["头痛"] > 0.5 and facts["牙痛"] > 0.5:
        return min(facts["头痛"], facts["牙痛"])
    return 0.0


# ==========================================================

# ======== 修改部分 2：实现新规则（鼻塞且流涕）函数 ========
def has_stuffy_and_runny_nose(facts):
    """题目2：若同时有鼻塞和流涕，返回两者中置信度较小的那个"""
    if "鼻塞" in facts and "流涕" in facts and facts["鼻塞"] > 0.5 and facts["流涕"] > 0.5:
        return min(facts["鼻塞"], facts["流涕"])
    return 0.0


# ==========================================================


# 添加原有针灸规则
aps.add_rule(has_headache, "合谷", 0.9)
aps.add_rule(has_constipation, "合谷", 0.8)
aps.add_rule(has_stomachache, "足三里", 0.95)

# ======== 修改部分：将新规则加入规则库 ========
aps.add_rule(has_headache_and_toothache, "合谷", 0.9)  # 题目1规则
aps.add_rule(has_stuffy_and_runny_nose, "风池", 0.85)  # 题目2规则
# ==============================================


print("\n--- 录入患者症状 ---")
# 原有症状
aps.add_fact("头痛", 0.8)
aps.add_fact("便秘", 0.7)
aps.add_fact("胃痛", 0.9)

# ======== 修改部分：录入题目要求的新事实 ========
aps.add_fact("牙痛", 0.6)  # 配合题目1
aps.add_fact("鼻塞", 0.8)  # 配合题目2
aps.add_fact("流涕", 0.7)  # 配合题目2
# ================================================

# 执行推理
aps.run()
aps.print_recommendations()