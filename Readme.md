# KidsBox - a music box for kids 

KidsBox is a simple music player for kids where they have all their favorit music and audio books in one place.

### Features:
* display to select album or audio book
* HW buttons for VOLUME (+,-) and ALBUMS, BACK, PLAY and FORWARD
* last postion is stored in the album
* samba folder to add, delete or update albums/audio books (WLAN access needed)
* software runs without hardware and can be tested and changed on desktop system 

## BOM
* Raspberry Pi Zero wh
* Adafruit I2S 3W Class D Amplifier
* Waveshare 3.5inch RPi LCD
* Visaton VS-FRS8 or Visaton FRS 7 Speaker
* Larcele Push Buttons

## Screenshots and Demo

### Fully assembled
![KidsBox Wood](https://github.com/dernerv/KidsBox/blob/master/Wood.JPG "Kids Box Wood")
![KidsBox inside](https://github.com/dernerv/KidsBox/blob/master/in.JPG "Inside KidsBox")
[Demo Video](https://www.youtube.com/embed/c5WPCfisl5I)

### Software
![startup view](https://github.com/dernerv/KidsBox/blob/master/intro.png "startup view")
![navigation view](https://github.com/dernerv/KidsBox/blob/master/alben.png "navigation view")
![navigation2 view](https://github.com/dernerv/KidsBox/blob/master/alben2.png "navigation2 view")
![Play view](https://github.com/dernerv/KidsBox/blob/master/play.png "play view")

### CAD
![Box](https://github.com/dernerv/KidsBox/blob/master/hardware/KidsBox.png "Box")
![Box groundplate](https://github.com/dernerv/KidsBox/blob/master/hardware/groundplate.png "Box groundplate")


## Configuration

### samba server

sudo apt-get install samba samba-common smbclient

sudo smbpasswd -a pi

sudo cp KidsBox/smb.conf  /etc/samba/smb.conf
