import os
import sys

# Add the project root directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

print("dir: ", os.path.dirname(os.path.dirname(os.path.abspath('note-app/lib'))))