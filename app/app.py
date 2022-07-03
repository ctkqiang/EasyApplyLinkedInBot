from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import math


class EasyApplyLinkedinJobBot:
    def __init__(self, account: str, jobs: list, location: str):
        try:
            self.endpoint: str = 'https://www.linkedin.com/jobs/search/'
            self.account: str = account
            self.applicationCount: int = 0
            self.countJob: int = 0
            self.jobsPerPage: int = 25
            self.jobsLocation: str = location
            self.searchKeywords: list = jobs
            self.easyApplyParameter: list = ['?f_AL=true', '&keywords=', '&']
            self.linkProfile: object = webdriver.FirefoxProfile(
                'C:/Program Files/Mozilla Firefox/'  # default directory
            )
            self.driver: object = webdriver.Firefox(self.linkProfile)
        except Exception as e:
            raise Exception(e)

    def main(self):
        for index in range(len(self.searchKeywords)):
            self.driver.get(
                self.endpoint +
                self.easyApplyParameter[0] +
                self.easyApplyParameter[1] +
                self.searchKeywords[index] +
                self.easyApplyParameter[2] +
                self.jobsLocation
            )

            amountOfAvailableJobs: object = self.driver.find_element_by_xpath(
                '//small'
            ).text

            spaceId: object = amountOfAvailableJobs.index(' ')
            totalVacancies: object = amountOfAvailableJobs[0: spaceId]
            totalVacanciesToInt: int = int(totalVacancies.replace(',', ''))
            numberOfReturnedPages: object = math.ceil(
                totalVacancies / self.jobsPerPage
            )
            


if __name__ == '__main__':
    e = EasyApplyLinkedinJobBot(
        account='asd',
        jobs=['flutter'],
        location='United Kingdom'
    )
    e.main()
