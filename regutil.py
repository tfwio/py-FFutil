# regutil.py

# https://stackoverflow.com/questions/15128225/python-script-to-read-and-write-a-path-to-registry#23624136
class w_util:
  REG_PATH = "SOFTWARE\\Plex, Inc.\\Plex Media Server"
  REG_KEY  = "LocalAppDataPath"

  @staticmethod
  def set_reg(name, value):
    import winreg as _winreg
    try:
      _winreg.CreateKey(_winreg.HKEY_CURRENT_USER, REG_PATH)
      registry_key = _winreg.OpenKey(_winreg.HKEY_CURRENT_USER, REG_PATH, 0, _winreg.KEY_WRITE)
      _winreg.SetValueEx(registry_key, name, 0, _winreg.REG_SZ, value)
      _winreg.CloseKey(registry_key)
      return True
    except WindowsError:
      return False

  @staticmethod
  def get_reg(key=w_util.REG_KEY,regpath=w_util.REG_PATH):
    import winreg as _winreg
    try:
      registry_key   = _winreg.OpenKey(_winreg.HKEY_CURRENT_USER, REG_PATH, 0, _winreg.KEY_READ)
      value, _ = _winreg.QueryValueEx(registry_key, key)
      _winreg.CloseKey(registry_key)
      return value
    except WindowsError:
      return None

