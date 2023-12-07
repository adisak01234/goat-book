from unittest import skip
from time import sleep

from selenium.webdriver import Keys
from selenium.webdriver.common.by import By

from .base import FunctionalTest


class ItemValidationTest(FunctionalTest):
    def check_error_element(self):
        error_elements = self.browser.find_elements(By.CSS_SELECTOR, '.has-error')
        return len([x for x in error_elements if x.is_displayed()]) > 0

    def test_cannot_add_empty_list_items(self):
        # a user goes to the home page and accidentally tries to submit
        # an empty list item. she hits Enter on the empty input box
        self.browser.get(self.live_server_url)
        self.get_item_input_box().send_keys(Keys.ENTER)

        # the home page refreshes, and there is an error message saying
        # that list items cannot be blank
        self.wait_for(
            lambda: self.browser.find_element(By.CSS_SELECTOR, '#id_text:invalid')
        )

        # she tries again with some text for the item, which now works
        self.get_item_input_box().send_keys("Buy milk")
        self.wait_for(
            lambda: self.browser.find_element(By.CSS_SELECTOR, '#id_text:valid')
        )
        self.get_item_input_box().send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table("1: Buy milk")

        # perversely, she now decides to submit a second blank list item

        self.get_item_input_box().send_keys(Keys.ENTER)

        # she receives a similar warning on the list page
        self.wait_for(
            lambda: self.browser.find_element(By.CSS_SELECTOR, '#id_text:invalid')
        )

        # and she can correct it by filling some text in
        self.get_item_input_box().send_keys("Make tea")
        self.wait_for(
            lambda: self.browser.find_element(By.CSS_SELECTOR, '#id_text:valid')
        )
        self.get_item_input_box().send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table("1: Buy milk")
        self.wait_for_row_in_list_table("2: Make tea")

    def test_error_messages_are_cleared_on_input(self):
        # Edith starts a list and causes a validation error:
        self.browser.get(self.live_server_url)
        self.get_item_input_box().send_keys('Banter too thick')
        self.get_item_input_box().send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Banter too thick')
        self.get_item_input_box().send_keys('Banter too thick')
        self.get_item_input_box().send_keys(Keys.ENTER)

        self.wait_for(
            lambda: self.assertTrue(
                self.check_error_element()
            )
        )

        # She starts typing in the input box to clear the error
        self.get_item_input_box().send_keys('a')
        self.get_item_input_box().send_keys(Keys.ENTER)

        # She is pleased to see that the error message disappears
        self.wait_for(
            lambda: self.assertFalse(
                self.check_error_element()
            )
        )