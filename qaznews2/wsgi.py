import sys
import os

# Укажите путь к вашему проекту на PythonAnywhere
project_path = '/home/YOUR_USERNAME/qaznews'

if project_path not in sys.path:
    sys.path.append(project_path)

os.chdir(project_path)

from app import app, init_db
init_db()

application = app
