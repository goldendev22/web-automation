from googletrans import Translator
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from transcodes import transcodes


def translate(sentences, language):
    translator = Translator()
    translation = translator.translate(sentences, dest=language)
    print(f"{translation.text}")
    return translation.text


class TAB:
    def __init__(self):
        self.chrome_options = Options()
        # self.chrome_options.add_argument("--headless")
        self.chrome_options.add_argument('--no-sandbox')
        self.chrome_options.add_argument('--save-page-as-mhtml')
        self.chrome_options.add_argument("--window-size=1920x1080")

        self.chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9014")

        self.browser = webdriver.Chrome(service=Service(ChromeDriverManager().install()),
                                        options=self.chrome_options)
        # self.browser = webdriver.Chrome(executable_path="D:/Apollo/Working/python/chromedriver.exe",
        #                                 options=self.chrome_options)

    def automate_page(self):

        # Switch to iframe
        WebDriverWait(self.browser, 10).until(
            EC.frame_to_be_available_and_switch_to_it(
                (By.XPATH, "//iframe[@src='cid:frame-8274DFDB27B0F318CC2B5016A06A2428@mhtml.blink']")))

        # Add all languages.
        WebDriverWait(self.browser, 10).until(
            EC.element_to_be_clickable(
                (By.XPATH, "//span[text()=' Manage languages ']"))).click()  # Open manage languages.
        time.sleep(1)
        lang_checkboxes = self.browser.find_elements(by=By.XPATH,
                                                     value="//div[@aria-label='Manage languages']/div[2]/div[3]/div[2]/div[@class='lang-item']")
        for index, item in enumerate(lang_checkboxes):
            checkbox = item.find_element(by=By.XPATH, value=".//label/span[1]")
            # move to element
            self.browser.execute_script("arguments[0].scrollIntoView({block: 'center'});", checkbox)
            time.sleep(0.1)
            checkbox.click()

        confirm_btn = self.browser.find_element(by=By.XPATH,
                                                value="//div[@aria-label='Manage languages']/div[@class='el-dialog__footer']/span/button[1]")  # Close manage languages.
        confirm_btn.click()
        time.sleep(1)

        # Select Language
        input_lang = self.browser.find_element(by=By.XPATH, value="//input[@placeholder='Select language']")
        input_lang.click()
        time.sleep(1)

        app_name_text = self.browser.find_element(by=By.XPATH,
                                                  value="//input[@id='AppInfoAppNameInputBox']").get_attribute('value')
        introduction_text = self.browser.find_element(by=By.XPATH,
                                                      value="//textarea[@id='AppInfoAppIntroduceInputBox']").get_attribute(
            'value')
        brief_intro_text = self.browser.find_element(by=By.XPATH,
                                                     value="//input[@id='AppInfoAppBriefInputBox']").get_attribute(
            'value')

        added_langs = self.browser.find_elements(by=By.XPATH,
                                                 value="//div[@class='el-select-dropdown el-popper']/div[@class='el-scrollbar']/div[@class='el-select-dropdown__wrap el-scrollbar__wrap']/ul[1]/li")

        for index, item in enumerate(added_langs):
            selc_item = item.find_element(by=By.XPATH, value=".//span[1]")
            print("Current language --- ", selc_item.text)
            if index != 0:
                input_lang.click()
                time.sleep(1)
                dest_transcode = transcodes[selc_item.text]
                print(dest_transcode)
                selc_item.click()

                trans_app_name = translate(app_name_text, dest_transcode)
                trans_introduction = translate(introduction_text, dest_transcode)
                trans_brief_intro = translate(brief_intro_text, dest_transcode)

                self.update_app_name_field(trans_app_name)
                self.update_introduction_field(trans_introduction)
                self.update_brief_intro_field(trans_brief_intro)

                # move to element
                self.browser.execute_script("arguments[0].scrollIntoView({block: 'center'});", input_lang)
                time.sleep(0.5)
            else:
                selc_item.click()

    def update_app_name_field(self, text):
        app_name = self.browser.find_element(by=By.XPATH, value="//input[@id='AppInfoAppNameInputBox']")
        app_name.clear()
        app_name.send_keys(" ")
        app_name._parent.execute_script("""
                                var elm = arguments[0], text = arguments[1];
                                if (!('value' in elm))
                                  throw new Error('Expected an <input> or <textarea>');
                                elm.focus();
                                elm.value = text;
                                elm.dispatchEvent(new Event('change'));
                                """, app_name, text)
        app_name.send_keys(" ")

    def update_introduction_field(self, text):
        introduction = self.browser.find_element(by=By.XPATH, value="//textarea[@id='AppInfoAppIntroduceInputBox']")
        introduction.clear()
        introduction.send_keys(" ")
        introduction._parent.execute_script("""
                        var elm = arguments[0], text = arguments[1];
                        if (!('value' in elm))
                          throw new Error('Expected an <input> or <textarea>');
                        elm.focus();
                        elm.value = text;
                        elm.dispatchEvent(new Event('change'));
                        """, introduction, text)
        introduction.send_keys(" ")

    def update_brief_intro_field(self, text):
        brief_intro = self.browser.find_element(by=By.XPATH, value="//input[@id='AppInfoAppBriefInputBox']")
        brief_intro.clear()
        brief_intro.send_keys(" ")
        brief_intro._parent.execute_script("""
                var elm = arguments[0], text = arguments[1];
                if (!('value' in elm))
                  throw new Error('Expected an <input> or <textarea>');
                elm.focus();
                elm.value = text;
                elm.dispatchEvent(new Event('change'));
                """, brief_intro, text)
        brief_intro.send_keys(" ")

    def close_browser(self):
        try:
            self.browser.close()
            print("Browser Closed.")
        except Exception as e:
            print(e.msg)


if __name__ == '__main__':
    tab_browser = TAB()
    tab_browser.automate_page()
    # tab_browser.close_browser()
