from selenium import webdriver
import unittest


class NewVisitorTest(unittest.TestCase):
    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    def test_can_start_a_todo_list(self):
        # She checks out the homepage
        self.browser.get("http://localhost:8000")

        # She notices the page title and header mention to-do lists
        self.assertIn("To-Do", self.browser.title)

        # She is invited to enter a to-do item
        self.fail("Finish the test!")

        # She types "Buy peacock features" into a text box

        # when she hit enter, the page updates, and now the page lists
        # "1: Buy peacock features" as an item in a to-do list

        # there is still a text box inviting her to add another item
        # she enters "Use peacock features to make a fly"

        # the page updates again, and now shows both items on her list


if __name__ == "__main__":
    unittest.main()
