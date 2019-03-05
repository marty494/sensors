# sensors

<h1>Raspberry Pi SENSORS</h1>

<p>Shell scripts:</p>
<ul>
  <li>email-check.sh => If e-mail's are not working try this</li>
  <li>output-check.sh => List the contents of the sensors output folders</li>
  <li>service-check.sh => Check the status of the sensors services</li>
</ul>

<p>Current sensors:</p>
<ul>
  <li>regeneration => Water flow sensor on the Water Softener's drain tube</li>
  <li>saltlevel => Distance IR sensor in the Water Softener's lid pointing down at the salt</li>
  <li>temperature => Temperature sensor in the Water Softener's outdoor enclosure</li>
  <li>user_modules => Shared library containing error handling and e-mail methods</li>
</ul>

<p>Notificatins:</p>
<ul>
  <li>regeneration => E-mail every time it regenerates</li>
  <li>saltlevel => E-mail when level below 25% and at 0%</li>
  <li>temperature => E-mail when too cold or too hot (appx. 5 or 30 degrees C)</li>
</ul>
