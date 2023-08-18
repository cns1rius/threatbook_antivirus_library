# @Author: s1rius
# @Date: 2023-07-19 14:24:49
# @LastEditTime: 2023-08-18 14:33:00
# @Description: https://s1rius.space/

# --------------Attention--------------
# 针对某公司语雀病毒库表格做的半自动脚本
# 整体复制上去后连接会呈现黑体
# 对链接需双击空格回车方可转化为蓝色字体链接

import time
import requests
from openpyxl import Workbook

headers = {
    "Cookie": "",
}
page = 10  # 爬取的总页数

sha256_alllist = []

name = "s1rius"
name_list = []
type_list = []
type_magic_list = []
sha256_list = []
sha1_list = []
md5_list = []
virus_type_list = []
virus_family_list = []
action_list = []
url_list = []
file_url_list = []

for page in range(page):
    list_url = f"https://s.threatbook.com/apis/samples/recent_submit?page={page}&size=20"  # 自定义页数改这里
    list_res = requests.get(list_url, headers=headers).json()
    for i in range(len(list_res["data"]["items"])):
        sha256 = list_res["data"]["items"][i]["sha256"]
        threat_level = list_res["data"]["items"][i]["threat_level"]
        if threat_level != "clean":
            print(sha256)
            sha256_alllist.append(sha256)

for s in sha256_alllist:
    try:
        summary_url = f"https://s.threatbook.com/apis/sample/summary/{s}"
        sign_url = f"https://s.threatbook.com/apis/sample/signatures?sha256={s}"

        sign = requests.get(sign_url, headers=headers).json()["data"]["signatureVos"][
            0
        ]["signatures"][0]["signatureData"]
        des_list = []
        for des in sign:
            des_list.append(des["signatures"]["description"])
            description = "\n".join(des_list)
            action_list.append(description)

        summary = requests.get(summary_url, headers=headers).json()["data"]
        name_list.append(summary["file_name"])
        type_list.append(summary["file_type"])
        type_magic_list.append(summary["file_format"])
        sha256_list.append(s)
        sha1_list.append(summary["sha1"])
        md5_list.append(summary["md5"])
        virus_type_list.append(summary["virusType"])
        virus_family_list.append(summary["virusFamily"])
        url_list.append(f"https://s.threatbook.com/report/file/{s}")
        file_url_list.append(
            f"https://s.threatbook.com/apis/sample/download/{s}/?type=sample"
        )
        print(sign_url)
    except Exception as e:
        print(e)
    # action_list.append(summary["description"])

wb = Workbook()
ws = wb.active
chart = []

for n in range(len(name_list)):
    row = [
        f"{time.strftime('%Y-%m-%d')}",
        f"{name}",
        name_list[n],
        type_list[n],
        type_magic_list[n],
        sha256_list[n],
        sha1_list[n],
        md5_list[n],
        virus_type_list[n],
        virus_family_list[n],
        action_list[n],
        "",
        "是/否",
        "是/否",
        file_url_list[n] + " \n",
        url_list[n] + " \n",
    ]
    print(row)
    ws.append(row)
wb.save("./test.xlsx")
