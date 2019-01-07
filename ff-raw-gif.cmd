@ECHO OFF
CALL %~dp0python-bin.cmd
@python "%~dp0source/ff" --info %*
@python "%~dp0source/ff" --FFnfo %*
pause