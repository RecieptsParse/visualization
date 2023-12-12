import os
import json
import pandas as pd
import sys
import subprocess

try:
    subprocess.run(['/bin/bash', 'install_packages.sh'], check=True)
except subprocess.CalledProcessError as e:
    print(f"Error running shell script: {e}")