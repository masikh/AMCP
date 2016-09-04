# License
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

# Developer usage:

### *- Copy AMCP.py file to  your source tree.

### from amcp import AMCP, amcp_session_open, amcp_session_close, stop, clear, mixer_clear
### amcp_session = amcp_session_open(config.HOST, config.PORT)

\# Setup: channel 1 layer 100 url: youtube parameters: ["-c:v", "nvenc"] Screen-size: 1920x1080, amcp_session: amcp_session
### channel = AMCP(1, 100, "https://www.youtube.com/watch?v=v9g0K2RktFg", ["-c:v", "nvenc"], (1920, 1080), acmp_session)

\# Set the position and size for this channel (scaling is relative to given resolution (e.g. 1920, 1080)
### channel.scale("1280x720+43+68")

\# Set the volume to 0.6 for this channel
### channel.volume(0.6)

\# Start playing the channel
### channel.play()

\# Stop stream
### stop(amcp_channels)

\# reset all consumers/producers
### clear(amcp_channels)

\# Clear all transformations
### mixer_clear(amcp_channels)

\# Close amcp telnet session
### amcp_session_close(amcp_session)
