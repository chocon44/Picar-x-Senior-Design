# Alternative 1 - Autostart service
# Save this as /etc/systemd/system/picar.service
[Unit]
Description=PiCar-X Auto Start Service
After=multi-user.target

[Service]
Type=simple
User=pi
WorkingDirectory=/home/pi/your_script_directory
ExecStart=/usr/bin/python3 /home/pi/your_script_directory/your_script.py
Restart=always

[Install]
WantedBy=multi-user.target

# enable it bash 
sudo systemctl enable picar.service
sudo systemctl start picar.service

# Alternative 2 rc.local
python3 /home/pi/your_script_directory/your_script.py &
