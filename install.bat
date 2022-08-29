type LICENSE
:PROMPT
SET /P AREYOUSURE=Do you agree with the terms of the license? (y/[n])?
IF /I "%AREYOUSURE%" NEQ "y" GOTO END
python-3.10.6-amd64.exe InstallAllUsers=1 PrependPath=1 Include_test=0 ^
&& python -m ensurepip && python -m pip install -r backend\requirements.txt && node-v16.17.0-x64.msi && cd frontend && npm install

:END
