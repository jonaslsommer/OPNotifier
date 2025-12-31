import os
from dotenv import load_dotenv
from pathlib import Path
import sys

# EXE folder
base_path = Path(sys.executable).parent.parent

# Folder containing your data
data_folder = base_path / "TCB_data"

# Path to the .env file
env_file = data_folder / ".env"

# Optional: print path for debugging
print(f"Loading .env from: {env_file}")

# Load .env
load_dotenv(dotenv_path=env_file)

# Access variables
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
GUILD_ID = os.getenv('DISCORD_GUILD_ID')
