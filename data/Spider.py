import csv

import requests
import json

from scrapy.utils.iterators import csviter

headers = {
    "accept": "*/*",
    "accept-language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
    "content-type": "application/json",
    "cookieorigin": "https://you.ctrip.com",
    "origin": "https://you.ctrip.com",
    "priority": "u=1, i",
    "referer": "https://you.ctrip.com/",
    "sec-ch-ua": "\"Not(A:Brand\";v=\"8\", \"Chromium\";v=\"144\", \"Microsoft Edge\";v=\"144\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"Windows\"",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-site",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/144.0.0.0 Safari/537.36 Edg/144.0.0.0",
    "x-ctx-ubt-pageid": "10650142842",
    "x-ctx-ubt-pvid": "4",
    "x-ctx-ubt-sid": "3",
    "x-ctx-ubt-vid": "1706875773930.c70faLfi8sWh",
    "x-ctx-wclient-req": "258668c69fbbcd862219517794023dfa"
}
cookies = {
    "UBT_VID": "1706875773930.c70faLfi8sWh",
    "MKT_CKID": "1706875773985.yc33y.l1pe",
    "_RSG": "6aq0AzRqHlCt18JUiVA.qA",
    "_RDG": "28a491646abec623233d42c94c07ab4e50",
    "_RGUID": "cbd1d1bf-4a03-4906-ad3e-29fb1e4c8077",
    "_ubtstatus": "%7B%22vid%22%3A%221706875773930.c70faLfi8sWh%22%2C%22sid%22%3A2%2C%22pvid%22%3A1%2C%22pid%22%3A600001375%7D",
    "_bfaStatusPVSend": "1",
    "_bfaStatus": "success",
    "_ga": "GA1.1.807841015.1737623675",
    "intl_ht1": "h4=32_3742724",
    "_RF1": "113.100.255.246",
    "Hm_lvt_a8d6737197d542432f4ff4abc6e06384": "1768821342",
    "Hm_lpvt_a8d6737197d542432f4ff4abc6e06384": "1768821342",
    "HMACCOUNT": "E134A829C1A5B97A",
    "MKT_Pagesource": "PC",
    "GUID": "09031131219047277081",
    "_ga_5DVRDQD429": "GS2.1.s1768821342$o2$g0$t1768821352$j50$l0$h167818409",
    "_ga_B77BES1Z8Z": "GS2.1.s1768821342$o2$g0$t1768821352$j50$l0$h0",
    "_ga_9BZF483VNQ": "GS2.1.s1768821342$o2$g0$t1768821352$j50$l0$h0",
    "StartCity_Pkg": "PkgStartCity=447",
    "nfes_isSupportWebP": "1",
    "_bfa": "1.1706875773930.c70faLfi8sWh.1.1768821379168.1768821387138.3.4.10650142842",
    "_jzqco": "%7C%7C%7C%7C1768821342546%7C1.1801477516.1768821342374.1768821379833.1768821387902.1768821379833.1768821387902.undefined.0.0.4.4"
}
url = "https://m.ctrip.com/restapi/soa2/18109/json/getAttractionList"
params = {
    "_fxpcqlniredt": "09031131219047277081",
    "x-traceID": "09031131219047277081-1768821419799-2575136"
}
def get_json(k,v,page):
    data = {
         "head": {
                "cid": "09031131219047277081",
                "ctok": "",
                "cver": "1.0",
                "lang": "01",
                "sid": "8888",
                "syscode": "999",
                "auth": "",
                "xsid": "",
                "extension": []
            },
            "scene": "online",
            "districtId": v, #城市
            "index": page,
            "sortType": 1,
            "count": 10,
            "filter": {
                "filterItems": []
            },
            "returnModuleType": "product"
        }
    data = json.dumps(data, separators=(',', ':'))
    response = requests.post(url, headers=headers, cookies=cookies, params=params, data=data)

    return response.json()

def get_data_info(resp,k):
    feeds = resp.get('attractionList',[])

    with open('data.csv','a',newline='',encoding='utf-8')as csvfile:
        csvwriter = csv.writer(csvfile)
        rows = []
        for feed in feeds:
            card = feed.get('card', {})
            coordinate = card.get('coordinate', {})

            # 提取景点信息
            poiId = card.get('poiId', '')  # 景点 id
            zoneName = card.get('zoneName', '')  # 景点区域
            poiName = card.get('poiName', '')  # 景点名称
            commentCount = card.get('commentCount', '')  # 评论数量
            commentScore = card.get('commentScore', '')  # 评分
            isAdvertisement = card.get('isAdvertisement', '')  # 是否为广告内容
            isRecommend = card.get('isRecommend', '')  # 是否推荐
            districtName = card.get('districtName', '')  # 城市名称
            coverImageUrl = card.get('coverImageUrl', '')  # 图片
            distanceStr = card.get('distanceStr', '')  # 与市中心的距离
            tagNameList = card.get('tagNameList', [])  # 标签
            detailUrl = card.get('detailUrl', '')  # 详情页链接
            marketPrice = card.get('marketPrice', '')  # 市场售价
            preferentialPrice = card.get('preferentialPrice', '')  # 优惠价格
            preferentialDesc = card.get('preferentialDesc', '')  # 优惠描述
            price = card.get('price', '免费')  # 价格
            priceType = card.get('priceType', '')  # 价格类型
            priceTypeDesc = card.get('priceTypeDesc', '')  # 价格类型描述
            isFree = card.get('isFree', '')  # 是否免费
            latitude = coordinate.get('latitude')  # 纬度
            longitude = coordinate.get('longitude')  # 经度
            heatScore = card.get('heatScore', '')  # 热度评分

            # 将提取的所有景点信息存入列表
            rows.append([
                poiId, zoneName, poiName, commentCount, commentScore,
                isAdvertisement, isRecommend, districtName, coverImageUrl,
                distanceStr, tagNameList, detailUrl, marketPrice,
                preferentialPrice, preferentialDesc, price, priceType,
                priceTypeDesc, isFree, latitude, longitude, heatScore,k
            ])

        csvwriter.writerows(rows)

if __name__ == "__main__":
    cityDict = {
        # 直辖市
        "北京": 1,
        "上海": 2,
        "天津": 154,
        "重庆": 158,
        # 各省省会城市
        "石家庄": 199,  # 河北省会
        "太原": 167,  # 山西省会
        "呼和浩特": 156,  # 内蒙古自治区首府
        "沈阳": 155,  # 辽宁省会
        "长春": 216,  # 吉林省会
        "哈尔滨": 151,  # 黑龙江省会
        "南京": 9,  # 江苏省会
        "杭州": 14,  # 浙江省会
        "合肥": 196,  # 安徽省会
        "福州": 164,  # 福建省会
        "南昌": 175,  # 江西省会
        "济南": 128,  # 山东省会
        "郑州": 157,  # 河南省会
        "武汉": 145,  # 湖北省会
        "长沙": 148,  # 湖南省会
        "广州": 152,  # 广东省会
        "南宁": 166,  # 广西壮族自治区首府
        "海口": 37,  # 海南省会
        "成都": 104,  # 四川省会
        "贵阳": 33,  # 贵州省会
        "昆明": 29,  # 云南省会
        "拉萨": 36,  # 西藏自治区首府
        "西安": 7,  # 陕西省会
        "兰州": 231,  # 甘肃省会
        "西宁": 237,  # 青海省会
        "银川": 239,# 宁夏回族自治区首府
        "乌鲁木齐":32,
        "香港":38,
        "台北":360,
        "厦门":21,
        "汕头":215,
        "丽江":32,
        "澳门":39,
    }
    for k,v in cityDict.items():
        for page in range(1,35):
            print(f'{k}正在爬取第{page}页......')
            resp = get_json(k,v,page)
            get_data_info(resp,k)