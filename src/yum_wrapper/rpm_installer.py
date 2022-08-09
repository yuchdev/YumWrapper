import os.path
import argparse
import sys
from package_helper import execute, read_packagefile
from path_utils import home_dir


class Package:
    """
    Package class
    """

    def __init__(self, package_info: str):
        """
        Package info provided by yum or dnf
        This is a string that have format "Name.Arch Version Repo"
        E.g. "libwpg.x86_64 0.3.0-1.el7 anaconda"
        Repo name may start or may not start with '@' sign, we will remove it later
        """
        package_info_list = package_info.split()
        if len(package_info_list) != 3:
            raise ValueError(f"Invalid package info: {package_info}")
        self.name, self.arch = package_info_list[0].split('.')
        self.version = package_info_list[1]
        self.repo = package_info_list[2][1:] if package_info_list[2].startswith('@') else package_info_list[2]

    def name(self):
        """
        Package name without Arch suffix, e.g. "libwpg"
        """
        return self.name

    def info(self):
        """
        Return full package info in format "Name.Arch Version Repo"
        """
        return f"{self.name}.{self.arch}-{self.version}-{self.repo}"

    def __str__(self):
        """
        Short Package representation, name without Arch suffix, e.g. "libwpg"
        """
        return self.name()

    def __repr__(self):
        """
        Full Package representation, string formatted like "Name.Arch Version Repo"
        """
        return self.info()


class RpmInstaller:
    """
    Install packages on RPM-based Linux distribution
    """

    def __init__(self, tool: str = yum):
        """
        :param tool: 'yum' by default
        """
        self.tool = tool

    def install(self, package):
        """
        Install single RPM package
        """
        execute(['sudo', self.tool, 'install', '-y', package])

    def install_list(self, packages: list):
        """
        Install RPM packages from list
        :param packages: list of packages to install
        """
        for package in packages:
            self.install(package)

    def install_file(self, package_file: str):
        """
        Install RPM packages from file
        Remove comments and empty lines from the list
        :param package_file: file with list of packages to install
        """
        packages = read_packagefile(package_file)
        self.install_list(packages)

    @staticmethod
    def _parse_packages(packages: list) -> list[Package]:
        """
        Parse packages from package information list, provided by 'yum list'
        :param packages: list of packages information strings formatted as "Name.Arch Version Repo"
        :return: list of Package objects
        """
        resulted_packages = []
        for package_info in packages:
            package = Package(package_info=package_info)
            resulted_packages.append(package)
        return resulted_packages

    def list(self, packages: list = None, selection: str = None) -> (list[Package], list[Package]):
        """
        List RPM packages using 'yum list'.
        Response is a list of strings, which consists of a header, which we ignore, and then a list of packages.
        List of packages may include installed and available packages.
        Every package is a string with format "Name.Arch Version Repo".
        We may include a list of packages we'd like to list. Package names support wildcards.
        :param packages: list of available/installed packages to list
        :param selection: selection of packages to list: "installed", "available", or "all"
        :return: tuple of two lists of Package objects, the first one is installed packages, the second is available
        """
        logger.info(f"Installing {packages}")
        base_cmd = [self.tool, 'list']

        if selection is not None and selection in ['available', 'installed', 'all']:
            base_cmd += [selection]

        if packages and isinstance(packages, list):
            base_cmd += packages
        elif packages and isinstance(packages, str):
            base_cmd += [packages]

        # TODO: sort out situation with only installed or only available
        ret_code, packages = execute(base_cmd)
        installed_index = packages.index('Installed Packages')
        available_index = packages.index('Available Packages')
        installed_packages = self._parse_packages(packages[installed_index + 1:available_index])
        available_packages = self._parse_packages(packages[available_index + 1:])

        return installed_packages, available_packages


def main():
    """
    Install everything from package file
    :return: system exit code
    """
    parser = argparse.ArgumentParser(description='Command-line params')
    parser.add_argument('--install',
                        help='Install RPM packages from file',
                        action='store_true',
                        default=False,
                        required=False)
    parser.add_argument('--list',
                        help='List RPM packages',
                        nargs='+',
                        required=False)

    args = parser.parse_args()
    rpm_installer = RpmInstaller('yum')
    if args.install:
        default_packagefile = os.path.join(home_dir(), 'Packagefile')
        rpm_installer.install_file(default_packagefile)
    if len(args.list):
        installed, available = rpm_installer.list(args.list)
        print(f"Installed: {installed}")
        print(f"Available: {available}")

    return 0


###########################################################################
if __name__ == '__main__':
    sys.exit(main())
