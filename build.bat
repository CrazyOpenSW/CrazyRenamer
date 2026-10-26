@echo off
setlocal enabledelayedexpansion

echo STARTING BATCH SCRIPT...
echo.

:: ----------------------------------------------------
:: 1. SETUP
:: ----------------------------------------------------
set BASE_NAME=CrazyRenamer_v
set ICON_FILE=app.ico
set VERSION_FILE=version_released.txt
set PYINSTALLER_COMMAND=pyinstaller
set "VERSION="

set "SCRIPT_DIR=%~dp0"
set "ICON_PATH=%SCRIPT_DIR%%ICON_FILE%"
set "VERSION_PATH=%SCRIPT_DIR%%VERSION_FILE%"

if not exist "%VERSION_PATH%" (
    echo ERRORE: File "%VERSION_FILE%" non trovato.
    echo Crea un file di testo con una sola riga, ad esempio: v1.0.0
    pause
    exit /b 1
)

if not exist "%ICON_PATH%" (
    echo ERRORE: Icona non trovata in "%ICON_PATH%"
    pause
    exit /b 1
)

:: ----------------------------------------------------
:: 2. LETTURA DELLA VERSIONE
:: ----------------------------------------------------
for /f "usebackq tokens=*" %%i in ("%VERSION_PATH%") do (
    set "VERSION=%%i"
    goto :VERSION_READ
)

:VERSION_READ
set "VERSION_CLEANED=!VERSION: =!"

if not defined VERSION_CLEANED (
    echo ERRORE: Versione vuota nel file di versione.
    pause
    exit /b 1
)

set "FINAL_EXE_NAME=%BASE_NAME%!VERSION_CLEANED!.exe"

echo Versione: !VERSION_CLEANED!
echo Nome finale: %FINAL_EXE_NAME%
echo.

:: ----------------------------------------------------
:: 3. PULIZIA FILE VECCHI
:: ----------------------------------------------------
if exist "%BASE_NAME%.spec" del "%BASE_NAME%.spec"
if exist "build" rmdir /s /q build

:: ----------------------------------------------------
:: 4. COMPILAZIONE
:: ----------------------------------------------------
echo Avvio compilazione...
"%PYINSTALLER_COMMAND%" ^
  --onefile ^
  --windowed ^
  --name "%FINAL_EXE_NAME%" ^
  --clean ^
  --icon "%ICON_PATH%" ^
  "main.py"

:: ----------------------------------------------------
:: 5. RISULTATO
:: ----------------------------------------------------
if exist "dist\%FINAL_EXE_NAME%" (
    echo -----------------------------------------------------
    echo COMPILAZIONE COMPLETATA CON SUCCESSO!
    echo File generato: dist\%FINAL_EXE_NAME%

    echo Pulizia vecchi eseguibili...
    for %%f in (%BASE_NAME%*.exe) do (
        echo Eliminazione di %%f...
        del /f /q "%%f"
    )

    echo Copia dell'eseguibile nella root...
    copy /y "dist\%FINAL_EXE_NAME%" "."

    echo.

    echo -----------------------------------------------------
) else (
    echo -----------------------------------------------------
    echo ERRORE: La compilazione e' fallita.
    echo Controlla i messaggi di PyInstaller.
    echo -----------------------------------------------------
)

endlocal
pause
