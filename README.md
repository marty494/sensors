<h1>Raspberry Pi sensors</h1>

<p>The following sensors are all currently deployed to monitor the Water Softener:</p>

<h2>Shell scripts</h2>
<ul>
  <li>email-check.sh => If e-mail's are not working try this</li>
  <li>output-check.sh => List the contents of the sensors output folders</li>
  <li>service-check.sh => Check the status of the sensors services</li>
</ul>

<h2>Current sensors</h2>
<ul>
  <li>regeneration => Water flow sensor on the Water Softener's drain tube</li>
  <li>saltlevel => Distance IR sensor in the Water Softener's lid pointing down at the salt</li>
  <li>temperature => Temperature sensor in the Water Softener's enclosure</li>
  <li>user_modules => Shared library containing error handling and e-mail methods</li>
</ul>

<h2>Notifications</h2>
<ul>
  <li>regeneration => E-mail every time it regenerates (ignores nuisance regenerations below 30 seconds)</li>
  <li>saltlevel => E-mail when level below 25% and at 0%</li>
  <li>temperature => E-mail when too cold or too hot (appx. 5 or 30 degrees C)</li>
</ul>
