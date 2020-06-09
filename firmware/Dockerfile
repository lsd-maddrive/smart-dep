# Fedora
FROM larsks/esp-open-sdk:latest

WORKDIR /app
RUN yum install -y patch

RUN git clone --recursive https://github.com/micropython/micropython.git
RUN cd micropython && git clone --recursive https://github.com/micropython/micropython-lib.git

RUN cd micropython && make -C mpy-cross -j `nproc --all`

# Update modules
COPY _main.py micropython/ports/esp8266/modules/
COPY upy-patches/ .

RUN patch -d micropython/ports/esp8266/boards/GENERIC < esp8266_manifest.patch
RUN patch -d micropython/ports/esp8266/modules < esp8266_inisetup.patch
RUN patch -d micropython/ports/esp8266/ < esp8266_main.patch

# Build firmware
RUN cd micropython/ports/esp8266 && make -j `nproc --all` && cp build-GENERIC/firmware-combined.bin /app/firmware.bin

# Install firmware
COPY _install_firmware.sh .

CMD ./_install_firmware.sh


