# Installation

1. Download Raspian Stretch Lite image. Image available [here](https://www.raspberrypi.org/downloads/raspbian/).
2. Install [Etcher](https://etcher.io/).
3. Format SD card to prevent fragmentation.
4. Use Etcher to burn image on SD card.
5. Create a empty file named `ssh` on `boot` partition of SD card. This will allow you to `ssh` into the device.
6. Boot raspberry headlessly and connect it to local network via ethernet cable.
7. If raspberry is not booting (only red light on) try to burn image again.
8. Follow instructions available [here](https://gist.github.com/ageitgey/1ac8dbe8572f3f533df6269dab35df65) to install dlib and the face recognition package on the Raspberry Pi.



# GPIO
1. sudo apt-get install wiringpi
2. gpio readall # Will give the mapping between phisical pins and BCM ones
3. On python, execute the commands replacing `PIN` with the BCM code of the pin you are using:
```
import RPi.GPIO as gpio
gpio.setmode(gpio.BCM)
gpio.setup(PIN, gpio.OUT)
gpio.output(PIN, False)
gpio.output(PIN, True)
gpio.output(PIN, False)
gpio.output(PIN, True)
```
