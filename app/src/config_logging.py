import logging


def setup():
    logging.basicConfig(
        level=logging.DEBUG,
        format="[%(levelname)s][%(name)s]: %(asctime)s - %(message)s",
    )
