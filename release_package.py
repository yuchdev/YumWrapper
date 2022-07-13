# -*- coding: utf-8 -*-
import os
import sys
import argparse
import platform
import json
from subprocess import run
from src.extract_version.version import VERSION

PROJECT_DIR = os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(__file__))))
PYTHON = "python3"
PIP = "pip3"


def is_linux():
    """
    :return: True if system is Linux, False otherwise
    """
    return platform.system() == 'Linux'


def is_macos():
    """
    :return: True if system is macOS, False otherwise
    """
    return platform.system() == 'Darwin'


def is_windows():
    """
    :return: True if system is Windows, False otherwise
    """
    return platform.system() == 'Windows'


if is_macos() or is_linux():
    PYTHON = "python3"
    PIP = "pip3"
elif is_windows():
    PYTHON = "python"
    PIP = "pip"


def wheel_path():
    """
    :return: Path to the wheel file
    """
    return os.path.join(PROJECT_DIR, 'dist', 'yum_wrapper-{}-py3-none-any.whl'.format(VERSION))


def targz_path():
    """
    :return: Path to the *.tar.gx archive
    """
    return os.path.join(PROJECT_DIR, 'dist', 'yum_wrapper-{}.tar.gz'.format(VERSION))


def uninstall_wheel():
    """
    pip.exe uninstall -y yum-wrapper
    """
    run([PIP, 'uninstall', '-y', 'yum-wrapper'])


def build_wheel():
    """
    python.exe -m pip install --upgrade pip
    python.exe -m pip install --upgrade build
    python.exe -m build
    """
    run([PYTHON, '-m', 'pip', 'install', '--upgrade', 'pip'])
    run([PYTHON, '-m', 'pip', 'install', '--upgrade', 'build'])
    run([PYTHON, '-m', 'pip', 'install', 'twine'])
    run([PYTHON, '-m', 'build'])


def install_wheel():
    """
    pip.exe install ./dist/yum_wrapper-{VERSION}-py3-none-any.whl
    """
    run([PIP, 'install', wheel_path()])


def cleanup_old_wheels():
    """
    Remove all previous yum_wrapper-{}-py3-none-any.whl in dist
    """
    if os.path.isdir(os.path.join(PROJECT_DIR, 'dist')):
        for file in os.listdir(os.path.join(PROJECT_DIR, 'dist')):
            if file.startswith('yum_wrapper-'):
                os.remove(os.path.join(PROJECT_DIR, 'dist', file))


def upload_s3():
    """
    Upload the package to S3.
    Example:
    aws s3 cp yum_wrapper--0.9.5-py3-none-any.whl s3://yum-wrapper/packages/ --acl public-read
    It is also possible to change existing ACL:
    aws s3api put-object-acl
        --bucket yum-wrapper
        --key server/yum_wrapper-0.9.5-py3-none-any.whl
        --acl public-read

    Resulting URL would be:
    https://yum-wrapper.s3.us-east-1.amazonaws.com/packages/yum_wrapper-0.9.5-py3-none-any.whl
    """
    run(['aws', 's3', 'cp', wheel_path(), 's3://yum-wrapper/packages/', '--acl=public-read'])
    run(['aws', 's3', 'cp', targz_path(), 's3://yum-wrapper/packages/', '--acl=public-read'])


def tag_release():
    """
    Tag the release on GitHub
    Example:
    git tag -a release.2.9.34 -m"Release 2.9.34"
    git push origin --tags master
    """
    run(['git', 'tag', '-a', 'release.{}'.format(VERSION), '-m', 'Release {}'.format(VERSION)])
    run(['git', 'push', 'origin', '--tags', 'master'])


def create_release(release_file):
    """
    Create a release on GitHub
    Example:
    gh release create release.2.9.34 dist/yum_wrapper-2.9.34-py3-none-any.whl --title 2.9.34 --notes-file RELEASE.md
    """
    run(['gh', 'release', 'create', 'release.{}'.format(VERSION), wheel_path(), targz_path(),
         '--title', '{}'.format(VERSION),
         '--notes-file', release_file])
    run('twine', 'upload', 'dist/*')


def tmp_release_notes(version):
    """
    Read the last release notes in JSON format from release_notes.json and create a temporary release notes file
    """
    # read release_notes.json as dict
    with open('RELEASE_NOTES.json', 'r') as release_json:
        release_notes = json.load(release_json)
        last_release = release_notes['releases'][version]['release_notes']
        release_url = release_notes['release']['download_link']
    # create a temporary release notes file
    with open('RELEASE.md', 'w') as release_tmp:
        release_tmp.write('## Release notes\n')
        for note in last_release:
            release_tmp.write('* {}\n'.format(note))
        release_tmp.write('## Staging Area Download URL\n')
        release_tmp.write('[Wheel Package {} on AWS S3]({})\n'.format(version, release_url))


def main():
    parser = argparse.ArgumentParser(description='Command-line params')
    parser.add_argument('--mode',
                        help='What to do with the package',
                        choices=["build", "install", "reinstall", "uninstall"],
                        default="reinstall",
                        required=False)
    parser.add_argument('--upload-s3',
                        help='Upload the package to S3',
                        action='store_true',
                        required=False)
    parser.add_argument('--create-release',
                        help='Create a release on GitHub',
                        action='store_true',
                        required=False)
    args = parser.parse_args()

    if args.mode == "build":
        build_wheel()
    elif args.mode == "install":
        cleanup_old_wheels()
        build_wheel()
        install_wheel()
    elif args.mode == "reinstall":
        cleanup_old_wheels()
        uninstall_wheel()
        build_wheel()
        install_wheel()
    elif args.mode == "uninstall":
        uninstall_wheel()
    else:
        print("Unknown mode")

    if args.create_release:
        tmp_release_notes(VERSION)
        release_file = os.path.abspath('RELEASE.md')

        tag_release()
        create_release(release_file=release_file)

        if os.path.isdir(os.path.join(PROJECT_DIR, 'ExtractVersion')):
            os.chdir('ExtractVersion')
            tag_release()
            create_release(release_file=release_file)

        os.remove(release_file)

    if args.upload_s3:
        upload_s3()

    return 0


if __name__ == '__main__':
    sys.exit(main())
