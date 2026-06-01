import requests
import pandas as pd
from bs4 import BeautifulSoup


def get_html(url):
    """
    获取网页 HTML
    """
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/120.0.0.0 Safari/537.36"
        ),
        "Referer": "https://www.weather.com.cn/"
    }

    response = requests.get(url, headers=headers, timeout=10)
    response.raise_for_status()

    # 中国天气网页面常用 utf-8
    response.encoding = "utf-8"

    return response.text


def parse_weather(html):
    """
    解析苏州 8-15 天天气信息
    """
    soup = BeautifulSoup(html, "html.parser")

    weather_list = []

    # 注意：id="15d" 以数字开头，不能写成 #15d
    lis = soup.select('[id="15d"] ul.t li')

    for li in lis:
        date_tag = li.select_one(".time")
        weather_tag = li.select_one(".wea")
        temp_tag = li.select_one(".tem")
        wind_tag = li.select_one(".wind")

        date = date_tag.get_text(strip=True) if date_tag else ""
        weather = weather_tag.get_text(strip=True) if weather_tag else ""
        temperature = temp_tag.get_text(strip=True) if temp_tag else ""
        wind = wind_tag.get_text(strip=True) if wind_tag else ""

        weather_list.append({
            "日期": date,
            "天气": weather,
            "温度": temperature,
            "风力": wind
        })

    return weather_list

def save_data(weather_list):
    """
    保存数据到文档
    """
    df = pd.DataFrame(weather_list)

    df.to_excel("苏州8-15天天气.xlsx", index=False)
    df.to_csv("苏州8-15天天气.csv", index=False, encoding="utf-8-sig")

    print("保存成功：苏州8-15天天气.xlsx")
    print("保存成功：苏州8-15天天气.csv")
    print(f"共保存 {len(df)} 条天气数据")


def main():
    url = "https://www.weather.com.cn/weather15d/101190401.shtml"

    html = get_html(url)
    weather_list = parse_weather(html)

    print(weather_list)

    if not weather_list:
        print("没有解析到数据，可能是网页结构变化或请求被限制。")
        return

    save_data(weather_list)


if __name__ == "__main__":
    main()