#from . import track, crthit, match_candidate
from .track import Track
from .track_point import TrackPoint
from .crthit import CRTHit
from .match_candidate import MatchCandidate
import numpy as np
"""
Collection of functions for performing CRT-TPC matching
"""

# TODO How to handle DCA for both start and end points?
# TODO Extrapolate in both directions?
def get_match_candidates(tracks, crthits, approach_distance_threshold=50):
    """
    Loop over CRT hits, calculate DCA for each, determine matches
    Return list of MatchCandidates
    """

    match_candidates = []
    for track in tracks:
        # get_track_endpoints gives a tuple of TrackPoint instances corresponding to 
        # the start and end points
        track_startpoint, track_endpoint = track.get_track_endpoints()
        for crt_hit in crthits:
            print('type crthit:', type(crt_hit))
            dca = calculate_distance_of_closest_approach(track_startpoint, crt_hit)
            if dca > approach_distance_threshold: continue
            match_candidate = MatchCandidate(track, crt_hit)
            match_candidates.append(match_candidate)

    return match_candidates

def calculate_distance_of_closest_approach(track_point, crt_hit, isdata=False): 
    """
    Tyler's C++ method to be ported:
        TVector3 pos (hit.x_pos, hit.y_pos, hit.z_pos);
        TVector3 end = start + direction;
        double denominator = direction.Mag();
        double numerator = (pos - start).Cross(pos - end).Mag();
        return numerator/denominator;
    """
    dca = 0
    crt_hit_time = crt_hit.GetTimeInMicroseconds(isdata)
    # Shift track point by -v*t 
    track_point.shift_position_x(crt_hit_time, isdata)
    # Find some fancy linear algebra to get the DCA
    crt_hit_position = (crt_hit.position_x, crt_hit.position_y, crt_hit.position_z)
    track_endpoint = (track_point.position_x, track_point.position_y, track_point.position_z)
    unit_vec = (track_point.direction_x, track_point.direction_y, track_point.direction_z)
    end = track_endpoint + unit_vec
    #denominator = np.sqrt(unit_vec[0]**2, unit_vec[1]**2, unit_vec[2]**2)
    denominator = np.linalg.norm(unit_vec)
    numerator = np.cross((crt_hit_position - track_endpoint), np.linalg.norm(crt_hit_position - end))
    dca = numerator/denominator
    return dca

def get_best_match(self, match_candidates):
    return min(candidate.distance_of_closest_approach for candidate in match_candidates)






















