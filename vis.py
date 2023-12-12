import os
import json
import sys
import subprocess

try:
    subprocess.run(['/bin/bash', 'install_packages.sh'], check=True)
except subprocess.CalledProcessError as e:
    print(f"Error running shell script: {e}")

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.write("MY APP")

data = dict()


