@SET PATH=%PATH%;%LOCALAPPDATA%\Programs\Python\Python36
@python "%~dp0source/ff" --gif --gif-iframe 3 --gif-fcount 90 --gif-fpsx 1.0 %*
IF NOT ERRORLEVEL 0 (
  PAUSE
)
PAUSE