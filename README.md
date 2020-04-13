# minipro

minipro is an open source program for controlling the MiniPRO TL866xx series of chip programmers. The source code is available at https://gitlab.com/DavidGriffith/minipro/

This repository is my notes on how to use it with a [TL866II Plus](http://www.xgecu.com/en/TL866_main.html) universal programmer on openSUSE.

![Image of TL866II Plus](resources/tl866iiplus.png)


## Building

The instructions in the readme on gitlab do not work on openSUSE.

In addition to the regular build tools like `make` and `gcc`, I installed these packages:

* `srecord`
* `rpmdevtools`
* `libusb-1_0-devel`

To build:

1. `$ git clone https://gitlab.com/DavidGriffith/minipro/`
2. Overwrite `minipro.spec` in the cloned repository with this one: [minipro.spec](rpm/minipro.spec)
3. The spec file specifies a certain commit to build. Update the commit hash and date if you want to build a different version.
4. `$ rpmdev-spectool -g -R minipro.spec`
5. `$ rpmbuild -ba minipro.spec`

After it completes you can find the rpm here, ready for installation with zypper: `~/rpmbuild/RPMS/x86_64/minipro-0.1-20200402.bf67708.x86_64.rpm`

Remember to add yourself to the `plugdev` group.


## How to use

Beware of using the programmer connected to an unpowered USB-hub. It draws a lot of power in use, and can potentially damage chips.

Start by finding the correct name of the device for use with the software. You can search using the `-L` parameter like this: 

`$ minipro -L atmega328`

The concrete device could be a `ATMEGA328P@DIP28` in this case. Include this with the `-p` parameter for all future operations.


### Working with EEPROMs

Read the contents of the EEPROM and save it to the file eeprom.bin:

`$ minipro -p "AT28C16@DIP24" -r eeprom.bin`

Write the contents of the file eeprom.bin to the EEPROM:

`$ minipro -p "AT28C16@DIP24" -w eeprom.bin`

Verify that the EEPROM has the same contents as the file eeprom.bin:

`$ minipro -p "AT28C16@DIP24" -m eeprom.bin`


### Working with AVR

AVR microcontrollers may have both flash memory for the program and EEPROM for the data, in addition to configuration parameters in the form of "fuses". All these can be read and written to, unless certain lock bits have been set. Lock bits can stop you from reading the chip, but erasing the chip will also reset the lock bits.

Writing to the chip will by default erase the chip. This can be confusing when you want to write to the different parts of the chip, as writing one of them will blank the other part. This can be avoided by erasing the chip first with the `-E` parameter, and then specifying the `-e` parameter when writing to disable automatic erase.

Erase chip:

`$ minipro -p "ATMEGA328P@DIP28" -E`

Write the contents of the file eeprom.bin to the EEPROM:

 `$ minipro -p "ATMEGA328P@DIP28" -c data -w eeprom.bin -e`

Write the contents of the file program.bin to the flash memory: 

`$ minipro -p "ATMEGA328P@DIP28" -c code -w program.bin -e`

Write the configuration for fuses and lock bits specified in the file fuses.cfg to the chip:

`$ minipro -p "ATMEGA328P@DIP28" -c config -w fuses.cfg -e`

This is the format for fuses.cfg:

```
fuses_lo = 0x62
fuses_hi = 0xd9
fuses_ext = 0xff
lock_byte = 0xff
```

Read the datasheet or use this http://www.engbedded.com/fusecalc/ to understand what this means.

Like the examples from working with EEPROM, you can verify the contents with the `-m` parameter, and read the contents into a file with the `-r` parameter.


### Hardware verifications

You can test for good pin connections with a particular chip inserted in the programmer:

`$ minipro -p AT28C256 -z`

To test that all the pins in the programmer works as intended, you can run a full hardware self check. Be sure to remove any chips from the programmer, otherwise you risk damaging it.

`$ minipro -t`


### Update firmware

You wont find the firmware as a standalone download, so you need to download the Windows software `Xgpro` from the homepage. Unrar the downloaded file to find a Windows executable. I have not found any software on Linux to extract the contents, but the website https://extract.me/ is able to. Download the file `updateII.dat` from the website after extraction.

Update the firmware like this:

`$ minipro -F updateII.dat`
