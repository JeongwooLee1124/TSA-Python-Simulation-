cls

echo off
echo Project 7 Unit Tests
echo Beginning Distribution Class Tests... > capture.txt
echo. >> capture.txt
python test_Distribution.py >> capture.txt 2>&1

echo on
