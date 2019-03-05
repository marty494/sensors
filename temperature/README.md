<h1>Temperature Sensor Application</h1>

<p>Move the *.service file in this directory to:</p>

<pre>
/lib/systemd/system/
</pre>

<p>Start/Stop/Status of service:</p>

<pre>
sudo systemctl start temp-sensor.service 
sudo systemctl status temp-sensor.service 
  
sudo systemctl stop temp-sensor.service 
sudo systemctl status temp-sensor.service 
</pre>

<p>Enable service on reboot</p>

<pre>
sudo systemctl enable temp-sensor.service
</pre>

<p>Service logging:</p>

<pre>
cat /var/log/daemon.log
</pre>
