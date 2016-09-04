from support_functions import get_geometry, get_display
from amcp import AMCP, amcp_session_open, amcp_session_close, stop, clear, mixer_clear
from channels import channels
import config


"""
Quick demostration of the AMCP class for interaction with a casparCG server

(c) Robert Nagtegaal 2016
"""


def start(geometries, display, acmp_session):
    """
    Start a multiview by placing each channel on a canvas with given offset and scalar
    Output the volume of one channel (6 - hardcoded!)

    :param geometries: dict of geometries
    :param display: list of channels
    :param acmp_session: handle for telnet session
    :return: dict of ACMP class objects (e.g. channel functions)
    """
    i = 0
    acmp_channels = {}
    for display_channel in display:
        # Get geometry and url for channel
        geometry = geometries["%s" % i]
        url = channels[display_channel]['channel']
        layer = str(i)
        if i < 10:
            layer = "0%s" % str(i)
        # Setup and play channel
        channel = AMCP(1, "2%s" % layer, url, ["-c:v", "mpegts"], config.RESOLUTION, acmp_session)
        channel.scale(geometry)
        channel.volume(0)
        if i == 6:
            channel.volume(0.2)
        channel.play()

        # Register channel in list
        acmp_channels['%s' % i] = channel

        # Next channel
        i += 1
    return acmp_channels


if __name__ == "__main__":
    # Open amcp telnet session
    amcp_session = amcp_session_open(config.HOST, config.PORT)

    # Get geometies and channels for Multiview
    geometries = get_geometry()
    display = get_display("0")

    # Start Multiview
    amcp_channels = start(geometries, display, amcp_session)

    # reset all consumers/producers
    stop(amcp_channels)
    clear(amcp_channels)
    mixer_clear(amcp_channels)

    # Close amcp telnet session
    amcp_session_close(amcp_session)
