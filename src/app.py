import os
import time
import math
import csv
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from getpass import getpass
from datetime import datetime


class EasyApplyLinkedinJobBot:
    def __init__(self, account: str, password: str, jobs: list, location: str):
        try:
            self.appName: str = "LinkedIn自动投递机器人"
            self.endpoint: str = "https://www.linkedin.com/jobs/search/"
            self.endpointJobViewer: str = "https://www.linkedin.com/jobs/view/"
            self.account: str = account
            self.password: str = password
            self.applicationCount: int = 0
            self.countJob: int = 0
            self.jobsPerPage: int = 25
            self.jobsLocation: str = location
            self.searchKeywords: list = jobs
            self.applied_jobs: list = []
            self.easyApplyParameter: list = [
                "?f_AL=true",
                "&keywords=",
                "&location=",
                "&start=",
            ]

            print(f"🤖 初始化 LinkedIn 自动投递机器人")
            print(f"👤 账号: {account}")
            print(f"🔍 搜索关键词: {', '.join(jobs)}")
            print(f"📍 地区: {location}")
            self.driver: object = webdriver.Firefox()
            self.driver.implicitly_wait(10)  # 设置隐式等待时间
            self.login_url = "https://www.linkedin.com/login"

            print("✅ 浏览器启动成功")
            self.sign_in()
        except Exception as e:
            print(f"❌ 初始化错误: {str(e)}")
            raise Exception(e)

    def wait_and_find_element(self, by, value, timeout=10):
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located((by, value))
            )
            return element
        except Exception as e:
            print(f"⚠️ 等待元素超时: {value}")
            return None

    def click_element(self, by, value, timeout=10):
        element = self.wait_and_find_element(by, value, timeout)
        if element:
            element.click()
            return True
        return False

    def sign_in(self):
        try:
            print("🔐 正在登录LinkedIn...")
            self.driver.get(self.login_url)

            username = self.wait_and_find_element(By.CSS_SELECTOR, "#username")
            password = self.wait_and_find_element(By.CSS_SELECTOR, "#password")

            if username and password:
                username.send_keys(self.account)
                password.send_keys(self.password)
                del self.password  # 清除内存中的密码

                if self.click_element(By.CSS_SELECTOR, "button[type='submit']"):
                    print("⏳ 等待登录完成...")

                    # 尝试多个选择器验证登录
                    selectors = [
                        "nav.global-nav",
                        ".feed-identity-module",
                        ".search-global-typeahead",
                        ".profile-rail-card",
                    ]

                    for selector in selectors:
                        if self.wait_and_find_element(
                            By.CSS_SELECTOR, selector, timeout=5
                        ):
                            print("✅ LinkedIn登录成功")
                            return

                    print("⚠️ 登录状态未能验证，但将继续尝试...")
            else:
                raise Exception("找不到登录表单")

        except Exception as e:
            print(f"❌ 登录失败: {str(e)}")
            raise Exception(e)

    def main(self):
        print("\n🚀 开始搜索职位...")
        job_ids: list = []
        all_jobs: list = []

        for keyword in self.searchKeywords:
            print(f"\n📊 正在搜索关键词: {keyword}")
            search_url = (
                f"{self.endpoint}{self.easyApplyParameter[0]}"
                f"{self.easyApplyParameter[1]}{keyword}"
                f"{self.easyApplyParameter[2]}{self.jobsLocation}"
            )

            print(f"🌐 访问搜索页面: {search_url}")
            self.driver.get(search_url)
            time.sleep(5)

            try:
                jobs_count = self.wait_and_find_element(
                    By.CSS_SELECTOR, ".jobs-search-results-list__title-heading"
                )

                if jobs_count:
                    # Extract only numbers from the text
                    count_text = "".join(filter(str.isdigit, jobs_count.text))
                    total_jobs = int(count_text) if count_text else 0
                    total_pages = math.ceil(total_jobs / self.jobsPerPage)
                    print(f"📑 找到 {total_jobs} 个职位，共 {total_pages} 页")

                    for page in range(total_pages):
                        print(f"\n📄 正在处理第 {page + 1}/{total_pages} 页")
                        page_url = f"{search_url}{self.easyApplyParameter[3]}{page * self.jobsPerPage}"
                        self.driver.get(page_url)

                        job_cards = self.driver.find_elements(
                            By.CSS_SELECTOR, ".job-card-container"
                        )

                        for card in job_cards:
                            try:
                                job_id = card.get_attribute("data-job-id")
                                if job_id:
                                    job_ids.append(job_id)
                                    # Fix selectors for job information
                                    job_title = card.find_element(
                                        By.CSS_SELECTOR, ".job-card-list__title"
                                    ).text
                                    job_company = card.find_element(
                                        By.CSS_SELECTOR,
                                        ".job-card-container__company-name",
                                    ).text
                                    job_location = card.find_element(
                                        By.CSS_SELECTOR,
                                        ".job-card-container__metadata-item",
                                    ).text

                                    all_jobs.append(
                                        {
                                            "datetime": datetime.now().strftime(
                                                "%Y-%m-%d %H:%M:%S"
                                            ),
                                            "title": job_title,
                                            "company": job_company,
                                            "location": job_location,
                                            "url": f"{self.endpointJobViewer}{job_id}",
                                            "status": "未申请",
                                        }
                                    )
                            except Exception as e:
                                print(f"⚠️ 无法获取职位卡片信息: {str(e)}")
                                continue

                        print(f"⏳ 已收集 {len(job_ids)} 个职位ID")

                    # 新增：保存搜索到的所有职位信息
                    self.saveSearchResultsToCSV(all_jobs, keyword)

            except Exception as e:
                print(f"❌ 搜索页面错误: {str(e)}")
                continue

        unique_job_ids = list(set(job_ids))

        print(f"\n📋 总计找到 {len(unique_job_ids)} 个不重复职位")
        print("\n🤖 开始自动申请流程...")

        success_count = 0

        for index, job_id in enumerate(unique_job_ids, 1):
            try:
                print(
                    f"\n💼 正在处理第 {index}/{len(unique_job_ids)} 个职位 (ID: {job_id})"
                )
                self.apply_to_job(job_id)
                success_count += 1
            except Exception as e:
                print(f"❌ 申请职位 {job_id} 时出错: {str(e)}")
                continue

        print(f"\n🎉 申请完成!")
        print(f"📊 统计信息:")
        print(f"   - 总职位数: {len(unique_job_ids)}")
        print(f"   - 成功申请: {success_count}")
        print(f"   - 失败数量: {len(unique_job_ids) - success_count}")

        # 保存已申请职位到CSV
        if self.applied_jobs:
            for keyword in self.searchKeywords:
                self.saveIntoCSV(self.applied_jobs, keyword)

    def apply_to_job(self, job_id):
        position_url = f"{self.endpointJobViewer}{job_id}"
        print(f"🔗 访问职位页面: {position_url}")
        self.driver.get(position_url)

        try:
            # 获取职位详情
            job_title = self.wait_and_find_element(
                By.CSS_SELECTOR, ".job-details-jobs-unified-top-card__job-title"
            )
            job_description = self.wait_and_find_element(
                By.CSS_SELECTOR, ".jobs-description"
            )
            job_location = self.wait_and_find_element(
                By.CSS_SELECTOR, ".jobs-unified-top-card__bullet"
            )

            apply_button = self.wait_and_find_element(
                By.CSS_SELECTOR, "button.jobs-apply-button"
            )

            if apply_button and "立即申请" in apply_button.text:
                print("🖱️ 点击申请按钮")
                apply_button.click()

                submit_button = self.wait_and_find_element(
                    By.CSS_SELECTOR, "button[aria-label='提交申请']"
                )

                if submit_button:
                    print("📝 发现快速申请按钮")
                    submit_button.click()
                    self.applicationCount += 1

                    # 保存职位数据
                    self.applied_jobs.append(
                        {
                            "datetime": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                            "title": job_title.text if job_title else "",
                            "description": (
                                job_description.text if job_description else ""
                            ),
                            "url": position_url,
                            "country": job_location.text if job_location else "",
                        }
                    )

                    print(f"✅ 成功申请职位 {job_id}")
                    print("⏳ 等待5秒后继续...")
                    time.sleep(5)
                else:
                    print("📋 需要多步骤申请流程")
                    self.handle_multi_step_application()
                    print("⏳ 等待5秒后继续...")
                    time.sleep(5)
            else:
                print(f"⚠️ 职位 {job_id} 无法直接申请")

        except Exception as e:
            print(f"❌ 申请过程出错: {str(e)}")

    def handle_multi_step_application(self):
        print("🔄 开始多步骤申请流程")
        try:
            while True:
                next_button = self.wait_and_find_element(
                    By.CSS_SELECTOR, "button[aria-label='继续下一步']"
                )

                if next_button:
                    print("➡️ 点击下一步")
                    next_button.click()
                else:
                    review_button = self.wait_and_find_element(
                        By.CSS_SELECTOR, "button[aria-label='检查申请']"
                    )

                    if review_button:
                        print("📋 检查申请信息")
                        review_button.click()

                        submit_button = self.wait_and_find_element(
                            By.CSS_SELECTOR, "button[aria-label='提交申请']"
                        )

                        if submit_button:
                            print("📤 提交申请")
                            submit_button.click()
                            self.applicationCount += 1
                            print("✅ 成功提交多步骤申请")
                            break
                    else:
                        print("⚠️ 无法完成多步骤申请")
                        break

        except Exception as e:
            print(f"❌ 多步骤申请出错: {str(e)}")

    def saveIntoCSV(self, data, keyword):
        try:

            export_dir = "export"
            if not os.path.exists(export_dir):
                os.makedirs(export_dir)

            current_time = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{export_dir}/{keyword}_applied_jobs_{current_time}.csv"

            print(f"💾 正在保存申请记录...")

            with open(filename, mode="w", newline="", encoding="utf-8") as file:
                fieldnames = ["datetime", "title", "description", "url", "country"]
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                writer.writeheader()
                for row in data:
                    writer.writerow(row)
            print(f"✅ 已保存到: {filename}")

        except Exception as e:
            print(f"❌ 保存CSV文件失败: {str(e)}")

    def saveSearchResultsToCSV(self, data, keyword):
        try:
            export_dir = "export"
            if not os.path.exists(export_dir):
                os.makedirs(export_dir)

            current_time = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{export_dir}/{keyword}_all_jobs_{current_time}.csv"

            print(f"💾 正在保存搜索结果...")

            with open(filename, mode="w", newline="", encoding="utf-8") as file:
                fieldnames = [
                    "datetime",
                    "title",
                    "company",
                    "location",
                    "url",
                    "status",
                ]
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                writer.writeheader()
                for row in data:
                    writer.writerow(row)
            print(f"✅ 已保存搜索结果到: {filename}")

        except Exception as e:
            print(f"❌ 保存搜索结果失败: {str(e)}")
