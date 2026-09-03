import logging

from core.config import LOG_PATH


def configure_logging():
    logging.basicConfig(
        level=logging.INFO,
        format=(
            "%(asctime)s | %(levelname)s | "
            "%(name)s | %(message)s"
        ),
        handlers=[
            logging.FileHandler(
                LOG_PATH,
                encoding="utf-8"
            ),
            logging.StreamHandler(),
        ],
        force=True,
    )

    logging.getLogger("discord").setLevel(
        logging.INFO
    )
