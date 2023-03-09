from . import track, crthit, match_candidate
"""
Collection of functions for performing CRT-TPC matching
"""

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
    track_point.shift_direction_x(crthit.t0)
    # Find some fancy linear algebra to get the DCA
    return dca

# TODO Add extrapolation length and use sin(dca/len) to determine best match
def get_best_match(self, match_candidates):
    return min(candidate.distance_of_closest_approach for candidate in match_candidates)






















