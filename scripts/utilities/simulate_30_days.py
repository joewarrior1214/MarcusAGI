from datetime import datetime, timedelta
import os
from resilience_mode import (
    initialize_marcus_systems,
    run_daily_learning_loop
)

# Initialize Marcus systems
memory_system, curriculum_system, reflection_system = initialize_marcus_systems()

# Set start date (1 day after your last saved session)
start_date = datetime.strptime("2025-08-02", "%Y-%m-%d")

# Loop over 30 days
for i in range(30):
    current_date = start_date + timedelta(days=i)
    date_str = current_date.strftime('%Y-%m-%d')
    print(f"\n📅 Running session for: {date_str}")

    run_daily_learning_loop(
        memory_system,
        curriculum_system,
        reflection_system,
        output_dir="output/sessions",
        today=date_str  # <- ensure your function accepts this arg
    )
