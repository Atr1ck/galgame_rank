import csv
import time
from time import sleep
import requests
from lxml import etree
from bs4 import BeautifulSoup

def fetch_with_retries(url, headers, retries=3, backoff_factor=1):
    """
    尝试从给定的URL获取数据，最多重试retries次，间隔时间随重试次数指数级增加
    :param url: 目标URL
    :param headers: 请求头
    :param retries: 最大重试次数
    :param backoff_factor: 每次重试间隔的倍数（指数级）
    :return: 请求的响应对象
    """
    attempt = 0
    while attempt < retries:
        try:
            # 尝试发送请求
            response = requests.get(url, headers=headers, timeout=10)
            # 请求成功返回响应
            return response
        except requests.exceptions.Timeout:
            # 捕获超时异常，准备重试
            attempt += 1
            wait_time = backoff_factor * (2 ** (attempt - 1))  # 指数回退策略
            print(f"请求超时，正在重试 {attempt}/{retries} ... 等待 {wait_time} 秒")
            time.sleep(wait_time)
        except requests.exceptions.RequestException as e:
            # 捕获其他可能的异常
            print(f"请求失败: {e}")
            break
    
    # 如果达到最大重试次数，返回 None 或抛出异常
    print("最大重试次数已达到，无法获取响应。")
    return None

# 打开文件
with open('games_info.csv', mode='w', newline='', encoding='utf-8') as csvfile: 
        writer = csv.writer(csvfile)
        writer.writerow(['游戏名称', '批评空间链接', '图片链接', '会社', '游戏官网', '中央值', '平均值', '标准偏差', '评论数'])
        offset = 0
        while 1:
            url = f'https://erogamescape.dyndns.org/~ap2/ero/toukei_kaiseki/toukei_median.php?offset={offset * 100}&count=100&year=1900'
            offset += 1
            headers = {
                'User-Agent': "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36 Edg/128.0.0.0"
            }
            response = fetch_with_retries(url, headers, retries=5, backoff_factor=1)
            html = response.text
            soup = BeautifulSoup(html, "lxml")
            with open('data1.txt', 'w') as f:
                f.write(soup.prettify())
            items = soup.find_all('tr')
            if len(items) == 1:
                break
            for item in items[1:]:
                # 提取游戏名称和链接
                game_link = item.find('a', class_='tooltip')
                game_name = game_link.text.strip()
                game_id = game_link['href']
                game_url = f'https://erogamescape.dyndns.org/~ap2/ero/toukei_kaiseki/{game_id}'

                # 提取图片链接
                image_tag = item.find('img')
                if image_tag:
                    image_url = image_tag['src']
                else:
                    image_url = "None"

                # 提取品牌名
                brand_link = item.find('a', href=lambda href: href and 'brand.php' in href)
                brand_name = brand_link.text.strip()
 

                # 提取品牌名链接
                brand_link = item.find('a', class_='ohp_link_01')
                if brand_link:
                    brand_url = brand_link['href']
                else:
                    brand_url = "None"

                # 提取评分和评论数
                ratings = [td.text.strip() for td in item.find_all('td')[2:]]

                writer.writerow([game_name, game_url, image_url, brand_name, brand_url, ratings[0], ratings[1], ratings[2], ratings[3]])
            
            print(f'第{offset}页写入完成')

