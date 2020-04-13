# minipro

minipro is an open source program for controlling the MiniPRO TL866xx series of chip programmers. The source code is available at https://gitlab.com/DavidGriffith/minipro/

This repository is my notes on how to use it with a [TL866II Plus](http://www.xgecu.com/en/TL866_main.html) universal programmer on openSUSE.

![](resources/tl866iiplus.png)


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


## Functions

TODO firmware, read, write, verify, self check, pin check, fuse, not usb-hub

https://extract.me/
updateII.dat
avr, eeprom
