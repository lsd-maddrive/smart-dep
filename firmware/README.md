# Firmware for NodeMCU (Micropython)

## Micropython intallation (based on [this manual](https://docs.micropython.org/en/latest/esp8266/tutorial/intro.html))

1. Install [requirements.txt](requirements.txt)
2. Download firmware for [ESP8266](http://micropython.org/download#esp8266)
3. Upload micropython to chip:
```bash
esptool.py --port /dev/ttyUSB0 erase_flash
esptool.py --port /dev/ttyUSB0 --baud 460800 write_flash --flash_size=detect 0 esp8266-20170108-v1.12.bin
```

> If there are errors - change baud to 115200

> Dont forget - you have your own port and firmware filename!

## Some preparations

[main.py](main.py) requires file `env.py` with next sample data:
```py
WIFI_SSID = "wifi_ssid",
WIFI_PASS = "wifi_password"
```

## IDEs

### Windows

Better use uPyCraft for firmware delivery https://randomnerdtutorials.com/install-upycraft-ide-windows-pc-instructions/

### Linux

You can use scripts and `ampy`/`rshell` python modules (mentioned in [requirements.txt](requirements.txt))

