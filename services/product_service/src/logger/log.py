import os
import json
import logging
import logging.config
import traceback

from utils.constants import APP_NAME


def setup_logger(
    logger_name=None,
    config_path='logging.json',
    default_level=logging.INFO,
    logging_env=None
):
    """
        Sets up the logger.
        * Adds levels
        * configures defaults
        * configures logger
    """
    if not logger_name:
        logger_name = APP_NAME
    logger = logging.getLogger(logger_name)
    add_levels(logger)
    add_defaults(logger)
    dirname = os.path.dirname(__file__)
    pathname = os.path.join(dirname, config_path)
    if os.path.exists(pathname):
        with open(pathname, 'rt') as f:
            config = json.load(f)
            logging.config.dictConfig(config)
    else:
        logging.basicConfig(level=default_level)


def add_defaults(logger):
    logger.marker = "-" * 60
    logger.step = 1
    logger.stage = ''


def add_levels(logger):
    logger.STAGE = 21
    logger.STEP = 22
    logger.TRACE = 9
    logger.WARNING = logging.WARN

    logging.addLevelName(logger.STAGE, 'STAGE')
    logging.addLevelName(logger.STEP, 'STEP')
    logging.addLevelName(logger.TRACE, 'TRACE')
    logging.addLevelName(logger.WARNING, 'WARN')


def INFO(message, logger=None):
    if not logger:
        logger = logging.getLogger(APP_NAME)
    logger.info(message, extra=__extra_info())


def TRACE(message, logger=None):
    if not logger:
        logger = logging.getLogger(APP_NAME)
    logger.trace(message, extra=__extra_info())


def DEBUG(message, logger=None):
    if not logger:
        logger = logging.getLogger(APP_NAME)
    logger.debug(message, extra=__extra_info())


def ERROR(message, logger=None):
    if not logger:
        logger = logging.getLogger(APP_NAME) 

def STEP(message, logger=None):
    if not logger:
        logger = logging.getLogger(APP_NAME)
    logger.step(logger.marker, extra=__extra_info())
    logger.step("%s", message, extra=__extra_info())
    logger.step(logger.marker, extra=__extra_info())


def STAGE(message, stage_name=None, logger=None):
    if not logger:
        logger = logging.getLogger(APP_NAME)

    if stage_name:
        __setup_stage(stage_name)
        __reset_stage()

    print('=' * 60)
    logger.info()
    print('=' * 60)


def __setup_stage(stage, logger=None):
    if not logger:
        logger = logging.getLogger(APP_NAME)
    logger.stage = stage


def __reset_stage(logger=None):
    if not logger:
        logger = logging.getLogger(APP_NAME)
    logger.step = 0


def __extra_info():
    return {}
