@ECHO OFF
CALL %~dp0python-bin.cmd
@python "%~dp0source/ff" --pix %*
pause