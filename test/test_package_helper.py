import os
import sys
import unittest

# Append package dir to sys.path
PROJECT_DIR = os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(__file__)), ".."))
sys.path.append(os.path.abspath(os.path.join(PROJECT_DIR)))
from package_helper import read_packagefile


class TestPackageHelper(unittest.TestCase):

    def test_package_helper(self):
        """
        Test apt packagefile
        """
        current_dir = os.path.dirname(os.path.abspath(__file__))
        package_file = os.path.join(current_dir, "../test_data/packages", 'Packagefile')
        packages = read_packagefile(package_file)
        expected_packages = ['binutils',
                             'build-essential',
                             'clang',
                             'mc',
                             'openssh-server',
                             'rsync',
                             'curl',
                             'net-tools',
                             'wget']
        self.assertEqual(packages, expected_packages)


if __name__ == "__main__":
    unittest.main()
