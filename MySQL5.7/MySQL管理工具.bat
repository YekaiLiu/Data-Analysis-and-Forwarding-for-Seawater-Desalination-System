@echo off&title MySQL tools
::���ô���
mode con cols=45 lines=11
::������ɫ
color 0f
::����MySQL����̨·��
pushd ".\bin"
::����MySQL�˿�
set "po=3306"


:main
cls
echo   ______________________________
echo  ^|                              ^| 
echo  ^|#####    MySQL������   #####^|
echo  ^|______________________________^|
echo   1����   2�ر�   3��־   0����
echo.
set "cho="
set /p cho=-^> ��ѡ��:
goto main%cho%

:main1
cls
echo   ______________________________
echo  ^|                              ^| 
echo    ###  ��������MySQL ...
echo  ^|______________________________^|.
echo  ���ڼ��˿�ռ��...
netstat -ano|find "0.0.0.0:%po% " && goto warning
start .\mysqld.exe --defaults-file="..\my.ini" --port=%po%
goto main
::
:warning
echo ���棺һ�������Ƕ˿ڱ�ռ�ã����޸�bat����
echo       ��������MySQL�����У��鿴���������
pause>nul
exit

:main2
cls
echo   ______________________________
echo  ^|                              ^| 
echo    ###  ׼���ر�MySQL
echo  ^|______________________________^|.
set "pass="
set /p pass=-^> ����������:
.\mysqladmin -P%po% -uroot -p%pass% shutdown || echo =^> �ر�MySQLʧ�� && pause>nul && goto main
del ..\data\%computername%.pid
goto main

:main3
start ..\tail.exe -f ..\data\%USERDOMAIN%.err
goto main

:main0
cls
echo   ______________________________
echo  ^|                              ^| 
echo    ###  �޸�MySQL����
echo  ^|______________________________^|.
set "passnew="
set /p passnew=-^> ������:
echo   ______________^|_______________
echo  ^|                              ^| 
echo    A��ԭ����         Bֱ������ 
choice /c:AB
if %errorlevel%==1 goto passnew1
if %errorlevel%==2 goto passnew2
::
:passnew1
set "pass="
set /p pass=-^> ԭ����:
.\mysqladmin -P%po% -uroot -p%pass% password %passnew% || echo =^>�޸�����ʧ�� && pause>nul && exit
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
echo    ###  ����MySQL����    �μǣ�
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
.\mysqladmin -P%po% -uroot -p%passnew% shutdown || echo =^>��������ʧ�� && pause>nul && goto main
cls
choice /c:yn /m ��%po%�˿�������MySQL
if %errorlevel%==1 goto main1
if %errorlevel%==2 goto main