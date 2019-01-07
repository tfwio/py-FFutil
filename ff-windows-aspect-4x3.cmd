@ECHO OFF
CALL %~dp0python-bin.cmd
@python "%~dp0source/ff" --aspect-4x3 %*
rem pause