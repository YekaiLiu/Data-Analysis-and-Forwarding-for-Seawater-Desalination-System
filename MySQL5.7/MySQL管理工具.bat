@echo off&title MySQL tools
::设置窗体
mode con cols=45 lines=11
::设置颜色
color 0f
::设置MySQL控制台路径
pushd ".\bin"
::设置MySQL端口
set "po=3306"


:main
cls
echo   ______________________________
echo  ^|                              ^| 
echo  ^|#####    MySQL管理工具   #####^|
echo  ^|______________________________^|
echo   1启动   2关闭   3日志   0密码
echo.
set "cho="
set /p cho=-^> 请选择:
goto main%cho%

:main1
cls
echo   ______________________________
echo  ^|                              ^| 
echo    ###  正在启动MySQL ...
echo  ^|______________________________^|.
echo  正在检测端口占用...
netstat -ano|find "0.0.0.0:%po% " && goto warning
start .\mysqld.exe --defaults-file="..\my.ini" --port=%po%
goto main
::
:warning
echo 警告：一、可能是端口被占用，请修改bat设置
echo       二、或似MySQL已运行，查看任务管理器
pause>nul
exit

:main2
cls
echo   ______________________________
echo  ^|                              ^| 
echo    ###  准备关闭MySQL
echo  ^|______________________________^|.
set "pass="
set /p pass=-^> 请输入密码:
.\mysqladmin -P%po% -uroot -p%pass% shutdown || echo =^> 关闭MySQL失败 && pause>nul && goto main
del ..\data\%computername%.pid
goto main

:main3
start ..\tail.exe -f ..\data\%USERDOMAIN%.err
goto main

:main0
cls
echo   ______________________________
echo  ^|                              ^| 
echo    ###  修改MySQL密码
echo  ^|______________________________^|.
set "passnew="
set /p passnew=-^> 新密码:
echo   ______________^|_______________
echo  ^|                              ^| 
echo    A输原密码         B直接重置 
choice /c:AB
if %errorlevel%==1 goto passnew1
if %errorlevel%==2 goto passnew2
::
:passnew1
set "pass="
set /p pass=-^> 原密码:
.\mysqladmin -P%po% -uroot -p%pass% password %passnew% || echo =^>修改密码失败 && pause>nul && exit
goto main
::
:passnew2
if not exist ..\data\%computername%.pid (goto core)
set /p mypid=<..\data\%computername%.pid
taskkill /f /pid %mypid%
::
:core
set string=password
cls
echo   ______________________________
echo  ^|                              ^| 
echo    ###  重置MySQL密码    牢记！
echo  ^|______________________________^|.
if /i "%passnew%"=="" exit
start .\mysqld.exe --skip-grant-tables
::
:authen
echo use mysql;>.\temp
echo update user set %string%=password("%passnew%") where user="root";>>.\temp
echo flush privileges;>>.\temp
echo quit>>.\temp
mysql<.\temp || set string=authentication_string && goto authen
del .\temp
.\mysqladmin -P%po% -uroot -p%passnew% shutdown || echo =^>重置密码失败 && pause>nul && goto main
cls
choice /c:yn /m 在%po%端口上启动MySQL
if %errorlevel%==1 goto main1
if %errorlevel%==2 goto main