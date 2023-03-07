def get_crt_tpc_matches(tracks, crthits, approach_distance_threshold=50):
    # Loop over CRT hits, calculate DCA for each, determine matches
    # Return list of MatchCandidates

    match_candidates = []
    for track in tracks:
        track_startpoint, track_endpoint = track.get_track_endpoints(track.points, track.depositions)
        track_startdir  , track_enddir   = track.get_track_endpoint_angles(track_startpoint, track_endpoint)
        get_track_endpoint_angles(self, track_startpoint, track_endpoint):
        for crthit in crthits:

    return match_candidates

def calculate_distance_of_closest_approach(track, crthit): 
    track_start_x = track.start_x
    track_start_y = track.start_y
    track_start_z = track.start_z

    track_direction_vector = track.get_track_angles()
    # Calculate distance of closest approach.
    # Requires shifting the track by -v*t and extrapolating to the 
    # CRT hit position.
    pass

def get_best_match(self, match_candidates):
    return min(candidate.distance_of_closest_approach for candidate in match_candidates)

if __name__ == "__main__":
    get_crt_tpc_matches(track_list, crthit_list, dca_threshold)
