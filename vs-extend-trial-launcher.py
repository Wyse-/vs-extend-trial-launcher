import datetime
from datetime import timedelta
import winreg
import win32crypt
import os

DEFAULT_REG_KEY_NAME = ""
LICENSE_REGISTRY_KEY_PATH = r'Licenses\5C505A59-E312-4B89-9508-E162F8150517\08878'
DAYS_TO_ADD = 31
DEVENV_EXECUTABLE_PATH = r'C:\Program Files (x86)\Microsoft Visual Studio\2017\Community\Common7\IDE\devenv.exe'
CMD_BG_COLOR_GREEN = 'color 4f'
CMD_BG_COLOR_RED = 'color 2f'


def start_vs():
    os.startfile(DEVENV_EXECUTABLE_PATH)


def get_license_reg_key():
    license_reg_key = winreg.OpenKey(winreg.HKEY_CLASSES_ROOT, LICENSE_REGISTRY_KEY_PATH, 0, winreg.KEY_ALL_ACCESS)
    return license_reg_key


def get_license_unencrypted_data(reg_key):
    encrypted_license_data = winreg.QueryValueEx(reg_key, DEFAULT_REG_KEY_NAME)[0]
    encrypted_license_data = bytearray(win32crypt.CryptUnprotectData(encrypted_license_data)[1])
    return encrypted_license_data


def get_license_expiration_date(data):
    expiration_year = int.from_bytes((data[-16], data[-15]), byteorder='little')
    expiration_month = int.from_bytes((data[-14], data[-13]), byteorder='little')
    expiration_day = int.from_bytes((data[-12], data[-11]), byteorder='little')
    expiration_date = datetime.date(expiration_year, expiration_month, expiration_day)
    return expiration_date


def patch_license_expiration_date(data, reg_key, new_date):
    year_bytes = int.to_bytes(new_date.year, length=2, byteorder='little')
    month_bytes = int.to_bytes(new_date.month, length=2, byteorder='little')
    day_bytes = int.to_bytes(new_date.day, length=2, byteorder='little')

    data[-16] = year_bytes[0]
    data[-15] = year_bytes[1]
    data[-14] = month_bytes[0]
    data[-13] = month_bytes[1]
    data[-12] = day_bytes[0]
    data[-11] = day_bytes[1]

    encrypted_patched_data = win32crypt.CryptProtectData(data)
    winreg.SetValueEx(reg_key, DEFAULT_REG_KEY_NAME, 0, winreg.REG_BINARY, encrypted_patched_data)

try:
	print("Gathering license data from registry...")
	regKey = get_license_reg_key()
	data = get_license_unencrypted_data(regKey)

	print("Extracting expiration date...")
	expirationDate = get_license_expiration_date(data)

	print("Current license expiration date: {}".format(expirationDate))

	print("Patching license expiration date to {} days from now...".format(DAYS_TO_ADD))
	patchedExpirationDate = datetime.datetime.now().date() + timedelta(days=DAYS_TO_ADD)
	patch_license_expiration_date(data, regKey, patchedExpirationDate);

	print("Extracting patched expiration date")
	patchedData = get_license_unencrypted_data(regKey)
	patchedExpirationDateInRegistry = get_license_expiration_date(patchedData)
	print("Patched license expiration date: {}".format(patchedExpirationDate))
	
	assert((patchedExpirationDate - patchedExpirationDateInRegistry).days == 0)
	os.system(CMD_BG_COLOR_GREEN)
	print("Starting devenv.exe and exiting...")
	start_vs()
	quit()
except:
	os.system(CMD_BG_COLOR_RED)