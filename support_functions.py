import channels


def get_geometry():
    i = 0
    geometries = {}
    for geometry in channels.geometry:
        geometries['%s' % i] = geometry
        i += 1
    return geometries


def get_display(display_number):
    return channels.displays[display_number]["channels"]
