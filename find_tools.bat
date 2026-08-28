@echo off
echo --- WHERE PYTHON --- > tools.txt
where python >> tools.txt 2>&1
echo --- WHERE PY --- >> tools.txt
where py >> tools.txt 2>&1
echo --- WHERE NODE --- >> tools.txt
where node >> tools.txt 2>&1
echo --- WHERE NPM --- >> tools.txt
where npm >> tools.txt 2>&1
echo --- WHERE UVICORN --- >> tools.txt
where uvicorn >> tools.txt 2>&1
echo --- DIR LOCALPROGRAMS PYTHON --- >> tools.txt
dir "%LOCALAPPDATA%\Programs\Python" >> tools.txt 2>&1
echo --- DIR C PROGRAMFILES NODEJS --- >> tools.txt
dir "C:\Program Files\nodejs" >> tools.txt 2>&1
