import json
import os
from typing import Dict, List

def extract_user_timestamps() -> Dict[str, List[str]]:
    """
    Read all synthetic log files and extract timestamps for each user.
    Returns a dictionary where keys are usernames and values are lists of timestamps.
    """
    # Get the path to the synthetic_logs directory
    current_dir = os.path.dirname(os.path.abspath(__file__))
    logs_dir = os.path.join(os.path.dirname(os.path.dirname(current_dir)), 'synthetic_logs')
    
    # Dictionary to store timestamps for each user
    user_timestamps = {}
    
    # Read each log file
    for filename in os.listdir(logs_dir):
        if filename.endswith('_logs.json'):
            # Extract username from filename (e.g., 'sim_user_alice_logs.json' -> 'alice')
            username = filename.replace('sim_user_', '').replace('_logs.json', '')
            
            # Read the log file
            with open(os.path.join(logs_dir, filename), 'r') as f:
                logs = json.load(f)
            
            # Extract timestamps
            timestamps = [log['timestamp'] for log in logs]
            user_timestamps[username] = timestamps
    
    return user_timestamps

if __name__ == '__main__':
    # Get timestamps for all users
    timestamps_by_user = extract_user_timestamps()
    
    # Print results
    for user, timestamps in timestamps_by_user.items():
        print(f"\nUser: {user}")
        print(f"Number of timestamps: {len(timestamps)}")
        print("First few timestamps:", timestamps[:5])