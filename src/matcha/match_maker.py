from . import track, crthit, match_candidate
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
        for crthit in crthits:
            dca = calculate_distance_of_closest_approach(track_startpoint, crthit)
            if dca > approach_distance_threshold: continue
            match_candidate = MatchCandidate(track, crthit)
            match_candidates.append(match_candidate)

    return match_candidates

def calculate_distance_of_closest_approach(track_point, crthit): 
    """
    Tyler's C++ method to be ported:
        TVector3 pos (hit.x_pos, hit.y_pos, hit.z_pos);
        TVector3 end = start + direction;
        double denominator = direction.Mag();
        double numerator = (pos - start).Cross(pos - end).Mag();
        return numerator/denominator;
    """
    dca = 0
    crthit_time = crthit.GetTimeInMicroseconds()
    # Shift track point by -v*t 
    track_point.shift_direction_x(crthit_time)
    # Find some fancy linear algebra to get the DCA
    crthit_position = (crthit.position_x, crthit.position_y, crthit.position_z)
    track_endpoint = (track_point.position_x, track_point.position_y, track_point.position_z)
    unit_vec = (track_point.direction_x, track_point.direction_y, track_point.direction_z)
    end = track_endpoint + unit_vec
    #denominator = np.sqrt(unit_vec[0]**2, unit_vec[1]**2, unit_vec[2]**2)
    denominator = np.linalg.norm(unit_vec)
    numerator = np.cross((crthit_position - track_endpoint), np.linalg.norm(crthit_position - end))
    dca = numerator/denominator
    return dca

def get_best_match(self, match_candidates):
    return min(candidate.distance_of_closest_approach for candidate in match_candidates)






















