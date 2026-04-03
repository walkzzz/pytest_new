@echo off
setlocal enabledelayedexpansion

set ENV=test
set MODULE=
set MARK=
set CASE=

:parse_args
if "%~1"=="" goto run_test
if /i "%~1"=="-e" set "ENV=%~2" & shift & shift & goto parse_args
if /i "%~1"=="-m" set "MODULE=%~2" & shift & shift & goto parse_args
if /i "%~1"=="-mk" set "MARK=%~2" & shift & shift & goto parse_args
if /i "%~1"=="-c" set "CASE=%~2" & shift & shift & goto parse_args
shift
goto parse_args

:run_test
echo ========================================
echo 自动化测试框架
echo ========================================
echo 环境: %ENV%

set CMD=python -m pytest

if not "%MODULE%"=="" set "CMD=!CMD! tests/%MODULE%"
if not "%MARK%"=="" set "CMD=!CMD! -m %MARK%"
if not "%CASE%"=="" set "CMD=!CMD! -k %CASE%"

set "CMD=!CMD! --alluredir=allure-results --env=%ENV% -v"

echo 执行命令: !CMD!
!CMD!

if errorlevel 1 (
    echo 测试执行失败
    exit /b 1
)

echo.
echo ========================================
echo 生成Allure报告...
echo ========================================
allure generate allure-results -o allure-report --clean

echo 报告生成完成，是否打开？(Y/N)
set /p open_report=
if /i "%open_report%"=="Y" allure open allure-report

echo 测试完成
