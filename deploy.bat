@echo off
cd /d c:\Users\ponshivavel\pysprak\Socialmedia-trend-analysis-pyspark
git init
git add .
git commit -m "first deploy"
git branch -M main
git remote add origin https://github.com/ponshivavel/Socialmedia-trend-analysis-pyspark
git push -u origin main
pause
