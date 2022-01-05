# ESP32N2K Flasher

ESP32N2kFlasher is a utility app for the [esp32nmea2000 gateway](https://github.com/wellenvogel/esp32-nmea2000)
framework and is designed to make flashing the firmware as simple as possible by:

 * Having pre-built binaries for most operating systems.
 * Hiding all non-essential options for flashing.

The Project is based on
[ESPHome-Flasher](https://github.com/esphome/esphome-flasher/tree/main/esphomeflasher)
project.

The flashing process is done using the [esptool](https://github.com/espressif/esptool)
library by espressif.

## Installation

It doesn't have to be installed, just double-click it and it'll start.
Check the [releases section](../../releases)
for downloads for your platform.

## Installation Using `pip`

If you want to install this application from `pip`:

- Install Python 3.x
- Install [wxPython 4.x](https://wxpython.org/) manually or run `pip3 install wxpython` (see also linux notes below)
- Install this project using `pip3 install esphomeflasher`
- Start the GUI using `esphomeflasher`. Alternatively, you can use the command line interface (
  type `esphomeflasher -h` for info)

## Build it yourself

If you want to build this application yourself you need to:

- Install Python 3.x
- Install [wxPython 4.x](https://wxpython.org/) manually or run `pip3 install wxpython`
- venv handling:
```
python3 -m venv --system-site-packages .
source bin/activate
pip3 install --upgrade pip
pip3 install --no-use-pep517 -e .
```
- Download this project and run `pip3 install -e .` in the project's root.
- Start the GUI using `esp32n2kflashtool`. 


## Linux Notes

Installing wxpython for linux can be a bit challenging (especially when you don't want to install from source).
You can use the following command to install a wxpython suitable with your OS:

```bash
# Go to https://extras.wxpython.org/wxPython4/extras/linux/gtk3/ and select the correct OS type
# here, we assume ubuntu 18.03 bionic
pip3 install -U \
    -f https://extras.wxpython.org/wxPython4/extras/linux/gtk3/ubuntu-18.04 \
    wxPython
```

## License

[MIT](http://opensource.org/licenses/MIT) © Marcel Stör, Otto Winter, Andreas Vogel
