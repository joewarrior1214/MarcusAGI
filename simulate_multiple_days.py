from datetime import date, timedelta
from daily_learning_loop import run_daily_learning_loop

# Set how many days to simulate
days_to_run = 10

# Start date for simulation (e.g., 10 days ago)
start_date = date.today() - timedelta(days=days_to_run - 1)

for i in range(days_to_run):
    run_date = start_date + timedelta(days=i)
    print(f"\n🗓️ Running session for {run_date}")
    run_daily_learning_loop(run_date)
