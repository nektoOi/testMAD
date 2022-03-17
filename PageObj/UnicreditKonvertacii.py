import time
from allure_commons.types import AttachmentType
import allure
from selenium.common.exceptions import NoSuchElementException
import pytest
from selenium.webdriver.common.keys import Keys


class Konvertacii:
    def __init__(self, initWebDriver):
        self.driver = initWebDriver

        self.tekushiy_balance = "(//span[contains(@class, 'BalanceValue__ValueContainer')])"
        self.button_podskazka = "(//button[contains(@class, 'QuestionIcon__Container')])"
        self.podskazka = "(//div[contains(@class, 'HelpWithPopup__Details')])"
        self.summa_dlya_konvertacii = "(//input[contains(@class, 'Conversion__ConversionInputField')])[1]"
        self.summa_zachislenia_na_cartu = "(//input[contains(@class, 'Conversion__ConversionInputField')])[2]"
        self.nazvanie_karti_dllya_zachisleniya = "(//div[contains(@class, 'conversion__DropdownZIndexed')])//span[2]"
        self.drop_down_strelka = "(//div[contains(@class, 'conversion__DropdownZIndexed')])//div[2]"
        self.drop_down_pervaya_karta = "((//div[contains(@class, 'Dropdown__DropdownFields')])//span)[1]"
        self.drop_down_vtoraya_karta = "((//div[contains(@class, 'Dropdown__DropdownFields')])//span)[2]"
        self.button_konvertaciya = "(//button[contains(@class, 'styles__ActionButtonView')])"
        self.button_success_convertation = "(//div[text() = 'Понятно'])"


    def get_text_podskazka(self,text_podsk):
        text_podskazki = self.driver.find_element_by_xpath(self.podskazka).text
        assert text_podsk == text_podskazki, print('Текст подсказки на странице \n' + text_podskazki)

    def click_button_podskazka(self):
        self.driver.find_element_by_xpath(self.button_podskazka).click()

    def check_button_convert_is_blue(self):
        color_button = self.driver.find_element_by_xpath(self.button_konvertaciya).value_of_css_property('background-color')
        return color_button


    def tekushiy_balances(self):
        balance_page = self.driver.find_element_by_xpath(self.tekushiy_balance).text
        return balance_page


    def summa_dlya_konvertacy(self):
        balance =  self.driver.find_element_by_xpath(self.summa_dlya_konvertacii).get_attribute('value')
        return balance


    def summa_zachisleniya_na_kartu(self):
        balance = self.driver.find_element_by_xpath(self.summa_zachislenia_na_cartu).get_attribute('value')
        return balance

    def karta_dllya_zachisleniya(self, name_kart):
        assert name_kart in self.driver.find_element_by_xpath(self.nazvanie_karti_dllya_zachisleniya).text


    def open_drop_down(self):
        self.driver.find_element_by_xpath(self.drop_down_strelka).click()
        time.sleep(1)

    def pervaya_karta_drop_down(self, name_kart):
        name_cart = self.driver.find_element_by_xpath(self.drop_down_pervaya_karta).text
        name_cart = str(name_cart.encode("utf-8"))
        assert name_kart in name_cart


    def vtoraya_karta_drop_down(self, name_kart):
        assert name_kart in self.driver.find_element_by_xpath(self.drop_down_vtoraya_karta).text

    def click_vtoraya_karta_drop_down(self):
        self.driver.find_element_by_xpath(self.drop_down_vtoraya_karta).click()
        time.sleep(0.5)

    def type_summ_convertation(self, summ):
        i = 1
        while i < 8:
            self.driver.find_element_by_xpath(self.summa_dlya_konvertacii).send_keys(Keys.BACKSPACE)
            i += 1
        time.sleep(0.2)
        self.driver.find_element_by_xpath(self.summa_dlya_konvertacii).send_keys(summ)

    def click_button_convertation(self):
        self.driver.find_element_by_xpath(self.button_konvertaciya).click()

    def click_button_prinato(self):
        self.driver.find_element_by_xpath(self.button_success_convertation).click()
