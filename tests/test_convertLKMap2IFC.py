import unittest

from click.testing import CliRunner

from convertLKMap2IFC import convertLKMap2IFC


class TestCLI(unittest.TestCase):
    def setUp(self):
        self.runner = CliRunner()

    def test_only_import_file_given(self):
        with self.runner.isolated_filesystem():
            result = self.runner.invoke(convertLKMap2IFC, ['abc.xtf'])
            self.assertGreater(result.exit_code, 0)

    def test_import_file_not_available(self):
        result = self.runner.invoke(convertLKMap2IFC, ["POINT(1 2 3)", "abc.xtf"])
        self.assertEqual(b'Error: The file abc.xtf cannot be found', result.stdout_bytes.strip())
        self.assertGreater(result.exit_code, 0)

    def test_invalid_2d_wkt_point(self):
        result = self.runner.invoke(convertLKMap2IFC, ["POINT(1 2)", "abc.xtf"])
        self.assertEqual(b'Error: The WKT Point provided must be 3 Dimensional!', result.stdout_bytes.strip())
        self.assertGreater(result.exit_code, 0)

    def test_invalid_wkt_point(self):
        result = self.runner.invoke(convertLKMap2IFC, ["(1 2 3)", "abc.xtf"])
        self.assertEqual(b'Error: (1 2 3) is not a valid WKT Point', result.stdout_bytes.strip())
        self.assertGreater(result.exit_code, 0)

    def test_invalid_wkt_polygon(self):
        result = self.runner.invoke(convertLKMap2IFC,
                                    ["--clip_src", "(3 4 5)", "POINT(1 2 3)", "abc.xtf"])
        self.assertEqual(b'Error: (3 4 5) is not a valid WKT Polygon', result.stdout_bytes.strip())
        self.assertGreater(result.exit_code, 0)


if __name__ == '__main__':
    unittest.main()
