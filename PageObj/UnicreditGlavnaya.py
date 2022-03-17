from selenium.common.exceptions import NoSuchElementException
import pytest


class GlavnayaPage:
    def __init__(self, initWebDriver):
        self.driver = initWebDriver

        # Бонусы и карты
        self.bonus_list = '//div[contains(@class, "CardHolder__Container")]'
        self.button_bonus = "//button[contains(@class, 'TabSection__Container')][1]"
        self.button_kartiy = "//button[contains(@class, 'TabSection__Container')][2]"
        self.pervaya_karta_img = '(//div[contains(@class, "ImageMain__ImageContainer")])[1]/img'
        self.vtoraya_karta_img = '(//div[contains(@class, "ImageMain__ImageContainer")])[2]/img'
        self.balans_pervoi_karti = '(//div[contains(@class, "CardHolder__Container")][1]//span[contains(@class, "BalanceValue__ValueContainer")])[1]'
        self.balans_vtoroy_karti = '(//div[contains(@class, "CardHolder__Container")][2]//span[contains(@class, "BalanceValue__ValueContainer")])[1]'
        self.privyazka_name_pervaya = "(//span[contains(@class, 'LinkedItem__Name')])[1]"
        self.privyazka_name_vtoraya = "(//span[contains(@class, 'LinkedItem__Name')])[2]"
        self.balance_card_privyazka_k_pervoy = '(//div[contains(@class, "CardHolder__Container")][1]//span[contains(@class, "BalanceValue__ValueContainer")])[2]'

        # Раздел левое меню
        self.menu_moi_karti = '//div[text() = "Мои карты"]/ancestor::div[contains(@class,  "Collapse__Container")]'

        # Раздел Возможности
        self.sekciya_vozmozhnosty = '//section[contains(@class, "PageSection__Container")][1]'
        self.title_vozmozhnosty = "//section[contains(@class, 'PageSection__Container')][1]/descendant::span[contains(@class, 'Title')]"
        self.banner_vozmozhnosty = '//section[contains(@class, "PageSection__Container")][1]/descendant::div[contains(@class, "Banner__BannerContainer")]'
        self.button_switch_banner_back_vozmozhnosty = '//section[contains(@class, "PageSection__Container")][1]/descendant::div[contains(@class, "Controls__Control")][1]'  # Кнопка переключения баннера назад
        self.button_switch_banner_forward_vozmozhnosty = '//section[contains(@class, "PageSection__Container")][1]/descendant::div[contains(@class, "Controls__Control")][2]'  # Кнопка переключения баннера вперед

        # Раздел бонучные программы
        self.sekciya_bonus_programm = '//section[contains(@class, "PageSection__Container")][2]'
        self.title_bonus_programm = "//section[contains(@class, 'PageSection__Container')][2]/descendant::span[contains(@class, 'Title')]"
        self.all_programm = "//section[contains(@class, 'PageSection__Container')][2]"


    def kolicgestvo_kart_ravno(self, kart_count):

        karti = self.driver.find_elements_by_xpath(self.bonus_list)
        assert len(karti) == kart_count
        #print('------------------------'+str(len(karti)))

    def pervaya_karta(self, img_url):
        img = self.driver.find_element_by_xpath(self.pervaya_karta_img).get_attribute('src')
        #print(img)
        assert img == img_url

    def balans_pervoy_karty(self):
        balans = self.driver.find_element_by_xpath(self.balans_pervoi_karti).text
        #assert ballance in balans
        return balans

    def vtoraya_karta(self, img_url):
        img = self.driver.find_element_by_xpath(self.vtoraya_karta_img).get_attribute('src')
        #print(img)
        assert img == img_url

    def balans_vtoroy_karty(self):
        try:
            self.driver.find_element_by_xpath(self.balans_vtoroy_karti).click()
            return False
        except NoSuchElementException:
            return True
        #return False

    def pereyti_k_kartam_na_glavnoy(self):
        self.driver.find_element_by_xpath(self.button_kartiy).click()

    def check_nemu_left(self, all_menu):

        for punkt_menu in all_menu:
            self.driver.find_element_by_xpath(f'//div[text() = "{punkt_menu}"]')

    def check_karti_in_menu(self, karti):

        for karta in karti:
            self.driver.find_element_by_xpath(f"//div[contains(text(), '{karta}')]")

    def get_name_privyazka_pervaya(self):
        privyazka = self.driver.find_element_by_xpath(self.privyazka_name_pervaya).text
        return privyazka

    def get_name_privyazka_vtoraya(self):
        privyazka = self.driver.find_element_by_xpath(self.privyazka_name_vtoraya).text
        return privyazka

    def get_ballance_privyazka_pervaya(self):
        balance = self.driver.find_element_by_xpath(self.balance_card_privyazka_k_pervoy).text
        return balance

    # Раздел Возможности
    def razdel_vozmozhnosty(self):
        title_razdel = self.driver.find_element_by_xpath(self.title_vozmozhnosty).text
        assert title_razdel == 'Возможности'

    def get_banner_vozmozhnosty(self):
        self.driver.find_element_by_xpath(self.banner_vozmozhnosty)

    def perekluchenie_bannera_nazad_vozmozhnosty(self):
        self.driver.find_element_by_xpath(self.button_switch_banner_back_vozmozhnosty).click()

    def perekluchenie_bannera_vpered_vozmozhnosty(self):
        self.driver.find_element_by_xpath(self.button_switch_banner_forward_vozmozhnosty).click()


    # Раздел Бонусные программы

    def razdel_bonus_programm(self):
        title_razdel = self.driver.find_element_by_xpath(self.title_bonus_programm).text
        assert title_razdel == 'Бонусные программы'

    def check_programm_name(self, name_programm):
        programm_name = self.driver.find_element_by_xpath(self.all_programm).text
        assert name_programm in programm_name
