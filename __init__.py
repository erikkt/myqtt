from os.path import dirname
from adapt.intent import IntentBuilder
from mycroft.skills.core import MycroftSkill, intent_handler, intent_file_handler
from mycroft.util.log import getLogger
from mycroft.util.log import LOG
from mycroft.audio import wait_while_speaking
from mycroft.skills.context import adds_context, removes_context
from mycroft.api import DeviceApi

# import sys
from websocket import create_connection

# from time import sleep
import uuid
import string
import random
import json
import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish
import re

__author__ = 'erikkt'

# Logger: used for debug lines, like "LOGGER.debug(xyz)". These
# statements will show up in the command line when running Mycroft.
LOGGER = getLogger(__name__)

# clear any previously connected mqtt clients on first load
try:
    mqttc
    LOG.info('Client exist')
    mqttc.loop_stop()
    mqttc.disconnect()
    LOG.info('Stopped old client loop')
except NameError:
    mqttc = mqtt.Client()
    LOG.info('Client created')


# The logic of each skill is contained within its own class, which inherits
# base methods from the MycroftSkill class with the syntax you can see below:
# "class ____Skill(MycroftSkill)"
class MqttSkill(MycroftSkill):

    # The constructor of the skill, which calls Mycroft Skill's constructor
    def __init__(self):
        super(MqttSkill, self).__init__(name="HAqtt")
        # Initialize settings values
        self._is_setup = False
        self.notifier_bool = True
        self.targetDevice = ''  # This is the targed device_id obtained through mycroft dialog
        self.base_topic = ''
        self.device_name = ''
        self.MQTT_Enabled = ''
        self.broker_address = ''
        self.broker_port = ''
        self.broker_uname = ''
        self.broker_pass = ''
        self.location_id = ''
        self.response_location = ''

    def on_connect(self, mqttc, obj, flags, rc):
        LOG.info("Connection Verified")
        LOG.info("This device location is: " + DeviceApi().get()["description"])

    def on_disconnect(self, mqttc, obj, flags, rc):
        self._is_setup = False
        LOG.info("MQTT has Disconnected")


    def initialize(self):
        self.load_data_files(dirname(__file__))
        #  Check and then monitor for credential changes
        self.settings_change_callback = self.on_websettings_changed
        self.on_websettings_changed()
        self.add_event('recognizer_loop:utterance', self.handle_utterances)  # should be "utterances"
        self.add_event('speak', self.handle_speak)  # should be "utterance"
        mqttc.on_connect = self.on_connect
        mqttc.on_disconnect = self.on_disconnect
        if self._is_setup:
            self.mqtt_init()

    def clean_base_topic(self, basetopic):
        if basetopic[-1] == "/":
            basetopic = basetopic[0:-1]
        if basetopic[0] == "/":
            basetopic = basetopic[1:]
        return basetopic

    def on_websettings_changed(self):  # called when updating mycroft home page
        self._is_setup = False
        self.MQTT_Enabled = self.settings.get("MQTT_Enabled", False)  # used to enable / disable mqtt
        self.broker_address = self.settings.get("broker_address", "127.0.0.1")
        raw_base_topic = self.settings.get("base_topic", "Mycroft")
        self.base_topic = self.clean_base_topic(raw_base_topic)
        self.device_name = self.settings.get("device_name", "")
        self.broker_port = self.settings.get("broker_port", 1883)
        self.broker_uname = self.settings.get("broker_uname", "")
        self.broker_pass = self.settings.get("broker_pass", "")
        
        this_location_id = str(DeviceApi().get()["description"])
        self.location_id = this_location_id.lower()
        LOG.info("This device location is: " + str(self.location_id))
        try:
            mqttc
            LOG.info('Client exist')
            mqttc.loop_stop()
            mqttc.disconnect()
            LOG.info('Stopped old client loop')
        except NameError:
            mqttc = mqtt.Client()
            LOG.info('Client re-created')
        LOG.info("Websettings Changed! " + self.broker_address + ", " + str(self.broker_port))
        self.mqtt_init()
        self._is_setup = True

    def mqtt_init(self):  # initializes the MQTT configuration and subscribes to its own topic
        if self.MQTT_Enabled:
            LOG.info('MQTT Is Enabled')
            try:
                LOG.info("Connecting to host: " + self.broker_address + ", on port: " + str(self.broker_port))
                if self.broker_uname and self.broker_pass:
                    LOG.info("Using MQTT Authentication")
                    mqttc.username_pw_set(username=self.broker_uname, password=self.broker_pass)
                mqttc.connect_async(self.broker_address, self.broker_port, 60)
                mqttc.loop_start()
                LOG.info("MQTT Loop Started Successfully")
                
            except Exception as e:
                LOG.error('Error: {0}'.format(e))


    # utterance event used for notifications ***This is what the user requests***
    def handle_utterances(self, message):

        voice_payload = str(message.data.get('utterances')[0])
        self.voice_load = voice_payload

    # mycroft speaking event used for notificatons ***This is what mycroft says***
    def handle_speak(self, message):
        voice_payload = message.data.get('utterance')
        if self.notifier_bool:
            try:
                if len(self.response_location) == 0:
                    self.response_location = ''
                else:
                    reply_payload = {
                        "source": str(self.location_id),
                        "message": voice_payload
                    }

            except Exception as e:
                LOG.error(e)
                self.on_websettings_changed()

    def send_MQTT(self, my_topic, my_message):  # Sends MQTT Message
        if self.MQTT_Enabled and self._is_setup:
            LOG.info("MQTT: " + my_topic + ", " + json.dumps(my_message))            
            LOG.info("address: " + self.broker_address + ", Port: " + str(self.broker_port))
            publish.single(my_topic, json.dumps(my_message), hostname=self.broker_address, retain=False, auth={ 'username': self.broker_uname, 'password': self.broker_pass })
        else:
            LOG.info("MQTT has been disabled in the websettings at https://home.mycroft.ai")



    # First step in the dialog is to receive the initial request to "send a message/command"
    # Todo Add .optionally("LocationRegex") to make the intent spoken language agnostic
    @intent_handler(IntentBuilder("SendMessageIntent").require("Allwords")
                    .build())

    def handle_send_message_intent(self, message):
        mqtt_path = self.base_topic + "/" + self.location_id 
        if self.notifier_bool:
            try:
                # LOG.info(voice_payload)
                self.send_MQTT(mqtt_path, self.voice_load)
            except Exception as e:
                LOG.error(e)
                self.on_websettings_changed()

#        self.speak_dialog('sending.message', expect_response=False)


    def stop(self):
        pass


# The "create_skill()" method is used to create an instance of the skill.
# Note that it's outside the class itself.
def create_skill():
    return MqttSkill()
