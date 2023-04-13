#from . import track, crthit, match_candidate
from .track import Track
from .track_point import TrackPoint
from .crthit import CRTHit
from .match_candidate import MatchCandidate
from .writer import write_to_file
from .dca_methods import simple_dca
import numpy as np

"""
Collection of functions for performing CRT-TPC matching
"""

def get_track_crthit_matches(tracks, crthits, 
                             approach_distance_threshold=50, dca_method='simple',
                             pca_radius=10, min_points_in_radius=10, 
                             trigger_timestamp=None, isdata=False, 
                             save_to_file=False, file_path='.'):
    """
    Should return a list of MatchCandidates, one per track. If each Track 
    endpoint has multiple candidates, select only the one with the smallest
    DCA.
    """
    best_matches = []
    for track in tracks:
        match_candidates = get_track_match_candidates(
            track, crthits, approach_distance_threshold, dca_method, 
            pca_radius, min_points_in_radius, trigger_timestamp, isdata
        )
        if not match_candidates: continue
        track_best_match = get_best_match(match_candidates)
        best_matches.append(track_best_match)

    if save_to_file: write_to_file(tracks, crthits, best_matches, file_path) 

    return best_matches

def get_track_match_candidates(track, crthits, 
                               approach_distance_threshold, dca_method, 
                               pca_radius, min_points_in_radius, 
                               trigger_timestamp, isdata):
    """
    Loop over CRT hits, calculate DCA for each, determine matches
    Return list of MatchCandidates
    """

    match_candidates = []
    track_startpoint, track_endpoint = track.get_endpoints(pca_radius, min_points_in_radius)
    for point in (track_startpoint, track_endpoint):
        if point.tpc_region.name not in ['EE', 'EW', 'WE', 'WW']: continue
        for crt_hit in crthits:
            dca = calculate_distance_of_closest_approach(
                point, crt_hit, dca_method, trigger_timestamp, isdata
            )
            if dca > approach_distance_threshold: continue
            match_candidate = MatchCandidate(track, crt_hit, dca)
            match_candidates.append(match_candidate)

    return match_candidates

def get_best_match(match_candidates):
    is_valid_list = all(isinstance(element, MatchCandidate) for element in match_candidates)
    if not is_valid_list:
        raise ValueError("""
            get_best_match method received an invalid list of match_candidates.
            match_candidates must only contain MatchCandidate class instances.
            """)
    min_dca = np.inf
    best_match = None
    for match in match_candidates:
        this_dca = match.distance_of_closest_approach
        if this_dca < min_dca:
            min_dca = this_dca
            best_match = match

    print('[BESTMATCH] returning best match', best_match)
    return best_match

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
    valid_dca_methods = ['simple']
    if dca_method not in valid_dca_methods:
        raise ValueError(f'dca_method must be one of {valid_dca_methods}')

    if dca_method == 'simple':
        dca = simple_dca(track_point, crt_hit, trigger_timestamp, isdata)
        return dca

    else:
        raise ValueError('dca_method parameter must be one of')



        











