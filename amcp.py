"""
Copyright (C) 2016 Robert Nagtegaal <masikh@gmail.com>

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.

# Purpose of this program/Class file:

This Class translates python calls to class functions into casparCP API calls.
Its basically an interface between python and the AMCP telnet API.

Usage:

*- Copy this file to  your source tree.

from amcp import AMCP, amcp_session_open, amcp_session_close, stop, clear, mixer_clear
amcp_session = amcp_session_open(config.HOST, config.PORT)

# Setup: channel 1 layer 100 url: youtube parameters: ["-c:v", "nvenc"] Screen-size: 1920x1080, amcp_session: amcp_session
channel = AMCP(1, 100, "https://www.youtube.com/watch?v=v9g0K2RktFg", ["-c:v", "nvenc"], (1920, 1080), acmp_session)

# Set the position and size for this channel
channel.scale("1280x720+43+68")

# Set the volume to 0.6 for this channel
channel.volume(0.6)

# Start playing the channel
channel.play()

# Stop stream
stop(amcp_channels)

# reset all consumers/producers
clear(amcp_channels)

# Clear all transformations
mixer_clear(amcp_channels)

# Close amcp telnet session
amcp_session_close(amcp_session)
"""

import telnetlib
from time import sleep


class AMCP:
    def __init__(self, channel, layer, resource, parameters, screen_size, acmp_session):
        """
        :param channel: int
        :param layer: int
        :param resource: string
        :param parameters: list
        :param acmp_session: telnet-handle
        """
        self.channel = channel
        self.layer = layer
        self.resource = resource
        self.parameters = parameters
        self.amcp_session = acmp_session
        self.screen_size = screen_size

    def compute_geometry(self, geometry):
        """
        Computes the casparCG geometry from a 'X11/Xorg' geometry.

        :param geometry: string e.g. 1280x720+456+87
        :return: tuple (offset-x, offset-y, width, height)
        """
        dimensions = geometry.split('+')[0]
        width = float(dimensions.split('x')[0])
        height = float(dimensions.split('x')[1])
        offset_x = float(geometry.split('+')[1])
        offset_y = float(geometry.split('+')[2])

        return offset_x / self.screen_size[0], \
               offset_y / self.screen_size[1], \
               width / self.screen_size[0], \
               height / self.screen_size[1]

    def restart_casparcg(self):
        """
        Restart CasparCG
        """
        sleep(0.1)
        self.amcp_channel.write("RESTART\r\n")
        amcp_session_close(self.amcp_session)
        print "RESTART"

    def play(self):
        """
        Creates a video stream and starts playing it
        """
        sleep(0.1)
        params = ""
        for param in self.parameters:
            params = params + " " + param

        self.amcp_session.write("PLAY %s-%s %s%s\r\n" % (self.channel, self.layer, self.resource, params))
        print "PLAY %s-%s %s%s" % (self.channel, self.layer, self.resource, params)

    def anchor(self, anchor):
        """
        Creates an ANCHOR
        :param anchor: (float: x, float: y) (X11/Xorg size or casparCG)
        """
        sleep(0.1)
        anchor_x = anchor[0]
        anchor_y = anchor[1]
        if anchor[0] > 1 and anchor[1] > 1:
            anchor_x = anchor[0]/self.resolution[0]
            anchor_y = anchor[1]/self.resolution[1]

        self.amcp_session.write("MIXER %s-%s ANCHOR %s %s\r\n" % (self.channel,
                                                                   self.layer,
                                                                   anchor_x,
                                                                   anchor_y))
        print "MIXER %s-%s ANCHOR %s %s" % (self.channel, self.layer, anchor_x, anchor_y)

    def scale(self, geometry):
        """
        Scales an video stream to the desired size
        :param geometry: WxH+X+Y
        """
        geometry = self.compute_geometry(geometry)
        sleep(0.1)
        self.amcp_session.write("MIXER %s-%s FILL %s %s %s %s\r\n" % (self.channel,
                                                                       self.layer,
                                                                       geometry[0],
                                                                       geometry[1],
                                                                       geometry[2],
                                                                       geometry[3]))
        print "MIXER %s-%s FILL %s %s %s %s" % (self.channel,
                                                  self.layer,
                                                  geometry[0],
                                                  geometry[1],
                                                  geometry[2],
                                                  geometry[3])

    def volume(self, volume):
        """
        Change the volume for this stream
        :param volume: float between 0 and 1
        """
        sleep(0.1)
        self.amcp_session.write("MIXER %s-%s VOLUME %s 25 easeinsine\r\n" % (self.channel, self.layer, volume))
        print "MIXER %s-%s VOLUME %s 25 easeinsine" % (self.channel, self.layer, volume)

    def sink(self, sink):
        """
        Create a sink for this stream
        :param sink: url (e.g. http://farm96.ffserver:8090/feed23.ffm)
        """
        sleep(0.1)
        self.amcp_session.write("ADD %s STREAM %s\r\n" % (self.channel, sink))
        print "ADD %s STREAM %s" % (self.channel, sink)

    def stop(self):
        """
        Stop this stream from playing
        """
        sleep(0.1)
        self.amcp_session.write("STOP %s-%s\r\n" % (self.channel, self.layer))
        print "STOP %s-%s" % (self.channel, self.layer)

    def clear(self):
        """
        Clears this consumer
        """
        sleep(0.1)
        self.amcp_session.write("CLEAR %s-%s\r\n" % (self.channel, self.layer))
        print "CLEAR %s-%s" % (self.channel, self.layer)

    def mixer_clear(self):
        """
        Clears all transformations from this consumer
        """
        sleep(0.1)
        self.amcp_session.write("MIXER %s-%s CLEAR\r\n" % (self.channel, self.layer))
        print "MIXER %s-%s CLEAR" % (self.channel, self.layer)

    def rotate(self, angle):
        """
        Rotates a stream around its anchor point
        """
        sleep(0.1)
        self.amcp_session.write("MIXER %s-%s ROTATION %s\r\n" % (self.channel, self.layer, angle))
        print "MIXER %s-%s ROTATION %s" % (self.channel, self.layer, angle)

    def master_volume(self, volume):
        """
        Sets the master volume
        """
        sleep(0.1)
        self.amcp_session.write("MIXER %s MASTERVOLUME %s\r\n" % (self.channel, volume))
        print "MIXER %s MASTERVOLUME %s" % (self.channel, volume)


def stop(amcp_channel_list):
    """
    Stops all playing layers from channel
    :param amcp_channel_list: list of AMCP class objects (initialized channels)
    """
    for amcp_channel in amcp_channel_list:
        amcp_channel_list["%s" % amcp_channel].stop()


def clear(amcp_channel_list):
    """
    Clears all settings on Channel
    :param amcp_channel_list: List of AMCP Class objects (initialized channels)
    """
    for amcp_channel in amcp_channel_list:
        amcp_channel_list["%s" % amcp_channel].clear()


def mixer_clear(amcp_channel_list):
    """
    Clears all transformations from a AMCP class object (channel)
    :param amcp_channel_list: List of AMCP Class objects (initialized channels)
    """
    for amcp_channel in amcp_channel_list:
        amcp_channel_list["%s" % amcp_channel].mixer_clear()


def amcp_session_open(host, port):
    """
    Open a telnet session to given host on given port
    :param host: string/ip-adress
    :param port: int
    :return: Telnet handle
    """
    return telnetlib.Telnet(host, port)


def amcp_session_close(handle):
    """
    Closes/Terminates the given telnet session
    :param handle: Telnet handle
    """
    return handle.close()
