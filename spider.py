#!/usr/local/bin/python3
# -*- encoding: utf-8 -*-

import requests
from lxml import etree
import time


def balance_query(room):

    url = "http://172.20.11.113:8080/admin/sys!chaxun.action"

    headers = {
        "Accept":
        "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "Referer": "http://172.20.11.113:8080/admin/sys!chaxun.action",
        "User-Agent":
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36 Edg/108.0.1462.54"
    }

    data = {"fjmc": room}

    response = requests.post(url, headers=headers, data=data)

    if response.status_code == 200:

        print("正在查询：寝室电费...")
        html = response.text
        html = etree.HTML(html)

        # 电费余额
        balance = html.xpath('//table/tr[3]/td[4]/text()')[0].strip()

    else:
        print("查询失败！")
        balance = None

    # 当前时间
    now_time = time.strftime("%Y-%m-%d %H:%M", time.localtime())

    return room, balance, now_time


def write_csv(result):
    room, balance, now_time = result
    file_name = f"./_data/{room}.csv"

    with open(file_name, "a", newline="") as f:
        f.write(f"{room}, {balance}, {now_time}\n")


def main():
    # 查询电费余额
    room = "30-2627"
    result = balance_query(room)
    write_csv(result)


if __name__ == "__main__":
    main()
