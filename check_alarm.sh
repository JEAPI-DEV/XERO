#!/bin/bash

# Get the alarm time from the command-line argument (format: HH:MM:SS)
ALARM_TIME="$1"
echo "Alarm trigger at $ALARM_TIME" >> alarm.log

# Loop indefinitely
while true
do
    # Get the current time (format: HH:MM)
    CURRENT_TIME=$(date +"%H:%M:%S")
    echo "Alarm current time $CURRENT_TIME  <--> $ALARM_TIME" >>  alarm.log

    # Check if the current time matches the alarm time
    if [ "${CURRENT_TIME%:*}" == "${ALARM_TIME%:*}" ]; then
        # Play the wake-up sound using the aplay command
        echo "Alarm triggered at $CURRENT_TIME" >> alarm.log
        vlc wake_up_sound.wav
        break
    fi

    # Wait for 1 second before checking the time again
    sleep 1
done
