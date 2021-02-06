# HAqtt
This skill is for "non-supported" languages, like Norwegian. It sends all sentences that start with trigger words in "allwords.voc" to the MQTT-broker. 
The intent is to let Node-Red handle all logic after message is sent. 

## About
Using Norwegian as example language, set Mycroft language to Norwegian (this is not supported by Mycroft): 

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
Be advised that this will make Mycroft useless for most other stuff than this skill, as NO is not supported by other skills. 

Edit Allwords.voc:

``$ nano ~/mycroft-core/skills/haqtt.erikkt/vocab/no-no/Allwords.voc `` 

If you are using another language than NO, copy the folder no-no to your language.
Enter all words you want to trigger on. For example: 
```
skru # (Turn (on))
slå  # Turn (on))
kjør # (Run)
start # (Start)
stop # (Stop)
aktiver # (Activate)
deaktiver # (Deactivate)
``` 
Whenever you say one of these words, the whole sentence will be sent to the MQTT broker. The rest will be up to Node Red to interpret. 

## Examples
There are some example flows for Node-Red in the examples folder both in Norwegian and English. Be advised the english flow is not tested by me. 
You will of course need to adjust these flows to your setup. You will also need to import the node-red-contrib-string node, if not already present. 
The examples contain flows for turning on and off lights and scenes, a flow for playing latest news on a media_player, a flow for making mycroft speak the temperature inside or outside based on your sensors, and also a flow for adding or removing items from the Home Assistant shopping list, and reporting back which items Mycroft has added/removed. 

## Tags
#remote
#Node Red
#control
#MQTT
#HA
#Homeassistant


## Installation Notes
- Ensure you have a working MQTT Broker. The Home Assistant Add-on Mosquitto works very well.
- SSH and run: mycroft-msm install https://github.com/erikkt/haqtt.git
- Configure home.mycroft.ai
    * Ensure MQTT is enabled.
    * Create a custom base topic name <base_topic>. This can be any MQTT formatted topic.
        * <base_topic> = Mycroft, <base_topic> = Mycroft/Cottage, <base_topic> = abcdef/myhome,   
    * Set IP Address of your broker
    * Set the websocket Port of your broker.
    * Set username/password of your broker
    * The <location_id> is automatically obtained from the Device websettings "Placement".
    * **MQTT paths are case sensitive**

- Configure Home Assistant to be able to send replies to Mycroft
    ```
    # Example configuration.yaml entry
    mycroft:
      host: 0.0.0.0 (Mycroft IP address)

    # Example configuration.yaml entry
    notify:
      - platform: mycroft
        name: mycroft
    ```
Also you need to add the MQTT integration in Home Assistant, so that HA and Node-Red can pick up the commands from the MQTT broker. 

## Requirements
- [paho-mqtt](https://pypi.org/project/paho-mqtt/).
- [Mycroft](https://docs.mycroft.ai/installing.and.running/installation).
- [Websockets](https://pypi.org/project/websockets/)

## Tips
As Norwegian (and many other languages) is not supported by Mycroft, some tweaking is beneficial. To avoid the "not.loaded" error when not hitting the correct commands, do the following: 
```
cd ~/mycroft-core/skills/fallback-unknown.mycroftai/vocab
cp -r en-us/ no-no/
cd ~/mycroft-core/skills/fallback-unknown.mycroftai/dialog
cp -r en-us/ no-no/
nano no-no/unknown.dialog
```
Edit the file and translate it to Norwegian (or your language). 
This is also wise to do on the "volume" skill, so that you can turn up and down the volume on Mycroft using voice commands.

## Problems

If you can't get google TTS to work with Norweigian, do: 

```
mycroft-pip uninstall gTTS
mycroft-pip install gTTS
```
