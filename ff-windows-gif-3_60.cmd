@ECHO OFF
CALL %~dp0python-bin.cmd
@python "%~dp0source/ff" --gif --gif-iframe 3 --gif-fcount 60 --gif-fpsx 1.0 %*
IF NOT ERRORLEVEL 0 (
  PAUSE
)