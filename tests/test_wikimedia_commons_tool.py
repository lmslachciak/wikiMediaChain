import unittest
from WikimediaCommonsSearchTool import WikimediaCommonsSearchTool

class TestWikimediaCommonsSearchTool(unittest.TestCase):
    def setUp(self):
        self.tool = WikimediaCommonsSearchTool()

    def test_run_valid_query(self):
        result = self.tool._run("locomotive steam engine", limit=5)
        self.assertIn("Found files on Wikimedia Commons", result)

    def test_run_no_results(self):
        result = self.tool._run("nonexistentquery12345", limit=5)
        self.assertIn("No files found", result)

    def test_run_invalid_limit(self):
        with self.assertRaises(ValueError):
            self.tool._run("locomotive steam engine", limit=-1)

if __name__ == "__main__":
    unittest.main()