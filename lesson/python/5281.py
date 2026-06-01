import requests

def translate(text, from_lang="auto", to_lang="zh"):
    url = "https://fanyi.baidu.com/sug"

    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/120.0.0.0 Safari/537.36"
        ),
        "Referer": "https://fanyi.baidu.com/"
    }

    data = {
        "kw": text
    }

    try:
        response = requests.post(url, headers=headers, data=data, timeout=10)
        response.raise_for_status()

        result = response.json()

        if result.get("errno") == 0 and result.get("data"):
            # sug 接口通常返回多个候选结果
            return result["data"][0]["v"]

        return "翻译失败：没有找到翻译结果"

    except requests.exceptions.RequestException as e:
        return f"网络请求失败：{e}"

    except ValueError:
        return "解析失败：返回内容不是 JSON 格式"

    except Exception as e:
        return f"程序出错：{e}"

def main():
    print("====== 百度翻译器（无 API Key 版）======")
    print("输入 q 或 quit 退出程序")

    while True:
        text = input("\n请输入要翻译的文本：").strip()

        if text.lower() in ["q", "quit", "exit"]:
            print("程序已退出")
            break

        if not text:
            print("输入不能为空")
            continue

        result = translate(text)
        print("翻译结果：", result)

if __name__ == "__main__":
    main()