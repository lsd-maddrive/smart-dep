FROM larsks/esp-open-sdk:latest

WORKDIR /app

RUN git clone --recursive https://github.com/micropython/micropython.git
RUN cd micropython && git submodule update --init
RUN cd micropython && make -C mpy-cross -j `nproc --all`
RUN cd micropython/ports/esp8266 && make -j `nproc --all`
RUN cd micropython/ports/esp8266/build-GENERIC && ls -lh firmware-combined.bin

# firmware-combined.bin




