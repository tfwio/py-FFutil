@ECHO OFF
CALL %~dp0python-bin.cmd
@python "%~dp0source/ff" --aspect-16x9 %*
rem pause