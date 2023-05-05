from .track import Track
from .track_point import TrackPoint
from .crthit import CRTHit
import numpy as np

def calculate_distance_of_closest_approach(track_point, crt_hit, dca_method, 
                                           trigger_timestamp, isdata): 
    """
    Calculate distance of closest approach between a CRTHit and a line segment
    defined by the track end point and direction.
    
    See https://mathworld.wolfram.com/Point-LineDistance3-Dimensional.html
    for the equation and derivation.

    Parameters
    ----------
    track_point : matcha.TrackPoint
        Track end point from Track.get_endpoints() 
    crt_hit : matcha.CRTHit
        CRT hit to which we calculate distance of closest approach
    isdata : bool
        Whether to run on simulation or data. Deteremines which value of
        drift velocity to use when getting CRT hit time.

    Return
    ------
    float value of distance of closest approach.
    """

    if dca_method == 'simple':
        dca = simple_dca(track_point, crt_hit, trigger_timestamp, isdata)
        return dca
    else:
        raise ValueError('dca_method parameter must be one of')

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

    if np.isnan(dca):
        dca = 1e6

    return dca
