from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from .base import FunctionalTest


class NewVisitorTest(FunctionalTest):
    def test_can_start_a_todo_list(self):
        # She checks out the homepage
        self.browser.get(self.live_server_url)

        # She notices the page title and header mention to-do lists
        self.assertIn("To-Do", self.browser.title)
        header_text = self.browser.find_element(By.TAG_NAME, "h1").text
        self.assertIn("To-Do", header_text)

        # She is invited to enter a to-do item
        inputbox = self.get_item_input_box()
        self.assertEqual(inputbox.get_attribute("placeholder"), "Enter a to-do item")

        # She types "Buy peacock features" into a text box
        inputbox.send_keys("Buy peacock features")

        # when she hit enter, the page updates, and now the page lists
        # "1: Buy peacock features" as an item in a to-do list
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table("1: Buy peacock features")

        # there is still a text box inviting her to add another item
        # she enters "Use peacock features to make a fly"
        inputbox = self.get_item_input_box()
        inputbox.send_keys("Use peacock features to make a fly")
        inputbox.send_keys(Keys.ENTER)

        # the page updates again, and now shows both items on her list
        self.wait_for_row_in_list_table("1: Buy peacock features")
        self.wait_for_row_in_list_table("2: Use peacock features to make a fly")

    def test_multiple_users_can_start_lists_at_different_urls(self):
        # user1 starts a new to-do list
        self.browser.get(self.live_server_url)
        inputbox = self.get_item_input_box()
        inputbox.send_keys("Buy peacock features")
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table("1: Buy peacock features")

        # she notices that her list has a unique URL
        user1_list_url = self.browser.current_url
        self.assertRegex(user1_list_url, "/lists/.*")

        self.browser.delete_all_cookies()

        # user2 visit the home page. There is no sign of user1's list
        self.browser.get(self.live_server_url)
        page_text = self.browser.find_element(By.TAG_NAME, "body").text
        self.assertNotIn("Buy peacock features", page_text)
        self.assertNotIn("make a fly", page_text)

        # user2 starts a new list by entering a new item
        inputbox = self.get_item_input_box()
        inputbox.send_keys("Buy milk")
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table("1: Buy milk")

        # user2 gets his own unique URL
        user2_list_url = self.browser.current_url
        self.assertRegex(user2_list_url, "/lists/.*")
        self.assertNotEquals(user2_list_url, user1_list_url)

        #  there is no trace of user1's list
        page_text = self.browser.find_element(By.TAG_NAME, "body").text
        self.assertNotIn("Buy peacock features", page_text)
        self.assertNotIn("make a fly", page_text)
