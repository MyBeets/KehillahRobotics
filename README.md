# KehillahRobotics:
the raspberry pi and arduino code for the Kehillah entry for the 2023 sailbot competition
<br />
<br />
## Raspberry pi setup:
to connect the pi to your laptop you'll need to remove the sd card and insert it into your computer.
Then go to the file labelled 'wpa_supplicant.conf' and comment (add a '#' to the beginning of) the lines starting with ssid and psk
then uncomment (remove the '#') from the lines starting with ssid and psk under the header of whatever wifi you are using (this will generally be kehillah)
the two presets for wifi currently are my home router and the Kehillah_Student wifi.
<br />
<br />
once you've connected the wifi you'll go into cmd (windows) or terminal (mac) and connect by entering the command
