import re
import time
import requests
import pandas as pd
from bs4 import BeautifulSoup


def get_html(url):
    """
    请求网页源码
    """
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/120.0.0.0 Safari/537.36"
        ),
        "Referer": "https://movie.douban.com/"
    }

    response = requests.get(url, headers=headers, timeout=10)
    response.raise_for_status()
    response.encoding = "utf-8"
    return response.text


def parse_title(item):
    """
    解析中文名、英文名、港台名
    """
    title_tags = item.select(".hd .title")
    other_tag = item.select_one(".hd .other")

    chinese_name = ""
    english_name = ""
    hk_tw_name = ""

    if title_tags:
        chinese_name = title_tags[0].get_text(strip=True)

    if len(title_tags) > 1:
        english_name = title_tags[1].get_text(strip=True)
        english_name = english_name.replace("/", "").strip()

    if other_tag:
        other_text = other_tag.get_text(strip=True)
        other_text = other_text.replace("/", " / ").strip()

        names = [name.strip() for name in other_text.split("/") if name.strip()]

        hk_tw_list = []
        for name in names:
            if "港" in name or "台" in name:
                hk_tw_list.append(name)

        hk_tw_name = " / ".join(hk_tw_list)

    return chinese_name, english_name, hk_tw_name


def parse_director(info_text):
    """
    解析导演
    """
    match = re.search(r"导演:\s*(.*?)\s{2,}|导演:\s*(.*?)主演:", info_text)

    if match:
        director = match.group(1) or match.group(2)
        return director.strip()

    # 备用解析
    if "导演:" in info_text:
        text = info_text.split("导演:")[-1]
        text = text.split("主演:")[0]
        return text.strip()

    return ""


def parse_year_genre(info_lines):
    """
    解析上映年份、电影分类
    """
    year = ""
    genre = ""

    for line in info_lines:
        line = line.strip()
        if re.search(r"\d{4}", line) and "/" in line:
            parts = [part.strip() for part in line.split("/")]

            if parts:
                year_match = re.search(r"\d{4}", parts[0])
                if year_match:
                    year = year_match.group()

            if len(parts) >= 3:
                genre = parts[-1]

            break

    return year, genre


def parse_movie_item(item):
    """
    解析单个电影条目
    """
    chinese_name, english_name, hk_tw_name = parse_title(item)

    bd_p = item.select_one(".bd p")
    info_text = bd_p.get_text(" ", strip=True) if bd_p else ""
    info_lines = bd_p.get_text("\n", strip=True).split("\n") if bd_p else []

    director = parse_director(info_text)
    year, genre = parse_year_genre(info_lines)

    rating_tag = item.select_one(".rating_num")
    rating = rating_tag.get_text(strip=True) if rating_tag else ""

    return {
        "中文名": chinese_name,
        "英文名": english_name,
        "港台名": hk_tw_name,
        "导演": director,
        "上映年份": year,
        "电影分类": genre,
        "评分": rating
    }


def crawl_douban_top250():
    """
    爬取豆瓣电影 Top250
    """
    movies = []

    for start in range(0, 250, 25):
        url = f"https://movie.douban.com/top250?start={start}&filter="
        print(f"正在爬取：{url}")

        html = get_html(url)
        soup = BeautifulSoup(html, "html.parser")

        items = soup.select(".grid_view .item")

        for item in items:
            movie = parse_movie_item(item)
            movies.append(movie)

        time.sleep(1)

    return movies


def save_to_excel(movies, filename="豆瓣电影Top250.xlsx"):
    """
    保存到 Excel 文档
    """
    df = pd.DataFrame(movies)

    df.to_excel(filename, index=False)

    print(f"保存成功：{filename}")
    print(f"共保存 {len(df)} 条电影数据")


def main():
    movies = crawl_douban_top250()
    save_to_excel(movies)


if __name__ == "__main__":
    main()