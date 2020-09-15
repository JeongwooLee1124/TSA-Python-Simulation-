cls

echo off
echo Project 7 Unit Tests
echo Beginning Distribution Class Tests... > capture.txt
echo. >> capture.txt
python test_Distribution.py >> capture.txt 2>&1

echo. >> capture.txt
echo. >> capture.txt
echo Beginning Experience tests >> capture.txt
echo. >> capture.txt
python test_Experience.py >> capture.txt 2>&1

echo. >> capture.txt
echo. >> capture.txt
echo Beginning Customer tests >> capture.txt
echo. >> capture.txt
python test_customer.py >> capture.txt 2>&1

echo. >> capture.txt
echo. >> capture.txt
echo Beginning SourcePopulation tests >> capture.txt
echo. >> capture.txt
python test_SourcePopulation.py >> capture.txt 2>&1

echo. >> capture.txt
echo. >> capture.txt
echo Beginning ServerState tests >> capture.txt
echo. >> capture.txt
python test_ServerState.py >> capture.txt 2>&1

echo. >> capture.txt
echo. >> capture.txt
echo Beginning ServerEvent tests >> capture.txt
echo. >> capture.txt
python test_ServerEvent.py >> capture.txt 2>&1

echo. >> capture.txt
echo. >> capture.txt
echo Beginning SystemExit tests >> capture.txt
echo. >> capture.txt
python test_SystemExit.py >> capture.txt 2>&1

echo. >> capture.txt
echo. >> capture.txt
echo Beginning Server tests >> capture.txt
echo. >> capture.txt
python test_Server.py >> capture.txt 2>&1

echo. >> capture.txt
echo. >> capture.txt
echo Beginning QueueEvent tests >> capture.txt
echo. >> capture.txt
python test_QueueEvent.py >> capture.txt 2>&1

echo. >> capture.txt
echo. >> capture.txt
echo Beginning SimQueue tests >> capture.txt
echo. >> capture.txt
python test_SimQueue.py >> capture.txt 2>&1

echo. >> capture.txt
echo. >> capture.txt
echo Beginning Simulation tests >> capture.txt
echo. >> capture.txt
python test_Simulation.py >> capture.txt 2>&1

echo. >> capture.txt
echo. >> capture.txt
echo Beginning SimulationAnalysis tests >> capture.txt
echo. >> capture.txt
python test_SimulationAnalysis.py >> capture.txt 2>&1

echo on
