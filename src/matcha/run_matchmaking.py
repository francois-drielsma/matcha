def get_crt_tpc_matches(tracks, crthits, approach_distance_threshold=50):
    # Loop over CRT hits, calculate DCA for each, determine matches
    # Return list of MatchCandidates

    match_candidates = []
    for track in tracks:
        # get_track_endpoints gives a tuple of TrackPoint instances corresponding to 
        # the start and end points
        track_startpoint, track_endpoint = track.get_track_endpoints(track.points, track.depositions)
        for crthit in crthits:
            dca = calculate_distance_of_closest_approach(track_startpoint, crthit)
            if dca > approach_distance_threshold: continue
            match_candidate = MatchCandidate(track, crthit)
            match_candidates.append(match_candidate)

    return match_candidates

def calculate_distance_of_closest_approach(track_point, crthit): 
    dca = 0
    # Shift track point by -v*t 
    track_point.shift_direction_x(crthit.t0)
    # Find some fancy linear algebra to get the DCA
    return dca

def get_best_match(self, match_candidates):
    return min(candidate.distance_of_closest_approach for candidate in match_candidates)

if __name__ == "__main__":
    match_candidates = get_crt_tpc_matches(track_list, crthit_list, dca_threshold)
    best_match = get_best_match(match_candidates)
