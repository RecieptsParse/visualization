import os
import json
import sys
import subprocess
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

try:
    subprocess.run(['/bin/bash', 'install_packages.sh'], check=True)
except subprocess.CalledProcessError as e:
    print(f"Error running shell script: {e}")

st.write("MY APP")
