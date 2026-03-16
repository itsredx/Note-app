import os
import sys

# Add the project root directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
print("dir: ", os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.shared_prefernce import PythraPreferences
from pythra.core import config

pref = PythraPreferences()

APP_NAME = config.get('app_name', 'Note App')
APP_VERSION = config.get('app_version', '0.0.1')
