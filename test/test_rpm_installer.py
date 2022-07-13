import os
import sys
import unittest

# Append package dir to sys.path
PROJECT_DIR = os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(__file__)), ".."))
sys.path.append(os.path.abspath(os.path.join(PROJECT_DIR)))
from rpm_installer import Package


class TestRpmInstaller(unittest.TestCase):

    PACKAGE_TEST_DIR = os.path.expandvars("$HOME/Projects/HomeDir/Scripting/test_data/packages")

    @staticmethod
    def read_packages(package_file):
        """
        Read packages from file ignoring empty lines and comments
        :param package_file: file with list of packages to install
        :return: list of packages
        """
        installed_packages = os.path.join(TestRpmInstaller.PACKAGE_TEST_DIR, package_file)
        with open(installed_packages, 'r') as f:
            packages_info_list = f.readlines()
        packages_list = [Package(package) for package in packages_info_list]
        return packages_list

    @staticmethod
    def split_package_info(package_list):
        package_names = [package.name for package in package_list]
        package_architectures = [package.arch for package in package_list]
        package_versions = [package.version for package in package_list]
        package_repos = [package.repo for package in package_list]
        return package_names, package_architectures, package_versions, package_repos

    def test_installed_packages(self):
        """
        Test last version of packages in system
        """
        installed_packages = self.read_packages("yum_list_installed.txt")
        package_names, package_architectures, package_versions, package_repos = self.split_package_info(installed_packages)
        expected_names = ['libxml2-python', 'libxshmfence', 'libxslt', 'libyaml', 'libzstd']
        expected_architectures = ['x86_64', 'x86_64', 'x86_64', 'x86_64', 'x86_64']
        expected_versions = ['2.9.1-6.el7_9.6', '1.2-1.el7', '1.1.28-6.el7', '0.1.4-11.el7_0', '1.5.2-1.el7']
        expected_repos = ['updates', 'anaconda', 'anaconda', 'anaconda', 'epel']
        self.assertEqual(package_names, expected_names)
        self.assertEqual(package_architectures, expected_architectures)
        self.assertEqual(package_versions, expected_versions)
        self.assertEqual(package_repos, expected_repos)

    def test_available_packages(self):
        """
        Test last version of packages in system
        """
        available_packages = self.read_packages("yum_list_available.txt")
        package_names, package_architectures, package_versions, package_repos = self.split_package_info(available_packages)
        expected_names = ['libwpg', 'libwps', 'libxcb', 'libxkbcommon', 'libxkbcommon-x11']
        expected_architectures = ['x86_64', 'x86_64', 'x86_64', 'x86_64', 'x86_64']
        expected_versions = ['0.3.0-1.el7', '0.4.7-1.el7', '1.13-1.el7', '0.7.1-3.el7', '0.7.1-3.el7']
        expected_repos = ['anaconda', 'base', 'anaconda', 'anaconda', 'anaconda']
        self.assertEqual(package_names, expected_names)
        self.assertEqual(package_architectures, expected_architectures)
        self.assertEqual(package_versions, expected_versions)
        self.assertEqual(package_repos, expected_repos)


if __name__ == "__main__":
    unittest.main()
