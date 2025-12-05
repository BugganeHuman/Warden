import logics
import customtkinter
import sys
from pathlib import Path
def main():
    master_key_input = input("write master key: ")
    if not Path("salt.key").exists():
        if len(master_key_input) < 11: 
            print("minimal length of password - 10 chapters")
            sys.exit()
    logics.start(master_key_input)

if __name__ == "__main__":
    main()
