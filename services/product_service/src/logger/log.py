import os
import json
import logging
import traceback

__LOGGER = None


def setup_logger(
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
    __LOGGER = logging.getLogger(__name__)
    add_levels()
    add_defaults()

    if os.path.exists(config_path):
        with open(config_path, 'rt') as f:
            config = json.load(f)
            __LOGGER.config.dictConfig(config)
    else:
        __LOGGER.basicConfig(level=default_level)


def add_defaults():
    __LOGGER.marker = "-" * 60
    __LOGGER.step = 1
    __LOGGER.stage = ''


def add_levels():
    __LOGGER.STAGE = 21
    __LOGGER.STEP = 22
    __LOGGER.TRACE = 9

    __LOGGER.addLevelName(__LOGGER.STAGE, 'STAGE')
    __LOGGER.addLevelName(__LOGGER.STEP, 'STEP')
    __LOGGER.addLevelName(__LOGGER.TRACE, 'TRACE')
    __LOGGER.addLevelName(__LOGGER.WARNING, 'WARN')


def INFO(message):
    __LOGGER.info(message, extra=__extra_info())


def TRACE(message):
    __LOGGER.info(message, extra=__extra_info())


def DEBUG(message):
    __LOGGER.info(message, extra=__extra_info())


def ERROR(message):
    __LOGGER.info(message, extra=__extra_info())


def STEP(message):
    __LOGGER.step(__LOGGER.marker, extra=__extra_info())
    __LOGGER.step("%s", message, extra=__extra_info())
    __LOGGER.step(__LOGGER.marker, extra=__extra_info())


def STAGE(message, stage_name=None):
    if stage_name:
        __setup_stage(stage_name)
        __reset_stage()

    print('=' * 60)
    __LOGGER.info()
    print('=' * 60)


def __setup_stage(stage):
    __LOGGER.stage = stage


def __reset_stage():
    __LOGGER.step = 0


def __extra_info():
    frame = traceback.extract_stack()
    file_name = frame[0].split("/")[-1]
    file_line = frame[1]
    return {
        "file_line": "%s:%s" % (file_name, file_line),
        "step": __LOGGER.step,
        "stage": __LOGGER.stage
    }
