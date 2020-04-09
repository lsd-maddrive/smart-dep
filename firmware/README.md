# Firmware for NodeMCU (Micropython)

## Micropython intallation (based on [this manual](https://docs.micropython.org/en/latest/esp8266/tutorial/intro.html))

1. Install [requirements.txt](requirements.txt)
2. Download firmware for [ESP8266](http://micropython.org/download#esp8266)
3. Upload micropython to chip:
```bash
esptool.py --port /dev/ttyUSB0 erase_flash
esptool.py --port /dev/ttyUSB0 --baud 460800 write_flash --flash_size=detect 0 esp8266-20170108-v1.8.7.bin
```

> If there are errors - change baud to 115200

> Dont forget - you have your own port and firmware filename!

##

