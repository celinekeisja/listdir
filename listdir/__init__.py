from listdir.listdir import *
from listdir.listdir import setup_logging
import os, sys; sys.path.append(os.path.dirname(os.path.realpath(__file__)))

name = 'listdir'
setup_logging(default_path=os.path.join("/".join(__file__.split('/')[:-1]), 'config', 'loggingConfig.yaml'))