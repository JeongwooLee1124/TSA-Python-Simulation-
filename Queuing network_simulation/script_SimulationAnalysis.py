from Simulation import Simulation
from SimulationAnalysis import SimulationAnalysis
import numpy as np
import math
import pandas as pd

simFig2 = Simulation(100)
simFig2.setup("Figure2")
simFig2.run(500)
# sa2 의 결과 확인위해서 실행
sa2 = SimulationAnalysis(simFig2)
sa2.customerSummary
# 아래 명령어 실행하면 제출하기 위한 답이 나옴
sa2.analyzeSystemPerformance()
simFig3 = Simulation(100)
simFig3.setup("Figure3")
simFig3.run(500)
# simFig3를 실행하고 나서 기존에 simFig3 와 결과 비교하기 위해서 아래 실행
# 아래 실행하면 나오는 결과는 simFig2 - simFig3 결과 임
# 워드 파일 Page 16을 참조해서 보면 이해 될 것임
# 여기서 워드 파일 설명에서와 같이 simFig3을 simFig3.setup("Figure3") 까지만 하면
# simFig3.run(500)으로 자동으로 실행함.
# 기본적으로 simFig3.run(500) 으로 시뮬레이션이 끝나고 나서 아래와 같이 실행하는 것이
# 좋은 방법임.
sa2.comparePerformance(simFig3)

# 만약 simFig3의 결과를 알고 싶으면, SimulationAnalysis를 하나 더 만들어서 따로 봐야함.
sa3 = SimulationAnalysis(simFig3)
sa3.analyzeSystemPerformance()

