from listdir.listdir import *
from listdir.listdir import setup_logging

name = 'listdir'
setup_logging(default_path=os.path.join("/".join(__file__.split('/')[:-1]), 'config', 'loggingConfig.yaml'))