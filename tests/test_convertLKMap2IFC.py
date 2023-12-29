import unittest

from click.testing import CliRunner

from convertLKMap2IFC import convertLKMap2IFC


class TestCLI(unittest.TestCase):
    def setUp(self):
        self.runner = CliRunner()

    def test_only_import_file_given(self):
        with self.runner.isolated_filesystem():
            result = self.runner.invoke(convertLKMap2IFC, ['abc.xtf'])
            self.assertEqual(
                (b"Usage: convertlkmap2ifc [OPTIONS] IMPORT_FILE\r\nTry 'convertlkmap2ifc --h"
                 b"elp' for help.\r\n\r\nError: Missing option '--null_point'.\r\n"),
                result.stdout_bytes)
            self.assertGreater(result.exit_code, 0)

    def test_import_file_not_available(self):
        result = self.runner.invoke(convertLKMap2IFC, ["--null_point", "POINT(1 2 3)", "abc.xtf"])
        self.assertEqual(b'Error: The file abc.xtf cannot be found\r\n', result.stdout_bytes)
        self.assertGreater(result.exit_code, 0)

    def test_invalid_2d_wkt_point(self):
        result = self.runner.invoke(convertLKMap2IFC, ["--null_point", "POINT(1 2)", "abc.xtf"])
        self.assertEqual(b'Error: The WKT Point provided must be 3 Dimensional!\r\n', result.stdout_bytes)
        self.assertGreater(result.exit_code, 0)

    def test_invalid_wkt_point(self):
        result = self.runner.invoke(convertLKMap2IFC, ["--null_point", "(1 2 3)", "abc.xtf"])
        self.assertEqual(b'Error: (1 2 3) is not a valid WKT Point\r\n', result.stdout_bytes)
        self.assertGreater(result.exit_code, 0)

    def test_invalid_wkt_polygon(self):
        result = self.runner.invoke(convertLKMap2IFC,
                                    ["--null_point", "POINT(1 2 3)", "--clip_src", "(3 4 5)", "abc.xtf"])
        self.assertEqual(b'Error: (3 4 5) is not a valid WKT Polygon\r\n', result.stdout_bytes)
        self.assertGreater(result.exit_code, 0)


if __name__ == '__main__':
    unittest.main()
