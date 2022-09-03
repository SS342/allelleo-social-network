'''import logging
from rich.logging import RichHandler
import os

FORMAT = "%(message)s"
logging.basicConfig(
    level="NOTSET", format=FORMAT, datefmt="[%X]", handlers=[RichHandler()]
)
log = logging.getLogger("rich")'''


class Logs(object):
    def __init__(self, *, path: str = "\\static\\Logs\\main.txt"):
        self.path = path

        # with open(os.getcwd() + "\\static\\Logs\\main.txt", 'w') as f:

