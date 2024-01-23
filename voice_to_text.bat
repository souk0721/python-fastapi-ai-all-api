@echo off

goto :activate_venv

:launch
:loop
echo Running Python script...
%PYTHON% "%~dp0\packages\voice_to_text_mo\voice_to_text.py"
echo Script ended, restarting...
goto :loop


:activate_venv
set PYTHON="%~dp0\venv\Scripts\python.exe"
echo venv %PYTHON%
goto :launch

:endofscript

echo.
echo Launch unsuccessful. Exiting.
pause