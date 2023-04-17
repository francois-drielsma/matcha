#from . import track, crthit, match_candidate
from .track import Track
from .track_point import TrackPoint
from .crthit import CRTHit
from .match_candidate import MatchCandidate
from .writer import write_to_file
from .dca_methods import calculate_distance_of_closest_approach, simple_dca
import numpy as np

"""
Collection of functions for performing CRT-TPC matching
"""

def get_track_crthit_matches(tracks, crthits, 
                             approach_distance_threshold=50, dca_method='simple',
                             direction_method='pca', pca_radius=10, min_points_in_radius=10, 
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
            track, crthits, approach_distance_threshold, 
            dca_method, direction_method,
            pca_radius, min_points_in_radius, 
            trigger_timestamp, isdata
        )
        if not match_candidates: continue
        track_best_match = get_best_match(match_candidates)
        best_matches.append(track_best_match)

    if save_to_file: write_to_file(tracks, crthits, best_matches, file_path) 

    return best_matches

def get_track_match_candidates(track, crthits, 
                               approach_distance_threshold, 
                               dca_method, direction_method, 
                               pca_radius, min_points_in_radius, 
                               trigger_timestamp, isdata):
    """
    Loop over CRT hits, calculate DCA for each, determine matches
    Return list of MatchCandidates
    """

    match_candidates = []

    track_startpoint = TrackPoint(track_id=track.id, 
        position_x=track.start_x, position_y=track.start_y, position_z=track.start_z,
        direction_x=track.start_dir_x, direction_y=track.start_dir_y, direction_z=track.start_dir_z,
    )
    track_endpoint = TrackPoint(track_id=track.id, 
        position_x=track.end_x, position_y=track.end_y, position_z=track.end_z,
        direction_x=track.end_dir_x, direction_y=track.end_dir_y, direction_z=track.end_dir_z,
    )

    if not track_startpoint.is_valid() or not track_endpoint.is_valid():
        print('Estimating track start/end points and directions using PCA...')
        track_startpoint, track_endpoint = track.get_endpoints(
            pca_radius, min_points_in_radius, direction_method
        )
        print('Done')
    else:
        print('Using user-provided track start/end points and directions')

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

    return best_match




        











