import time
import pandas as pd
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import logging

# 日志配置
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("google_restaurant.log", encoding="utf-8"),
        logging.StreamHandler()
    ]
)
log = logging.getLogger(__name__)

def wait_for_captcha(driver):
    """
    如果出现 Google 人机验证，则一直等待，
    用户完成验证后自动继续。
    """
    while True:
        try:
            url = driver.current_url.lower()
        except Exception:
            url = ""
        try:
            page = driver.page_source.lower()
        except Exception:
            page = ""
        if (
            "sorry/index" in url
            or "recaptcha" in page
            or "unusual traffic" in page
            or "our systems have detected unusual traffic" in page
            or "进行人机身份验证" in page
        ):
            log.warning("检测到 Google 人机验证！")
            log.warning("请在浏览器中完成验证，程序将自动继续运行……")

            time.sleep(2)
            continue
        return

# 创建浏览器
def get_driver():

    service = Service(r"C:\chromedriver-win64\chromedriver.exe")
    options = webdriver.ChromeOptions()

    # 最大化窗口
    options.add_argument("--start-maximized")
    # 防检测
    options.add_argument("--disable-blink-features=AutomationControlled")
    # 不建议无头模式
    # options.add_argument("--headless=new")
    driver = webdriver.Chrome(service=service,options=options)
    # 打开谷歌地图
    driver.get("https://www.google.com/maps?hl=zh-HK")

    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located(
            (By.CSS_SELECTOR, 'input[name="q"]')
        )
    )
    return driver

# 搜索餐厅
def search_restaurant(driver, keyword):
    log.info(f"开始搜索：{keyword}")
    try:
        # 每次重新进入 Google Maps 首页
        driver.get("https://www.google.com/maps?hl=en")
        # 检测验证码
        wait_for_captcha(driver)
        # 等待搜索框
        search_box = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, 'input[name="q"]')
            )
        )
        # 双保险，虽然首页一般为空
        search_box.send_keys(Keys.CONTROL, "a")
        search_box.send_keys(Keys.DELETE)

        # 输入关键词
        search_box.send_keys(keyword)
        search_box.send_keys(Keys.ENTER)

        # 搜索完成最容易触发验证码
        wait_for_captcha(driver)

        # 等待出现列表或详情页
        WebDriverWait(driver, 20).until(
            lambda d:
            len(d.find_elements(By.CSS_SELECTOR, "a.hfpxzc")) > 0
            or len(d.find_elements(By.CSS_SELECTOR, "h1.DUwDvf")) > 0
        )
        # 如果出现搜索列表，点击第一条
        rows = driver.find_elements(By.CSS_SELECTOR, "a.hfpxzc")

        if rows:
            driver.execute_script("arguments[0].click();", rows[0])
            wait_for_captcha(driver)
            WebDriverWait(driver, 20).until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, "h1.DUwDvf")
                )
            )
        # 页面稳定
        time.sleep(1)
        return True
    except Exception as e:
        log.exception(f"搜索失败：{keyword}")
        return False

def get_element_txt(driver, css_path, get_method="text"):
    try:
        ele = WebDriverWait(driver,5).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, css_path)
            )
        )
        if get_method == "text":
            return ele.text.strip()
        return ele.get_attribute(get_method).strip()
    except Exception:
        return ""

def get_latlng(driver, url):
    m = re.search(r'@(-?\d+\.\d+),(-?\d+\.\d+)',url)
    if m:
        return m.group(1), m.group(2)
    return "", ""

def get_restaurant_detail(driver):
    item = {}
    item['detail_url'] = driver.current_url
    item['shop_name'] = get_element_txt(driver, css_path='h1.DUwDvf.lfPIob')
    item['category'] = get_element_txt(driver, css_path='button.DkEaL')
    item['price'] = get_element_txt(driver,css_path='span.mgr77e span:last-child').replace("·", "").strip()

    score = get_element_txt(driver,'.F7nice .ceNzKf','aria-label')
    item['score'] = re.search(r'[\d.]+', score).group() if score else ""

    item['review_count'] = (get_element_txt(driver,css_path='.F7nice span[role="img"][aria-label*="reviews"]')
        .replace("(", "")
        .replace(")", "")
        .replace(",", "")
        .strip() )

    item['address'] = (get_element_txt(driver, css_path='[data-item-id="address"]').replace("", "").strip())
    item['locatedin'] = (get_element_txt(driver, css_path='[data-item-id="locatedin"]').replace("Located in:", "")
    .replace("位於：", "")
    .replace("位于：", "")
    .strip() )

    item['phone'] = (get_element_txt(driver, css_path='[data-item-id^="phone:"]').replace("", "")
    .replace("+", "")
    .strip() )

    item['website'] = get_element_txt(driver, css_path='[data-item-id="authority"]', get_method='href')
    item['opening_hours'] = (get_element_txt(driver, css_path='span.ZDu9vd').replace("Open · Closes", "")
    .replace("Closed · Opens", "")
    .replace("營業中 ·", "")
    .replace("休息中 ·", "")
    .replace("营业中 ·", "")
    .replace("Open", "")
    .replace("Closed", "")
    .strip()
)
    item['google_map_lat'], item['google_map_lng'] = get_latlng(driver, item['detail_url'])
    return item

# 主程序
def main():
    file_path = "餐厅.xlsx"

    # 读取Excel
    df = pd.read_excel(file_path)
    # 防空值
    df["restaurant_name"] = (df["restaurant_name"].fillna("").astype(str))

    fields = [
        "detail_url",
        "shop_name",
        "category",
        "price",
        "score",
        "review_count",
        "address",
        "locatedin",
        "phone",
        "website",
        "opening_hours",
        "google_map_lat",
        "google_map_lng"
    ]
    for field in fields:
        if field not in df.columns:
            df[field] = ""

    # 浏览器
    driver = get_driver()

    # 遍历搜索
    for index, row in df.iterrows():
        restaurant_name = row["restaurant_name"].strip()
        # 组合搜索关键词
        keyword = restaurant_name
        # 空值跳过
        if keyword == "":
            continue
        try:
            # 搜索
            ok = search_restaurant(driver, keyword)
            # 搜索失败
            if ok:
                item = get_restaurant_detail(driver)
                log.info(f"获取成功：{item}")
                for k, v in item.items():
                    df.loc[index, k] = v
            else:
                log.warning(f"未搜索到结果：{keyword}")

            # 每5条自动保存
            if index % 5 == 0:
                df.to_excel("香港谷歌地址结果_实时保存.xlsx",index=False)
                log.info(f"已自动保存，第 {index} 条")

        except Exception as e:
            log.exception(f"搜索失败：{keyword}")
            df.to_excel("香港谷歌地址结果_实时保存.xlsx",index=False)
    # 最终保存
    output_file = "香港谷歌地址结果.xlsx"
    df.to_excel(output_file,index=False)
    log.info(f"程序完成，结果保存至：{output_file}")
    input("按回车关闭浏览器")
    log.info("Google Maps 餐厅采集结束")
    driver.quit()

# 启动
if __name__ == "__main__":
    main()