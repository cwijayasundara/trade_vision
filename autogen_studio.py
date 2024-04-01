import subprocess
from dotenv import load_dotenv

load_dotenv()

subprocess.run(["autogenstudio", "ui", "--port", "8081"])
