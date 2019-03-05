<h1>Salt Level Sensor Application</h1>

<p>Move the *.service file in this directory to:</p>

<pre>
/lib/systemd/system/
</pre>

<p>Start/Stop/Status of service:</p>

<pre>
sudo systemctl start salt-sensor.service 
sudo systemctl status salt-sensor.service 
  
sudo systemctl stop salt-sensor.service 
sudo systemctl status salt-sensor.service 
</pre>

<p>Enable service on reboot</p>

<pre>
sudo systemctl enable salt-sensor.service
</pre>

<p>Service logging:</p>

<pre>
cat /var/log/daemon.log
</pre>
