import logging

import PyPWA.core_libs.initial_logging


def test_InitialLogging_SetDebug():
    """
    Extremely simple test for the initial logging
    """
    PyPWA.core_libs.initial_logging.define_logger(logging.DEBUG)
