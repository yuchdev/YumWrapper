# -*- coding: utf-8 -*-

import os
import pathlib
from log_helper import logger

PROJECT_DIR = os.path.join(os.path.realpath(__file__), "..")
HOME_DIR = os.path.join(pathlib.Path.home())


def home_dir():
    """
    :return: Current user home dir
    """
    return HOME_DIR


def project_dir():
    """
    :return: Project dir
    """
    return PROJECT_DIR


def create_symlinks_recursive(src, dst):
    """
    Create symlinks for all files in src directory to dst directory
    :param src: source directory
    :param dst: destination directory
    :return: system exit code
    """
    logger.info("Creating symlinks for directory: {}".format(src))
    if not os.path.isdir(src):
        logger.error("Source directory does not exist: {}".format(src))
        return 1
    if not os.path.isdir(dst):
        logger.error("Destination directory does not exist: {}".format(dst))
        return 1
    for root, dirs, files in os.walk(src):
        for file in files:
            src_file = os.path.join(root, file)
            dst_file = os.path.join(dst, file)
            if os.path.islink(dst_file) or os.path.isfile(dst_file):
                logger.info("Removing existing symlink: {}".format(dst_file))
                os.remove(dst_file)
            logger.info("Creating symlink: {}".format(dst_file))
            os.symlink(src_file, dst_file)
    return 0
