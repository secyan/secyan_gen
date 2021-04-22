from unittest import TestCase


class QueryTestCase(TestCase):
    def assert_content_in_arr(self, arr, content: str):
        for a in arr:
            if content in a:
                self.assertTrue(True)
                return
        self.assertTrue(False)

    def assert_content_in(self, content_a: str, content_b: str):
        """
        Assert content a in content b
        :param content_a:
        :param content_b:
        :return:
        """
        self.assertTrue(content_a in content_b)
