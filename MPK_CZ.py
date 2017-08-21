# --------------------------------------------------- #
'''

MPK25 control script for ableton Live, written by Christopher Zaworski
Based of my script for the MPD26


special credits to Alzy (Seppe?), his original script can be found at
https://forum.ableton.com/viewtopic.php?f=4&t=157266
Also thank you to
http://livecontrol.q3f.org/ableton-liveapi/articles/introduction-to-the-framework-classes/
and especially http://remotescripts.blogspot.ca/

Also credits to Julien Bayle for providing much of Ableton's API in an awesome
resource available at:
http://julienbayle.net/AbletonLiveRemoteScripts_Docs/_Framework/


'''


#.....................................
#---------------------------------------------------- #
from __future__ import with_statement

import sys
import Live
from _Framework.ControlSurface import ControlSurface
from _Framework.InputControlElement import *
from _Framework.ButtonElement import ButtonElement
from _Framework.ButtonMatrixElement import ButtonMatrixElement
from ConfigurableButtonElement import ConfigurableButtonElement
from _Framework.SessionComponent import SessionComponent
from _Framework.TransportComponent import TransportComponent
from _Framework.DeviceComponent import DeviceComponent
from _Framework.EncoderElement import EncoderElement
from _Framework.SessionZoomingComponent import SessionZoomingComponent

from _Framework.ChannelStripComponent import ChannelStripComponent
from _APC.DetailViewCntrlComponent import DetailViewCntrlComponent

from DeviceNavComponent import DeviceNavComponent


from _Framework.MixerComponent import MixerComponent # Class encompassing several channel strips to form a mixer
from _Framework.SliderElement import SliderElement # Class representing a slider on the controller
from consts import *
mixer = None


class MPK_CZ(ControlSurface):
    def __init__(self, c_instance):
        ControlSurface.__init__(self, c_instance)
        self._device_selection_follows_track_selection = True
        with self.component_guard():
            self._suppress_send_midi = True
            self._suppress_session_highlight = True
            self._control_is_with_automap = False
            is_momentary = True
            self._suggested_input_port = 'Akai MPK26'
            self._suggested_output_port = 'Akai MPK26'
            self.log("BEFORE mixer")
            self._setup_mixer_control()
            self._setup_device_control()


            # self.clipcontrol(8)

            self.log("AFTER MIXER")
            """SESSION ViEW"""
            global session
            session = SessionComponent(GRIDSIZE[0],GRIDSIZE[1])
            session.name = 'Session_Control'
            matrix = ButtonMatrixElement()
            matrix.name = 'Button_Matrix'
            up_button = ButtonElement(True, MIDI_CC_TYPE, CHANNEL, UP_BUTTON)
            down_button = ButtonElement(True, MIDI_CC_TYPE, CHANNEL, DOWN_BUTTON)
            left_button = ButtonElement(True, MIDI_CC_TYPE, CHANNEL, LEFT_BUTTON)
            right_button = ButtonElement(True, MIDI_CC_TYPE, CHANNEL, RIGHT_BUTTON)

            # session.set_scene_bank_buttons(down_button, up_button)
            # session.set_track_bank_buttons(right_button, left_button)

            session_zoom = SessionZoomingComponent(session)
            session_zoom.set_nav_buttons(up_button,down_button,left_button,right_button)

            session_stop_buttons = []
            self.log("SETTING UP GRID")
            for row in xrange(GRIDSIZE[1]):
                button_row = []
                self.log("CZ ROW")
                self.log(str(row))
                scene = session.scene(row)
                scene.name = 'Scene_' + str(row)
                scene.set_launch_button(ButtonElement(True, MIDI_NOTE_TYPE, CHANNEL, SCENE_BUTTONS[row]))
                scene.set_triggered_value(2)

                for column in xrange(GRIDSIZE[0]):
                    self.log("CZ COLUMN")
                    self.log(str(column))
                    button = ConfigurableButtonElement(True, MIDI_NOTE_TYPE, CHANNEL, LAUNCH_BUTTONS[row][column])
                    button.name = str(column) + '_Clip_' + str(row) + '_Button'
                    button_row.append(button)
                    clip_slot = scene.clip_slot(column)
                    clip_slot.name = str(column) + '_Clip_Slot_' + str(row)
                    clip_slot.set_launch_button(button)

                matrix.add_row(tuple(button_row))

            for column in xrange(GRIDSIZE[0]):
                session_stop_buttons.append((ButtonElement(True, MIDI_NOTE_TYPE, CHANNEL, TRACK_STOPS[column])))

            self._suppress_session_highlight = False
            self._suppress_send_midi = False
            self.set_highlighting_session_component(session)
            session.set_stop_track_clip_buttons(tuple(session_stop_buttons))
            session.set_mixer(mixer)


    def log(self, message):
        sys.stderr.write("LOG: " + message.encode("utf-8"))


    def _setup_mixer_control(self):
        num_tracks = GRIDSIZE[1] # Here we define the mixer width in tracks (a mixer has only one dimension)
        global mixer # We want to instantiate the global mixer as a MixerComponent object (it was a global "None" type up until now...)
        mixer = MixerComponent(num_tracks) #(num_tracks, num_returns, with_eqs, with_filters)
        mixer.set_track_offset(0) #Sets start point for mixer strip (offset from left)
        """set up the mixer buttons"""
        self.song().view.selected_track = mixer.channel_strip(0)._track
        # mixer.set_master_volume_control(SliderElement(MIDI_CC_TYPE, CHANNEL, MASTER_VOLUME))
        # master = mixer.master_strip()
        # master.set_volume_control(SliderElement(MIDI_CC_TYPE, CHANNEL, MASTER_VOLUME))

        # mixer.set_prehear_volume_control(SliderElement(MIDI_CC_TYPE, CHANNEL, PREHEAR))
        for index in xrange(GRIDSIZE[0]):
            mixer.channel_strip(index).set_volume_control(SliderElement(MIDI_CC_TYPE, CHANNEL, MIX_FADERS[index]))
            mixer.channel_strip(index).set_pan_control(SliderElement(MIDI_CC_TYPE, CHANNEL, PAN_CONTROLS[index]))
            mixer.channel_strip(index).set_arm_button(ButtonElement(True, MIDI_NOTE_TYPE, CHANNEL, ARM_BUTTONS[index])) #sets the record arm button
            mixer.channel_strip(index).set_solo_button(ButtonElement(True, MIDI_NOTE_TYPE, CHANNEL, SOLO_BUTTONS[index]))
            mixer.channel_strip(index).set_mute_button(ButtonElement(True, MIDI_NOTE_TYPE, CHANNEL, MUTE_BUTTONS[index]))
            mixer.channel_strip(index).set_select_button(ButtonElement(True, MIDI_NOTE_TYPE, CHANNEL, TRACK_SELECTS[index]))




        """TRANSPORT CONTROLS"""
        stop_button = ButtonElement(False, MIDI_CC_TYPE, 0, STOP_BUTTON)
        play_button = ButtonElement(False, MIDI_CC_TYPE, 0, PLAY_BUTTON)
        record_button = ButtonElement(False,MIDI_CC_TYPE,0,RECORD_BUTTON)
        transport = TransportComponent()
        transport.set_stop_button(stop_button)
        transport.set_play_button(play_button)
        transport.set_overdub_button(record_button)
        transport.set_overdub_button(record_button)
        transport.set_seek_buttons(ButtonElement(False,MIDI_CC_TYPE,0,SEEK_LEFT),ButtonElement(False,MIDI_CC_TYPE,0,SEEK_RIGHT))

    def _setup_device_control(self):
        is_momentary = True
        self._device = DeviceComponent()
        self._channelstrip = ChannelStripComponent()
        self._device.name = 'Device_Component'

        device_param_controls = []
        for index in range(8):
            device_param_controls.append(SliderElement(MIDI_CC_TYPE, CHANNEL, MACRO_CONTROLS[index]))
        self._device.set_parameter_controls(device_param_controls)
        # self._device.set_on_off_button(ButtonElement(True, MIDI_CC_TYPE, CHANNEL, DEVICE_ON))
        # self._device.set_lock_button(ButtonElement(True, MIDI_CC_TYPE, CHANNEL, DEVICE_LOCK))
        # self._device.set_bank_down_value(ButtonElement(True, MIDI_CC_TYPE, CHANNEL, DEVICE_LOCK))
        # self._device.set_bank_up_value(ButtonElement(True, MIDI_CC_TYPE, CHANNEL, DEVICE_ON))
        up_bank_button = ButtonElement(True, MIDI_CC_TYPE, CHANNEL, DEVICE_ON)
        down_bank_button = ButtonElement(True, MIDI_CC_TYPE, CHANNEL, DEVICE_LOCK)
        # self._device.set_bank_buttons(down_bank_button, up_bank_button)
        self.set_device_component(self._device)
        self._device_nav = DeviceNavComponent()
        self._device_nav.set_device_nav_buttons(ButtonElement(True, MIDI_CC_TYPE, CHANNEL, PREVIOUS_DEVICE),ButtonElement(True, MIDI_CC_TYPE, CHANNEL, NEXT_DEVICE))
        self._device.set_bank_prev_button(down_bank_button)
        self._device.set_bank_next_button(up_bank_button)




    def _set_session_highlight(self, track_offset, scene_offset, width, height, include_return_tracks):
        if not self._suppress_session_highlight:
            ControlSurface._set_session_highlight(self, track_offset, scene_offset, width, height, include_return_tracks)

    def disconnect(self):
        """clean things up on disconnect"""
        ControlSurface.disconnect(self)
        return None
