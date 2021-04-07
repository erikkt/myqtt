# Installation guide for Geekworm
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
- sudo ./install.sh 2mic --compat-kernel
- sudo reboot
- aplay -l (take note of card # and device #, e.g. 1,0. Change file below accordingly)
- sudo nano /etc/mycroft/mycroft.conf
      
      "play_wav_cmdline": "aplay -Dhw:1,0 %1",
      "play_mp3_cmdline": "mpg123 -a hw:1,0 %1",

- LED ring
      mycroft-msm install https://github.com/erikkt/Geekworm-Raspi-Voice-Hat-LED-Ring
      sudo raspi-config
      Go to “Interfacing Options”
      Go to “SPI”
      Enable SPI
      Exit raspi-config
      sudo reboot 
      
- MyQTT
      mycroft-msm install https://github.com/erikkt/myqtt.git

``$ mycroft-config edit user``

```
{
  "max_allowed_core_version": 20.8,  
  "lang": "no-no",
  "tts": {
    "module": "google",
    "google": {
      "lang": "no"
    }
  }
}
```


``$ nano ~/mycroft-core/skills/myqtt.erikkt/vocab/no-no/Allwords.voc `` 

```
cd ~/mycroft-core/skills/fallback-unknown.mycroftai/vocab
cp -r en-us/ no-no/
cd ~/mycroft-core/skills/fallback-unknown.mycroftai/dialog
cp -r en-us/ no-no/
nano no-no/unknown.dialog
```
