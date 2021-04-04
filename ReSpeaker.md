# Installation guide for ReSpeaker 4-mic array
- Download latest Picroft
- Install Picroft on SD-card with BalenaEtcher
- Remove and reinsert SD-card 
- Create emtpy file "ssh" and create wpa_supplicant.conf
- Insert SD-card in RPi. 
- Find IP in router and log in via SSH
- Select "No" to guided setup
- Ctrl-C - "mycroft-stop"
- git clone https://github.com/respeaker/seeed-voicecard.git
- cd /home/pi/seeed-voicecard
- ./install.sh 4mic --compat-kernel
- sudo reboot

### Support for LED ring: 

    mycroft-msm install https://github.com/j1nx/respeaker-4mic-hat-skill.git 
    sudo raspi-config
    Go to “Interfacing Options”
    Go to “SPI”
    Enable SPI
    Exit raspi-config
    sudo reboot 


# Raspi 2-mic voicehat from Geekworm
- Select "No" to guided setup
- Ctrl-C - "mycroft-stop"
- git clone https://github.com/respeaker/seeed-voicecard.git
- cd /home/pi/seeed-voicecard
- ./install.sh 2mic --compat-kernel
- sudo reboot
- aplay -l (take note of card # and device #, e.g. 1,0. Change file below accordingly)
- sudo nano /etc/mycroft/mycroft.conf
      
      "play_wav_cmdline": "aplay -Dhw:1,0 %1",
      "play_mp3_cmdline": "mpg123 -a hw:1,0 %1",
