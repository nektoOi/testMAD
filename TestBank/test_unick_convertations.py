import pytest
#from pytest import assume
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import configparser
import configparser
import os
import allure

from PageObj import UnicreditGlavnaya
from PageObj import UnicreditBonusProgram
from PageObj import UnicreditKonvertacii
from PageObj import UnicreditHistoryCard
from PageObj import UnicreditHistoryBonus


class TestConvertation:

    @allure.story("Сверяем все балансы в ЛК")
    def test_all_balance_lk(self, auth_unik_convertation, initWebDriver):
        self.url = auth_unik_convertation
        initWebDriver.get(auth_unik_convertation)

        GlavnayaP = UnicreditGlavnaya.GlavnayaPage(initWebDriver)
        Programm_page = UnicreditBonusProgram.BonusProgram(initWebDriver)
        PageKonvertaciya = UnicreditKonvertacii.Konvertacii(initWebDriver)
        PageHistoryPrograms = UnicreditHistoryBonus.HistoryBonus(initWebDriver)

        with allure.step('Баланс Кэш рублей главная '):
            balance_glavnaya = GlavnayaP.balans_pervoy_karty().replace('+', '').replace(' ', '')

        with allure.step('Баланс Кэш рублей Бонусная программа '):
            Programm_page.click_bonusnie_programmi_v_menu()
            time.sleep(1)
            Programm_page.click_program_kesh_balli()
            time.sleep(2)
            balance_Programm_page = Programm_page.balance_programmi_nayden().replace('+', '').replace(' ', '')

        with allure.step('Баланс Кэш рублей конвертация текущий баланс '):
            initWebDriver.get("https://test.test.ru/conversion/99990051")
            balance_PageKonvertaciya_tekushiy = PageKonvertaciya.tekushiy_balances().replace('+', '').replace(' ', '')
        with allure.step('Баланс Кэш рублей конвертация текущий баланс '):
            balance_PageKonvertaciya_summa_konvertatii = PageKonvertaciya.summa_dlya_konvertacy().replace('+',
                                                                                                          '').replace(
                ' ', '')

        with allure.step('Баланс Кэш рублей бонусная история (текущий) '):
            initWebDriver.get("https://test.test.ru/history/bonus")
            balance_PageHistoryPrograms_tekushiy = PageHistoryPrograms.get_tekushiy_balans_programmi().replace('+',
                                                                                                               '').replace(
                ' ', '')
        with allure.step('Баланс Кэш рублей бонусная история (для конвертации) '):
            balance_PageHistoryPrograms_dlya_konvertacii = PageHistoryPrograms.get_ballov_dostupno_dly_cinvertacii().replace(
                '+', '').replace(' ', '')

        with allure.step("Сравниваем балансы"):
            assert balance_glavnaya == balance_Programm_page == balance_PageKonvertaciya_tekushiy == balance_PageKonvertaciya_summa_konvertatii == balance_PageHistoryPrograms_tekushiy == balance_PageHistoryPrograms_dlya_konvertacii

    @allure.story("Тестирование конвертации 0 баллов")
    def test_convertation_0_ballov(self, auth_unik_convertation, initWebDriver):
        self.url = auth_unik_convertation
        initWebDriver.get(auth_unik_convertation)
        summ_convertation = 0

        PageKonvertaciya = UnicreditKonvertacii.Konvertacii(initWebDriver)

        with allure.step('Баланс Кэш рублей конвертация текущий баланс '):
            initWebDriver.get("https://test.test.ru/conversion/99990051")
            balance_PageKonvertaciya_tekushiy = PageKonvertaciya.tekushiy_balances().replace('+', '').replace(' ',
                                                                                                              '')
        with allure.step('Вводим сумму для конвертации'):
            PageKonvertaciya.type_summ_convertation(summ_convertation)
            time.sleep(0.5)

        with allure.step('Баланс Кэш рублей конвертация текущий баланс '):
            summ_for_convertation = PageKonvertaciya.summa_dlya_konvertacy().replace('+', '').replace(' ', '')
            assert summ_for_convertation == str(summ_convertation)
            time.sleep(0.5)

        with allure.step('Баланс Кэш рублей  будет зачислено на карту'):
            summ_for_zachisleniya = PageKonvertaciya.summa_zachisleniya_na_kartu().replace('+', '').replace(' ', '')
            assert summ_for_zachisleniya == '0'

        with allure.step("Кнопка конвертации неактивна(цвет серый)"):
            color = PageKonvertaciya.check_button_convert_is_blue()
            assert "rgba(224, 224, 224, 1)" == color, print(color)

        with allure.step("Клик по кнопке конвертация"):
            PageKonvertaciya.click_button_convertation()
            time.sleep(0.5)

        with allure.step('Проверяем текущий баланс после нажатия на кнопку конвертировать '):
            balance_PageKonvertaciya_tekushiy_after_convertation = PageKonvertaciya.tekushiy_balances().replace('+',
                                                                                                                '').replace(
                ' ', '')
            assert balance_PageKonvertaciya_tekushiy_after_convertation == balance_PageKonvertaciya_tekushiy

        with allure.step('Проверяем текущий баланс после обновления страницы '):
            initWebDriver.get("https://test.test.ru/conversion/99990051")
            balance_PageKonvertaciya_tekushiy_after_convertation_after_reload_page = PageKonvertaciya.tekushiy_balances().replace(
                '+', '').replace(' ', '')
            print(balance_PageKonvertaciya_tekushiy_after_convertation_after_reload_page)
            assert balance_PageKonvertaciya_tekushiy_after_convertation_after_reload_page == balance_PageKonvertaciya_tekushiy

    @allure.story("Тестирование конвертации 1 баллов")
    def test_convertation_1_ballov(self, auth_unik_convertation, initWebDriver):
        self.url = auth_unik_convertation
        initWebDriver.get(auth_unik_convertation)
        summ_convertation = 1

        PageKonvertaciya = UnicreditKonvertacii.Konvertacii(initWebDriver)
        GlavnayaP = UnicreditGlavnaya.GlavnayaPage(initWebDriver)

        with allure.step('Баланс Кэш рублей конвертация текущий баланс '):
            initWebDriver.get("https://test.test.ru/conversion/99990051")
            balance_PageKonvertaciya_tekushiy = PageKonvertaciya.tekushiy_balances().replace('+', '').replace(' ',
                                                                                                              '')
        with allure.step('Вводим сумму для конвертации'):
            PageKonvertaciya.type_summ_convertation(summ_convertation)
            time.sleep(0.5)

        with allure.step('Баланс Кэш рублей конвертация текущий баланс '):
            summ_for_convertation = PageKonvertaciya.summa_dlya_konvertacy().replace('+', '').replace(' ', '')
            assert summ_for_convertation == str(summ_convertation)
            time.sleep(0.5)

        with allure.step('Баланс Кэш рублей  будет зачислено на карту'):
            summ_for_zachisleniya = PageKonvertaciya.summa_zachisleniya_na_kartu().replace('+', '').replace(' ', '')
            assert summ_for_zachisleniya == str(summ_convertation)

        with allure.step("Кнопка конвертации активна(Цветная)"):
            color = PageKonvertaciya.check_button_convert_is_blue()
            assert "rgba(0, 122, 145, 1)" == color, print(color)

        with allure.step("Клик по кнопке конвертация"):
            PageKonvertaciya.click_button_convertation()
            time.sleep(0.5)

        with allure.step("Клик по кнопке Принято"):
            PageKonvertaciya.click_button_prinato()
            time.sleep(0.2)

        with allure.step('Проверяем текущий баланс На главной '):
            balance_glavnaya =  GlavnayaP.balans_pervoy_karty().replace('+', '').replace(' ', '')
            assert int(balance_glavnaya) == int(balance_PageKonvertaciya_tekushiy) - summ_convertation



        with allure.step('Проверяем текущий баланс после обновления страницы '):
            initWebDriver.get("https://test.test.ru/conversion/99990051")
            balance_PageKonvertaciya_tekushiy_after_convertation_after_reload_page = PageKonvertaciya.tekushiy_balances().replace(
                '+', '').replace(' ', '')
            print(balance_PageKonvertaciya_tekushiy_after_convertation_after_reload_page)
            assert int(balance_PageKonvertaciya_tekushiy_after_convertation_after_reload_page) == int(balance_PageKonvertaciya_tekushiy) - summ_convertation

    @allure.story("Тестирование конвертации 9 баллов")
    def test_convertation_9_ballov(self, auth_unik_convertation, initWebDriver):
        self.url = auth_unik_convertation
        initWebDriver.get(auth_unik_convertation)
        summ_convertation = 9

        PageKonvertaciya = UnicreditKonvertacii.Konvertacii(initWebDriver)
        GlavnayaP = UnicreditGlavnaya.GlavnayaPage(initWebDriver)

        with allure.step('Баланс Кэш рублей конвертация текущий баланс '):
            initWebDriver.get("https://test.test.ru/conversion/99990051")
            balance_PageKonvertaciya_tekushiy = PageKonvertaciya.tekushiy_balances().replace('+', '').replace(' ',
                                                                                                              '')
        with allure.step('Вводим сумму для конвертации'):
            PageKonvertaciya.type_summ_convertation(summ_convertation)
            time.sleep(0.5)

        with allure.step('Баланс Кэш рублей конвертация текущий баланс '):
            summ_for_convertation = PageKonvertaciya.summa_dlya_konvertacy().replace('+', '').replace(' ', '')
            assert summ_for_convertation == str(summ_convertation)
            time.sleep(0.5)

        with allure.step('Баланс Кэш рублей  будет зачислено на карту'):
            summ_for_zachisleniya = PageKonvertaciya.summa_zachisleniya_na_kartu().replace('+', '').replace(' ', '')
            assert summ_for_zachisleniya == str(summ_convertation)

        with allure.step("Кнопка конвертации активна(Цветная)"):
            color = PageKonvertaciya.check_button_convert_is_blue()
            assert "rgba(0, 122, 145, 1)" == color, print(color)

        with allure.step("Клик по кнопке конвертация"):
            PageKonvertaciya.click_button_convertation()
            time.sleep(0.5)

        with allure.step("Клик по кнопке Принято"):
            PageKonvertaciya.click_button_prinato()
            time.sleep(0.2)

        with allure.step('Проверяем текущий баланс На главной '):
            balance_glavnaya = GlavnayaP.balans_pervoy_karty().replace('+', '').replace(' ', '')
            assert int(balance_glavnaya) == int(balance_PageKonvertaciya_tekushiy) - summ_convertation

        with allure.step('Проверяем текущий баланс после обновления страницы '):
            initWebDriver.get("https://unicredit.test.ru/conversion/99990051")
            balance_PageKonvertaciya_tekushiy_after_convertation_after_reload_page = PageKonvertaciya.tekushiy_balances().replace(
                '+', '').replace(' ', '')
            print(balance_PageKonvertaciya_tekushiy_after_convertation_after_reload_page)
            assert int(balance_PageKonvertaciya_tekushiy_after_convertation_after_reload_page) == int(
                balance_PageKonvertaciya_tekushiy) - summ_convertation

    @allure.story("Сверяем все балансы в ЛК после конвертаций")
    def test_all_balance_lk_after_convertation(self, auth_unik_convertation, initWebDriver):
        self.url = auth_unik_convertation
        initWebDriver.get(auth_unik_convertation)

        GlavnayaP = UnicreditGlavnaya.GlavnayaPage(initWebDriver)
        Programm_page = UnicreditBonusProgram.BonusProgram(initWebDriver)
        PageKonvertaciya = UnicreditKonvertacii.Konvertacii(initWebDriver)
        PageHistoryPrograms = UnicreditHistoryBonus.HistoryBonus(initWebDriver)

        with allure.step('Баланс Кэш рублей главная '):
            balance_glavnaya = GlavnayaP.balans_pervoy_karty().replace('+', '').replace(' ', '')

        with allure.step('Баланс Кэш рублей Бонусная программа '):
            Programm_page.click_bonusnie_programmi_v_menu()
            time.sleep(1)
            Programm_page.click_program_kesh_balli()
            time.sleep(2)
            balance_Programm_page = Programm_page.balance_programmi_nayden().replace('+', '').replace(' ', '')

        with allure.step('Баланс Кэш рублей конвертация текущий баланс '):
            initWebDriver.get("https://unicredit.test.ru/conversion/99990051")
            balance_PageKonvertaciya_tekushiy = PageKonvertaciya.tekushiy_balances().replace('+', '').replace(' ', '')
        with allure.step('Баланс Кэш рублей конвертация текущий баланс '):
            balance_PageKonvertaciya_summa_konvertatii = PageKonvertaciya.summa_dlya_konvertacy().replace('+',
                                                                                                          '').replace(
                ' ', '')

        with allure.step('Баланс Кэш рублей бонусная история (текущий) '):
            initWebDriver.get("https://unicredit.test.ru/history/bonus")
            balance_PageHistoryPrograms_tekushiy = PageHistoryPrograms.get_tekushiy_balans_programmi().replace('+',
                                                                                                               '').replace(
                ' ', '')
        with allure.step('Баланс Кэш рублей бонусная история (для конвертации) '):
            balance_PageHistoryPrograms_dlya_konvertacii = PageHistoryPrograms.get_ballov_dostupno_dly_cinvertacii().replace(
                '+', '').replace(' ', '')

        with allure.step("Сравниваем балансы"):
            assert balance_glavnaya == balance_Programm_page == balance_PageKonvertaciya_tekushiy == balance_PageKonvertaciya_summa_konvertatii == balance_PageHistoryPrograms_tekushiy == balance_PageHistoryPrograms_dlya_konvertacii
