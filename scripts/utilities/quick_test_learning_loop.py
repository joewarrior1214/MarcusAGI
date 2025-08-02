import sys
sys.path.insert(0, '/workspaces/MarcusAGI')
from core.learning.daily_learning_loop import run_daily_learning_loop

if __name__ == "__main__":
    session = run_daily_learning_loop()
