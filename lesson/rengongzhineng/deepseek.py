import requests
import json
import os
import random  # 新增：引入 random 模块用于控制生成的多样性（温度和风格的随机选择）
from typing import Dict, Any, Optional, List  # 修改：导入 List 用于类型注解
class DeepSeekAgent:
    def __init__(self, api_key: Optional[str] = None):
        """初始化DeepSeek智能体"""
        # 获取API密钥（优先从参数获取，否则从环境变量获取）
        self.api_key = '***REMOVED***'
        # API端点URL
        self.api_url = "https://api.deepseek.com/v1/chat/completions"
        # HTTP请求头，包含认证信息和数据格式说明
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }
        # 智能体配置 - 设定AI模型的行为和诗词生成要求
        self.system_prompt = """
        你是一位才华横溢的诗人助手。根据用户提供的主题和要求，创作高质量的诗词作品。
        请确保：
        1. 诗词符合传统韵律和意境
        2. 语言优美，富有想象力
        3. 根据用户指定的形式创作（绝句、律诗、词等）
        """
        # ==================== 新增功能：拓展多种诗歌流派的系统提示词，用于多样性控制 ====================
        self.style_prompts = {
            "默认": self.system_prompt,
            "婉约": """
            你是一位擅长婉约派风格的清丽诗人。请创作词句清丽、情感细腻深婉、意境幽怨缠绵的诗词。
            请确保：
            1. 诗词符合传统韵律和意境
            2. 情感细腻，多用比兴，格调柔美
            3. 根据用户指定的形式创作（绝句、律诗、词等）
            """,
            "豪放": """
            你是一位擅长豪放派风格的豪迈诗人。请创作气势磅礴、意境雄浑开阔、情感热烈奔放的诗词。
            请确保：
            1. 诗词符合传统韵律和意境
            2. 笔力雄健，想象奇特，格局宏大
            3. 根据用户指定的形式创作（绝句、律诗、词等）
            """,
            "田园": """
            你是一位擅长山水田园风格的隐逸诗人。请创作意境闲适宁静、自然清新、富有乡村与山水生活情趣的诗词。
            请确保：
            1. 诗词符合传统韵律和意境
            2. 语言质朴自然，展现人与自然的和谐之美
            3. 根据用户指定的形式创作（绝句、律诗、词等）
            """,
            "边塞": """
            你是一位擅长边塞诗风格的慷慨诗人。请创作格调雄浑、悲壮苍凉、展现边疆风光与将士豪情的诗词。
            请确保：
            1. 诗词符合传统韵律和意境
            2. 充满边防色彩，气势慷慨，意境深沉
            3. 根据用户指定的形式创作（绝句、律诗、词等）
            """
        }
        # ==================================================================================
    # 修改：扩展了可选参数 style（风格选择）与 temperature（多样性/随机性控制，默认 0.7）
    def generate_poem(self,
                      theme: str,
                      poem_type: str = "绝句",
                      length: str = "五言",
                      style: str = "默认",
                      temperature: float = 0.7) -> str:
        """
        根据主题和要求生成诗歌
        参数:
            theme: 诗歌主题
            poem_type: 诗歌类型（绝句、律诗等）
            length: 诗歌长度（五言、七言等）
            style: 创作风格（如"默认", "婉约", "豪放", "田园", "边塞"）
            temperature: 采样温度（0-1之间，值越高随机性与创意性越强）
        """
        # 构建用户提示，明确告诉AI需要生成的诗词类型和主题
        user_prompt = f"请以'{theme}'为主题，创作一首{length}{poem_type}。"
        # 修改：根据指定的风格选择对应的系统提示词
        selected_system_prompt = self.style_prompts.get(style, self.system_prompt)
        # 构建API请求载荷，包含模型选择、消息内容和生成参数
        payload = {
            "model": "deepseek-chat",  # 指定使用的DeepSeek模型
            "messages": [
                {"role": "system", "content": selected_system_prompt},  # 修改：使用已选择的风格提示词
                {"role": "user", "content": user_prompt}  # 用户请求，包含诗词创作要求
            ],
            "temperature": temperature,  # 修改：使用传入的 temperature 参数控制随机性
            "max_tokens": 500  # 限制最大生成的token数量，避免生成过长文本
        }
        try:
            # 发送POST请求到DeepSeek API，传递请求头和载荷
            response = requests.post(self.api_url, headers=self.headers, data=json.dumps(payload))
            # 检查请求是否成功（非200状态码会抛出HTTPError异常）
            response.raise_for_status()
            # 解析JSON格式的响应数据
            result = response.json()
            # 提取生成的诗词内容（从响应的choices列表中获取）
            return result["choices"][0]["message"]["content"].strip()
        except requests.exceptions.RequestException as e:
            # 处理网络请求错误（如无网络、API密钥错误、请求超时等）
            print(f"API请求错误: {e}")
            return "抱歉，诗歌生成失败，请稍后再试。"
        except (KeyError, json.JSONDecodeError) as e:
            # 处理响应解析错误（如响应格式异常、关键字缺失等）
            print(f"响应解析错误: {e}")
            return "抱歉，解析API响应时出错。"
    # ==================== 新增功能：批量生成诗词并进行多样性控制 ====================
    def generate_poems_batch(self,
                             themes: List[str],
                             count_per_theme: int = 1,
                             poem_type: str = "绝句",
                             length: str = "五言",
                             styles: Optional[List[str]] = None) -> List[Dict[str, Any]]:
        results = []
        # 确定候选风格池
        style_pool = styles if styles else list(self.style_prompts.keys())
        for theme in themes:
            for i in range(count_per_theme):
                selected_style = random.choice(style_pool)
                random_temp = round(random.uniform(0.5, 0.9), 2)

                print(f"正在批量生成 -> 主题: {theme} ({i+1}/{count_per_theme}) | 风格: {selected_style} | 温度: {random_temp}")

                poem_content = self.generate_poem(
                    theme=theme,
                    poem_type=poem_type,
                    length=length,
                    style=selected_style,
                    temperature=random_temp
                )

                # 将结果及元数据整理保存
                results.append({
                    "theme": theme,
                    "index": i + 1,
                    "style": selected_style,
                    "temperature": random_temp,
                    "poem": poem_content
                })
        return results
    # ============================================================================
# 使用示例，主程序入口
if __name__ == "__main__":
    # 注意：请替换为你的实际API密钥，或设置环境变量 DEEPSEEK_API_KEY
    agent = DeepSeekAgent(api_key="your_api_key_here")
    # ==================== 修改：示例改用批量生成方法，并展示多样性参数的效果 ====================
    print("【测试：单首生成（兼容旧版用法）】")
    # 生成一首关于"春"的五言绝句
    poem = agent.generate_poem("春", "绝句", "五言")
    # 打印诗词标题和生成的诗词
    print("《春景》")
    print(poem)
    print("=" * 40)
    print("\n【测试：批量生成与多样性控制】")
    # 支持一次性传入多个主题，并指定每个主题生成的数量
    themes_list = ["梅", "兰"]
    batch_results = agent.generate_poems_batch(
        themes=themes_list,
        count_per_theme=2,
        poem_type="绝句",
        length="七言"
    )

    # 打印批量生成的成果
    print("\n========= 批量生成诗词集展示 =========")
    for item in batch_results:
        print(f"\n主题: 《{item['theme']}》 (第{item['index']}首)")
        print(f"生成流派: {item['style']}风格 | 随机采样温度: {item['temperature']}")
        print("作品内容:")
        print(item["poem"])
        print("-" * 30)
    # ======================================================================================
