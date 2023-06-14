import re
import subprocess

def set_alarm(query):
    # Regex pattern to extract the alarm time
    time_pattern = r"(?:(?:set\s+(?:a\s+)?timer|set\s+(?:an\s+)?alarm)\s+(?:for\s+)?)?(\d{1,2}:\d{2})\s*(am|pm)?"
    time_match = re.search(time_pattern, query, re.IGNORECASE)

    if time_match:
        # Extract the alarm time
        alarm_time = time_match.group(1)
        am_pm = time_match.group(2)
        if am_pm is not None:
            # Convert 12-hour time to 24-hour time
            alarm_time = subprocess.run(['date', '+%H:%M', '-d', f"{alarm_time} {am_pm}"], stdout=subprocess.PIPE).stdout.decode().strip()
            
        start_alarm(alarm_time)
        return(f"Alarm set for {alarm_time}")
    else:
        return("Alarm time not found")

def start_alarm(alarm_time):
    # Run the bash script to check the alarm time in the background
    subprocess.Popen(['./check_alarm.sh', alarm_time], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
