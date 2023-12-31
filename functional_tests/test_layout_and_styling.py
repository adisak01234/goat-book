from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from .base import FunctionalTest


MAX_WAIT = 5


class LayoutAndStylingTest(FunctionalTest):
    def test_layout_and_styling(self):
        # user goes  to the home page
        self.browser.get(self.live_server_url)

        # her browser window is set to a very specific size
        self.browser.set_window_size(1024, 768)

        # she notices the input box is nicely centered
        inputbox = self.get_item_input_box()
        self.assertAlmostEquals(
            inputbox.location["x"] + inputbox.size["width"] / 2,
            512,
            delta=10,
        )

        # she starts a new list and sees the input nicely centered there too
        inputbox.send_keys("testing")
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table("1: testing")
        inputbox = self.get_item_input_box()
        self.assertAlmostEquals(
            inputbox.location["x"] + inputbox.size["width"] / 2,
            512,
            delta=10,
        )


