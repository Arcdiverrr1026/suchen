# 导入所需库
from py2neo import Graph, Node, Relationship
import pandas as pd

# 1. 连接Neo4j数据库（修改密码为自己设置的Neo4j密码）
graph = Graph(
    "bolt://localhost:7687",  # Neo4j默认连接地址
    auth=("neo4j", "12345678")  # 用户名：neo4j，密码：自己修改的密码
)

# 2. 清空数据库（谨慎使用！用于重新导入数据，避免重复）
graph.run("MATCH (n) DETACH DELETE n")

# 3. 读取CSV文件（修改为自己的Neo4j import文件夹路径）
import_path = "D:/Neo4j/neo4j-community-2026.02.2-windows/import/"
acupoints_df = pd.read_csv(import_path + "acupoints.csv", encoding="utf-8")
meridians_df = pd.read_csv(import_path + "meridians.csv", encoding="utf-8")
diseases_df = pd.read_csv(import_path + "diseases.csv", encoding="utf-8")
relations_df = pd.read_csv(import_path + "relations.csv", encoding="utf-8")
# 4. 批量创建Acupoint节点
for index, row in acupoints_df.iterrows():
    acupoint_node = Node(
        "Acupoint",
        id=int(row["id"]),  # 修正：将id转为整数，与CSV数据类型一致
        name=row["name"],
        location=row["location"],
        effect=row["effect"],
        category=row["category"]
    )
    graph.create(acupoint_node)
print("Acupoint节点批量创建完成！")

# 5. 批量创建Meridian节点
for index, row in meridians_df.iterrows():
    meridian_node = Node(
        "Meridian",
        id=int(row["id"]),  # 修正：将id转为整数
        name=row["name"],
        nature=row["nature"],
        distribution=row["distribution"]
    )
    graph.create(meridian_node)
print("Meridian节点批量创建完成！")

# 6. 批量创建Disease节点
for index, row in diseases_df.iterrows():
    disease_node = Node(
        "Disease",
        id=int(row["id"]),  # 修正：将id转为整数
        name=row["name"],
        symptom=row["symptom"],
        etiology=row["etiology"]
    )
    graph.create(disease_node)
print("Disease节点批量创建完成！")


#7. 批量创建关系（修正：匹配节点时，id需转为整数，与节点id类型一致）
for index, row in relations_df.iterrows():
    # 查找源节点和目标节点（修正：将csv中的id转为整数，避免类型不匹配）
    source_node = graph.nodes.match(id=int(row["source_id"])).first()
    target_node = graph.nodes.match(id=int(row["target_id"])).first()
    # 获取关系类型和属性
    relation_type = row["relation_type"]
    property_key = row["property_key"]
    property_value = row["property_value"]
    # 处理属性值类型（修正：穴位排序转为整数，其余为字符串，贴合实际需求）
    if property_key == "acupoint_order":
        property_value = int(property_value)
    # 创建关系（添加属性）
    relation = Relationship(source_node, relation_type, target_node, **{property_key: property_value})
    # 将关系添加到Neo4j中
    graph.create(relation)
print("关系批量创建完成！")

# 8. 验证导入结果
print("验证导入结果：")
result = graph.run("MATCH (a:Acupoint)-[:TREATS]->(d:Disease) RETURN a.name, d.name LIMIT 5")
for record in result:
    print(f"{record['a.name']} 治疗 {record['d.name']}")