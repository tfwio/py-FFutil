@ECHO OFF
@SET PATH=%PATH%;%LOCALAPPDATA%\Programs\Python\Python36
@python "%~dp0source/ff" --aspect-16x9 %*
rem pause