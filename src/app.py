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
            self.appName: str = "领英自动投递机器人"
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
            keyword_jobs = []
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
                    By.CSS_SELECTOR,
                    ".jobs-search-results-list__title-heading, .jobs-search-results__text",
                )

                if jobs_count:
                    count_text = "".join(filter(str.isdigit, jobs_count.text))
                    total_jobs = int(count_text) if count_text else 0
                    total_pages = math.ceil(total_jobs / self.jobsPerPage)

                    print(f"📑 找到 {total_jobs} 个职位，共 {total_pages} 页")

                    for page in range(total_pages):
                        print(f"\n📄 正在处理第 {page + 1}/{total_pages} 页")
                        page_url = f"{search_url}{self.easyApplyParameter[3]}{page * self.jobsPerPage}"

                        max_attempts = 3
                        for attempt in range(max_attempts):
                            try:
                                self.driver.get(page_url)
                                time.sleep(10)

                                selectors = [
                                    ".jobs-search-results-list",
                                    ".jobs-search-results__list",
                                    ".jobs-search__results-list",
                                    "[data-test-id='job-card']",
                                ]

                                job_list = None
                                for selector in selectors:
                                    try:
                                        job_list = WebDriverWait(self.driver, 15).until(
                                            EC.presence_of_element_located(
                                                (By.CSS_SELECTOR, selector)
                                            )
                                        )
                                        if job_list:
                                            break
                                    except:
                                        continue

                                if not job_list:
                                    raise Exception("职位列表未加载")

                                # 循环滚动直到加载所有职位
                                last_height = self.driver.execute_script(
                                    "return document.body.scrollHeight"
                                )
                                while True:
                                    # 滚动到底部
                                    self.driver.execute_script(
                                        "window.scrollTo(0, document.body.scrollHeight);"
                                    )
                                    time.sleep(2)

                                    # 计算新的滚动高度并与上一个滚动高度进行比较
                                    new_height = self.driver.execute_script(
                                        "return document.body.scrollHeight"
                                    )
                                    if new_height == last_height:
                                        break
                                    last_height = new_height

                                # 确保所有职位卡片都已加载
                                job_cards = WebDriverWait(self.driver, 10).until(
                                    EC.presence_of_all_elements_located(
                                        (
                                            By.CSS_SELECTOR,
                                            ".job-card-container, .jobs-search-results__list-item",
                                        )
                                    )
                                )

                                for card in job_cards:
                                    try:
                                        # 使用JavaScript获取元素文本，避免StaleElement异常
                                        job_id = self.driver.execute_script(
                                            "return arguments[0].getAttribute('data-job-id')",
                                            card,
                                        )

                                        if job_id:
                                            job_ids.append(job_id)
                                            job_title = self.driver.execute_script(
                                                "return arguments[0].querySelector('.job-card-list__title').textContent",
                                                card,
                                            )
                                            job_company = self.driver.execute_script(
                                                "return arguments[0].querySelector('.job-card-container__company-name').textContent",
                                                card,
                                            )
                                            job_location = self.driver.execute_script(
                                                "return arguments[0].querySelector('.job-card-container__metadata-item').textContent",
                                                card,
                                            )

                                            keyword_jobs.append(
                                                {
                                                    "datetime": datetime.now().strftime(
                                                        "%Y-%m-%d %H:%M:%S"
                                                    ),
                                                    "title": (
                                                        job_title.strip()
                                                        if job_title
                                                        else ""
                                                    ),
                                                    "company": (
                                                        job_company.strip()
                                                        if job_company
                                                        else ""
                                                    ),
                                                    "location": (
                                                        job_location.strip()
                                                        if job_location
                                                        else ""
                                                    ),
                                                    "url": f"{self.endpointJobViewer}{job_id}",
                                                    "status": "未申请",
                                                }
                                            )
                                    except Exception as e:
                                        print(f"⚠️ 无法获取职位卡片信息: {str(e)}")
                                        continue
                                # 将break移到这里，确保处理完所有职位卡片后再跳出重试循环
                                break
                            except Exception as e:
                                if attempt == max_attempts - 1:  # 最后一次尝试
                                    print(
                                        f"⚠️ 第{attempt + 1}次尝试获取职位列表失败: {str(e)}"
                                    )
                                time.sleep(2)
                                continue

                        print(f"⏳ 已收集 {len(keyword_jobs)} 个职位")

                    if keyword_jobs:
                        try:
                            print(f"\n💾 保存关键词 '{keyword}' 的搜索结果...")
                            self.saveSearchResultsToCSV(keyword_jobs, keyword)
                        except Exception as e:
                            print(f"❌ 保存搜索结果失败: {str(e)}")

                    all_jobs.extend(keyword_jobs)

            except Exception as e:
                print(f"❌ 搜索页面错误: {str(e)}")
                continue

        unique_job_ids = list(set(job_ids))

        if all_jobs:
            try:
                print("\n💾 保存所有搜索到的职位...")
                export_dir = os.path.join(os.getcwd(), "export", "all_jobs")
                os.makedirs(export_dir, exist_ok=True)

                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = os.path.join(export_dir, f"all_jobs_{timestamp}.csv")

                print(f"📊 总职位数: {len(all_jobs)} 个")

                with open(filename, mode="w", newline="", encoding="utf-8-sig") as file:
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

                    batch_size = 50
                    for i in range(0, len(all_jobs), batch_size):
                        batch = all_jobs[i : i + batch_size]
                        writer.writerows(batch)
                        print(
                            f"⏳ 已保存: {min(i + batch_size, len(all_jobs))}/{len(all_jobs)} 个职位"
                        )

                print(f"✅ 已保存所有职位到: {filename}")
            except Exception as e:
                print(f"❌ 保存所有职位失败: {str(e)}")

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

        if self.applied_jobs:
            for keyword in self.searchKeywords:
                self.saveIntoCSV(self.applied_jobs, keyword)

    def apply_to_job(self, job_id):
        position_url = f"{self.endpointJobViewer}{job_id}"
        print(f"🔗 访问职位页面: {position_url}")

        self.driver.get(position_url)
        time.sleep(3)

        try:
            job_title = self.wait_and_find_element(
                By.CSS_SELECTOR, ".job-details-jobs-unified-top-card__job-title"
            )

            job_description = self.wait_and_find_element(
                By.CSS_SELECTOR, ".jobs-description"
            )

            job_location = self.wait_and_find_element(
                By.CSS_SELECTOR, ".jobs-unified-top-card__bullet"
            )

            print(
                {
                    "title": job_title.text if job_title else "",
                    "description": job_description.text if job_description else "",
                    "location": job_location.text if job_location else "",
                }
            )

            # 更新申请按钮选择器
            applied_button = self.wait_and_find_element(
                By.CSS_SELECTOR,
                ".jobs-apply-button--applied, [aria-label='已申请'], [data-control-name='applied']",
            )

            if applied_button:
                print("⚠️ 已经申请过此职位")
                return

            # 更新申请按钮选择器
            apply_button = self.wait_and_find_element(
                By.CSS_SELECTOR,
                ".jobs-apply-button:not(.jobs-apply-button--applied), [aria-label='申请'], [data-control-name='apply']",
            )

            if apply_button and any(
                text in apply_button.text for text in ["立即申请", "Apply", "申请"]
            ):
                print("🖱️ 点击申请按钮")
                apply_button.click()
                time.sleep(3)

                self.handle_screening_questions()

                submit_button = self.wait_and_find_element(
                    By.CSS_SELECTOR, "button[aria-label='提交申请']"
                )

                if submit_button:
                    print("📝 发现快速申请按钮")
                    submit_button.click()
                    self.applicationCount += 1

                    self.applied_jobs.append(
                        {
                            "datetime": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                            "title": job_title.text if job_title else "",
                            "description": (
                                job_description.text if job_description else ""
                            ),
                            "url": position_url,
                            "country": job_location.text if job_location else "",
                            "status": "已申请",
                        }
                    )

                    print(f"✅ 成功申请职位 {job_id}")
                    time.sleep(5)
                else:
                    print("📋 需要多步骤申请流程")
                    if self.handle_multi_step_application():
                        self.applicationCount += 1
                        print(f"✅ 成功申请职位 {job_id}")
                    else:
                        print("⚠️ 无法完成多步骤申请")
            else:
                print(f"⚠️ 职位 {job_id} 无法直接申请")

        except Exception as e:
            print(f"❌ 申请过程出错: {str(e)}")

    def handle_screening_questions(self):
        """处理申请过程中的筛选问题"""
        try:
            # 查找常见问题容器
            question_containers = self.driver.find_elements(
                By.CSS_SELECTOR, ".jobs-easy-apply-form-section__grouping"
            )

            for container in question_containers:
                # 处理单选按钮（自动选择"是"）
                radio_buttons = container.find_elements(
                    By.CSS_SELECTOR, "input[type='radio'][value='Yes']"
                )
                for radio in radio_buttons:
                    try:
                        radio.click()
                    except:
                        continue

                # 处理下拉菜单
                dropdowns = container.find_elements(
                    By.CSS_SELECTOR, "select.fb-dropdown"
                )
                for dropdown in dropdowns:
                    try:
                        # 选择第一个选项
                        options = dropdown.find_elements(By.TAG_NAME, "option")
                        if len(options) > 1:
                            options[1].click()
                    except:
                        continue

            # 尝试查找并点击下一步按钮
            next_button = self.wait_and_find_element(
                By.CSS_SELECTOR, "button[aria-label='继续']"
            )
            if next_button:
                next_button.click()
                time.sleep(1)

        except Exception as e:
            print(f"⚠️ 处理筛选问题时出错: {str(e)}")

    def handle_multi_step_application(self):
        """处理多步骤申请流程"""
        print("🔄 开始多步骤申请流程")
        最大步骤数 = 5  # 尝试的最大步骤数
        当前步骤 = 0

        try:
            while 当前步骤 < 最大步骤数:
                当前步骤 += 1

                # 首先处理筛选问题
                self.handle_screening_questions()

                # 查找下一步按钮
                next_button = self.wait_and_find_element(
                    By.CSS_SELECTOR,
                    "button[aria-label='继续下一步'], button[aria-label='继续']",
                )

                if next_button and next_button.is_enabled():
                    print(f"➡️ 点击下一步 ({当前步骤}/{最大步骤数})")
                    next_button.click()
                    time.sleep(2)
                    continue

                # 查找检查申请按钮
                review_button = self.wait_and_find_element(
                    By.CSS_SELECTOR, "button[aria-label='检查申请']"
                )

                if review_button:
                    print("📋 检查申请信息")
                    review_button.click()
                    time.sleep(2)

                    # 最终提交
                    submit_button = self.wait_and_find_element(
                        By.CSS_SELECTOR, "button[aria-label='提交申请']"
                    )

                    if submit_button:
                        print("📤 提交申请")
                        submit_button.click()
                        time.sleep(2)
                        return True

                # 如果找不到按钮，可能卡住了
                print(f"⚠️ 步骤 {当前步骤}: 未找到下一步按钮")
                return False

            print("⚠️ 达到最大步骤数")
            return False

        except Exception as e:
            print(f"❌ 多步骤申请出错: {str(e)}")
            return False

    def saveIntoCSV(self, data, keyword):
        """保存已申请的职位到CSV文件"""
        try:
            export_dir = os.path.join(os.getcwd(), "export", keyword)
            os.makedirs(export_dir, exist_ok=True)

            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = os.path.join(export_dir, f"applied_jobs_{timestamp}.csv")

            print(f"💾 正在保存申请记录...")
            print(f"📊 申请职位数: {len(data)} 个")

            with open(filename, mode="w", newline="", encoding="utf-8-sig") as file:
                fieldnames = [
                    "datetime",
                    "title",
                    "description",
                    "url",
                    "country",
                    "status",
                ]
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                writer.writeheader()

                # 批量写入以提高性能
                batch_size = 50
                for i in range(0, len(data), batch_size):
                    batch = data[i : i + batch_size]
                    writer.writerows(batch)
                    print(
                        f"⏳ 已保存: {min(i + batch_size, len(data))}/{len(data)} 个职位"
                    )

            # 验证导出的数据
            with open(filename, mode="r", encoding="utf-8-sig") as file:
                reader = csv.DictReader(file)
                saved_jobs = list(reader)
                if len(saved_jobs) == len(data):
                    print("✅ 数据验证成功")
                    print(f"📊 总计导出: {len(saved_jobs)} 个职位")
                    print(f"📁 文件保存在: {filename}")
                else:
                    print(
                        f"⚠️ 数据验证失败: 期望 {len(data)} 条记录，实际保存 {len(saved_jobs)} 条"
                    )

        except Exception as e:
            print(f"❌ 保存CSV文件失败: {str(e)}")
            raise

    def saveSearchResultsToCSV(self, data, keyword):
        """保存搜索结果到CSV文件"""
        try:
            export_dir = os.path.join(os.getcwd(), "export", keyword)
            os.makedirs(export_dir, exist_ok=True)

            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = os.path.join(export_dir, f"jobs_{timestamp}.csv")

            print(f"\n💾 正在保存搜索结果...")
            print(f"📊 职位总数: {len(data)} 个")

            with open(filename, mode="w", newline="", encoding="utf-8-sig") as file:
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

                # 批量写入以提高性能
                batch_size = 50
                for i in range(0, len(data), batch_size):
                    batch = data[i : i + batch_size]
                    writer.writerows(batch)
                    print(
                        f"⏳ 已保存: {min(i + batch_size, len(data))}/{len(data)} 个职位"
                    )

            print(f"✅ 已保存所有职位到: {filename}")

            # 验证导出的数据
            with open(filename, mode="r", encoding="utf-8-sig") as file:
                reader = csv.DictReader(file)
                saved_jobs = list(reader)
                if len(saved_jobs) == len(data):
                    print("✅ 数据验证成功")
                    print(f"📊 总计导出: {len(saved_jobs)} 个职位")
                else:
                    print(
                        f"⚠️ 数据验证失败: 期望 {len(data)} 条记录，实际保存 {len(saved_jobs)} 条"
                    )

        except Exception as e:
            print(f"❌ 保存搜索结果失败: {str(e)}")
