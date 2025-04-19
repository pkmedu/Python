# -*- coding: utf-8 -*-
"""
Created on Mon Feb  3 09:58:23 2025

@author: Pradip.Muhuri
"""

import winreg

def get_installed_apps(root, registry_path):
    """Query the registry key for installed applications."""
    apps = []
    try:
        key = winreg.OpenKey(root, registry_path)
    except FileNotFoundError:
        return apps

    for i in range(0, winreg.QueryInfoKey(key)[0]):
        try:
            subkey_name = winreg.EnumKey(key, i)
            subkey = winreg.OpenKey(key, subkey_name)
            try:
                # "DisplayName" is typically the name of the application.
                app_name, _ = winreg.QueryValueEx(subkey, "DisplayName")
                apps.append(app_name)
            except FileNotFoundError:
                # Some subkeys might not have a DisplayName.
                pass
        except EnvironmentError:
            break
    return apps

def list_installed_applications():
    """Combine installed applications from various registry locations."""
    registry_locations = [
        (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall"),
        (winreg.HKEY_CURRENT_USER,  r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall"),
        (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall")
    ]
    
    installed_apps = []
    for root, path in registry_locations:
        installed_apps.extend(get_installed_apps(root, path))
    
    # Remove duplicates and sort the list.
    return sorted(set(installed_apps))

if __name__ == "__main__":
    apps = list_installed_applications()
    print("Installed Applications:")
    for app in apps:
        print(" -", app)
