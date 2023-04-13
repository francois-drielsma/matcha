from .track import Track
from .track_point import TrackPoint
from .crthit import CRTHit
import numpy as np

def simple_dca(track_point, crt_hit, trigger_timestamp, isdata):

    crt_hit_time = crt_hit.get_time_in_microseconds(trigger_timestamp, isdata)
    shifted_x = track_point.shift_position_x(crt_hit_time, isdata)

    crt_hit_position = np.array([crt_hit.position_x, crt_hit.position_y, crt_hit.position_z])
    track_endpoint = np.array([shifted_x, track_point.position_y, track_point.position_z])
    track_point_direction = np.array([track_point.direction_x, track_point.direction_y, track_point.direction_z])
    point_on_line = np.array(track_endpoint + track_point_direction)

    numerator = np.linalg.norm(np.cross((crt_hit_position - track_endpoint), (crt_hit_position - point_on_line)))
    denominator = np.linalg.norm(track_point_direction)

    dca = numerator/denominator
    return dca
