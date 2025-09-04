@echo off
TITLE Agenda da Clinica

ECHO ======================================
ECHO  INICIANDO APLICATIVO DA AGENDA...
ECHO  Por favor, aguarde.
ECHO ======================================

:: Ativa o ambiente virtual do Python. 
:: O %~dp0 garante que ele encontre a pasta venv, não importa onde o projeto esteja.
call "%~dp0venv\Scripts\activate.bat"

:: Executa o script principal do seu aplicativo
echo Iniciando interface grafica...
python "%~dp0main_gui.py"

ECHO Aplicativo fechado.