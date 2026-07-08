import sys
import os

project_path = os.path.dirname(os.path.abspath(__file__))
if project_path not in sys.path:
    sys.path.append(project_path)


from src.main import app as application


if __name__ == "__main__":
    application.run()