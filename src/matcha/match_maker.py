#from . import track, crthit, match_candidate
from .track import Track
from .track_point import TrackPoint
from .crthit import CRTHit
from .match_candidate import MatchCandidate
import numpy as np
"""
Collection of functions for performing CRT-TPC matching
"""
# TODO Extrapolate in both directions?
# TODO Find a good reference for DCA equation

def get_track_crthit_matches(tracks, crthits, approach_distance_threshold=50):
    """
    Should return a list of MatchCandidates, one per track. If each Track 
    endpoint has multiple candidates, select only the one with the smallest
    DCA.
    """
    match_candidates = []
    best_matches = []
    for track in tracks:
        match_candidates = get_track_match_candidates(track, crthits, approach_distance_threshold)
        if not match_candidates: continue
        track_best_match = get_best_match(match_candidates)
        print('[GETTRACKCRTHITMATCHES] track {} best match: {}'.format(track.id, track_best_match))
        best_matches.append(track_best_match)

    print('[GETTRACKCRTHITMATCH] best_matches', best_matches)
    return best_matches

def get_track_match_candidates(track, crthits, approach_distance_threshold=50):
    """
    Loop over CRT hits, calculate DCA for each, determine matches
    Return list of MatchCandidates
    """

    match_candidates = []
    track_startpoint, track_endpoint = track.get_endpoints()
    for point in (track_startpoint, track_endpoint):
        if point.tpc_region.name not in ['EE', 'EW', 'WE', 'WW']: continue
        #trackpoint_match_candidates = []
        for crt_hit in crthits:
            dca = calculate_distance_of_closest_approach(point, crt_hit)
            if dca > approach_distance_threshold: continue
            print('[GETMATCHES] Got good DCA')
            match_candidate = MatchCandidate(track, crt_hit, dca)
            print('[GETMATCHES] Appending', match_candidate)
            match_candidates.append(match_candidate)

        print('[GETMATCHES] Getting best match for ', [m for m in match_candidates])

        #if not trackpoint_match_candidates: continue
        #this_trackpoint_best_match = get_best_match(trackpoint_match_candidates)
        #best_matches.append(this_trackpoint_best_match)

    return match_candidates

def get_best_match(match_candidates):
    #return min(candidate.distance_of_closest_approach for candidate in match_candidates)
    is_valid_list = all(isinstance(element, MatchCandidate) for element in match_candidates)
    if not is_valid_list:
        raise ValueError("""
            get_best_match method received an invalid list of match_candidates.
            match_candidates must only contain MatchCandidate class instances.
            """)
    print('[BESTMATCH] len match candidates:', len(match_candidates))
    print('[BESTMATCH] match_candidates:', [m for m in match_candidates])
    min_dca = np.inf
    best_match = None
    for match in match_candidates:
        this_dca = match.distance_of_closest_approach
        if this_dca < min_dca:
            min_dca = this_dca
            best_match = match

    print('[BESTMATCH] returning best match', best_match)
    return best_match

def calculate_distance_of_closest_approach(track_point, crt_hit, isdata=False): 
    """
    Tyler's C++ method to be ported:
        TVector3 pos (hit.x_pos, hit.y_pos, hit.z_pos);
        TVector3 end = start + direction;
        double denominator = direction.Mag();
        double numerator = (pos - start).Cross(pos - end).Mag();
        return numerator/denominator;
    """
    print('[CALCDCA] crt_hit:', crt_hit)
    print('[CALCDCA] track_point:', track_point)
    print('[CALCDCA] track_point x:', track_point.position_x)
    crt_hit_time = crt_hit.get_time_in_microseconds(isdata)
    #track_point.shift_position_x(crt_hit_time, isdata)
    shifted_x = track_point.shift_position_x(crt_hit_time, isdata)
    print('[CALCDCA] track_point shifted x:', shifted_x)
    # Do some fancy linear algebra to get the DCA
    crt_hit_position = np.array([crt_hit.position_x, crt_hit.position_y, crt_hit.position_z])
    track_endpoint = np.array([shifted_x, track_point.position_y, track_point.position_z])
    unit_vec = np.array([track_point.direction_x, track_point.direction_y, track_point.direction_z])
    end = np.array(track_endpoint + unit_vec)
    denominator = np.linalg.norm(unit_vec)
    numerator = np.linalg.norm(np.cross((crt_hit_position - track_endpoint), (crt_hit_position - end)))
    dca = numerator/denominator
    print('[CALCDCA] DCA:', dca)
    return dca

        











