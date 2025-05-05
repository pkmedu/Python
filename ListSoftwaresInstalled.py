# -*- coding: utf-8 -*-
"""
Created on Sat Feb 15 22:19:34 2025

@author: muhuri
"""

import winreg

def list_installed_software(registry_path):
    try:
        reg = winreg.ConnectRegistry(None, winreg.HKEY_LOCAL_MACHINE)
        key = winreg.OpenKey(reg, registry_path)

        for i in range(winreg.QueryInfoKey(key)[0]):
            try:
                software_key_name = winreg.EnumKey(key, i)
                software_key = winreg.OpenKey(key, software_key_name)
                software_name = winreg.QueryValueEx(software_key, "DisplayName")[0]
                print(software_name)
            except FileNotFoundError:
                pass  # Some keys may not have "DisplayName"
            except Exception as e:
                print(f"Error: {e}")
    except Exception as e:
        print(f"Could not open registry path: {registry_path}, Error: {e}")

# Check both registry paths
list_installed_software(r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall")
list_installed_software(r"SOFTWARE\Wow6432Node\Microsoft\Windows\CurrentVersion\Uninstall")
