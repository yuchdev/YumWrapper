import subprocess


def execute(command: list):
    """
    Execute command
    :param command: list of command and arguments
    """
    # check_output
    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    output = result.stdout.decode("utf-8")
    # trim leading and training whitespaces in any element
    output_list = [s.strip() for s in output.split('\n') if s]
    ret_code = result.returncode
    return ret_code, output_list


def read_packagefile(package_file: str):
    """
    Read packages from file ignoring empty lines and comments
    :param package_file: file with list of packages to install
    :return: list of packages
    """
    with open(package_file, 'r') as f:
        packages = f.readlines()
    packages = [package.strip() for package in packages if package.strip() and not package.startswith('#')]
    return packages
