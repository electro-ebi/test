import sys
from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need fine tuning.
build_exe_options = {"packages": ["os", "tkinter", "sqlite3", "hashlib","pyperclip","requests","uuid"]}

base = None
if sys.platform == "win32":
    base = "Win32GUI"

setup(
    name="CircleCalculator",
    version="1.0",
    description="Circle Calculator Application",
    options={"build_exe": build_exe_options},
    executables=[Executable("radiusCalaculator.py", base=base)]
)

