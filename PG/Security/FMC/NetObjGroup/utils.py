import json
import os


"""
Author: Mario Uriel Romero Martínez
Organization:Cisco CX BCS SD-WAN
Description: Python script to generate a report for Network Group objects from Firepower Management Center 
"""

def savefile(filename,dict):
    try:
        with open(filename, 'w') as jf:
            json.dump(dict, jf, indent=4)
        print(f"File {filename} saved...")
    except Exception as e:
        print(f"File {filename} not saved:", e)

