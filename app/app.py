from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import math


class EasyApplyLinkedinJobBot:
    def __init__(self, account: str, jobs: list, location: str):
        try:
            self.appName: str = 'Easy Apply LinkedIn Bot'
            self.endpoint: str = 'https://www.linkedin.com/jobs/search/'
            self.endpointJobViewer: str = 'https: // www.linkedin.com/jobs/view/'
            self.account: str = account
            self.applicationCount: int = 0
            self.countJob: int = 0
            self.jobsPerPage: int = 25
            self.jobsLocation: str = location
            self.searchKeywords: list = jobs
            self.easyApplyParameter: list = [
                '?f_AL=true', '&keywords=', '&', '&start='
            ]
            self.linkProfile: object = webdriver.FirefoxProfile(
                'C:/Program Files/Mozilla Firefox/'  # default directory
            )
            self.driver: object = webdriver.Firefox(self.linkProfile)
        except Exception as e:
            raise Exception(e)

    def main(self):
        id: list = []

        for index in range(len(self.searchKeywords)):
            self.driver.get(
                self.endpoint +
                self.easyApplyParameter[0] +
                self.easyApplyParameter[1] +
                self.searchKeywords[index] +
                self.easyApplyParameter[2] +
                self.jobsLocation
            )

            amountOfAvailableJobs: object = self.driver.find_element(
                'xpath',
                '//small'
            ).text

            spaceId: object = amountOfAvailableJobs.index(' ')
            totalVacancies: object = amountOfAvailableJobs[0: spaceId]
            totalVacanciesToInt: int = int(totalVacancies.replace(',', ''))
            numberOfReturnedPages: object = math.ceil(
                totalVacancies / self.jobsPerPage
            )

            for i in range(numberOfReturnedPages):
                consPageMultiple: object = self.jobsPerPage * i

                self.driver.get(
                    self.endpoint +
                    self.easyApplyParameter[0] +
                    self.easyApplyParameter[1] +
                    self.searchKeywords[index] +
                    self.easyApplyParameter[2] +
                    self.jobsLocation +
                    self.easyApplyParameter[3] +
                    str(consPageMultiple)
                )

                time.sleep(10)

                links: object = self.driver.driver.find_element(
                    'xpath',
                    '//div[@data-job-id]'
                )

                for link in links:
                    temp: object = link.get_attribute('data-job-id')
                    jobId: object = temp.split(':')[-1]
                    id.append(int(jobId))
                ids: object = set(ids)
                jobIds: object = [x for x in ids]

                for jobId in jobIds:
                    position: str = self.endpointJobViewer + str(jobId)
                    self.driver.get(position)
                    self.applicationCount += 1
                    time.sleep(5)

                    try:
                        applyButton: object = self.driver.driver.find_element(
                            'xpath',
                            "//button[contains(@class, 'jobs-apply')]/span[1]"
                        )

                        btnEasyApply: object = applyButton[0]
                    except:
                        btnEasyApply: bool = False

                    applyButton: object = btnEasyApply

                    if applyButton is not False:
                        message: str = '* has an easy apply button'
                        applyButton.click()
                        time.sleep(2)

                        try:
                            self.driver.find_element_by_css_selector(
                                "button[aria-label='Submit application']"
                            ).click()

                            time.sleep(3)

                            self.applicationCount += 1

                            print('--> You had just applied to this Position')
                        except:
                            error: str = '--> > Can\'t apply position ' + position

                            try:
                                applyButton: object = self.driver.find_element_by_css_selector(
                                    "button[aria-label='Continue to next step']"
                                ).click()

                                time.sleep(3)

                                percent: object = self.driver.driver.find_element(
                                    'xpath',
                                    '/html/body/div[3]/div/div/div[2]/div/div/span'
                                ).text

                                percentNumber: int = int(
                                    percen[0:percen.index('%')]
                                )

                                if int(percentNumber) < 25:
                                    print(error)

                                else:
                                    try:
                                        self.onClick()
                                    except:
                                        print(error)
                            except Exception as e:
                                raise Exception(e)
                    else:
                        print('Applied')

    def onClick(self):
        self.driver.find_element_by_css_selector(
            "button[aria-label='Continue to next step']"
        ).click()

        time.sleep(3)

        self.driver.find_element_by_css_selector(
            "button[aria-label='Continue to next step']"
        ).click()

        time.sleep(3)

        self.driver.find_element_by_css_selector(
            "button[aria-label='Review your application']"
        ).click()

        time.sleep(3)

        self.driver.find_element_by_css_selector(
            "button[aria-label='Submit application']"
        ).click()

        self.applicationCount += 1

        print(
            '* You had just Applied to this position!' + position
        )
