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
    track_best_matches = []
    for track in tracks:
        track_match_candidates = get_track_match_candidates(
            track, crthits, approach_distance_threshold, 
            dca_method, direction_method,
            pca_radius, min_points_in_radius, 
            trigger_timestamp, isdata
        )
        if not track_match_candidates: continue
        track_best_match = get_track_best_match(track_match_candidates)
        track_best_matches.append(track_best_match)

    # Check for CRT hits that are matched to more than one track
    best_matches = get_crthit_best_matches(track_best_matches)

    if len(best_matches) == 0:
        print('No matches found for this event. Returning default MatchCandidate.')
        default_track = Track(id=-1, image_id=-1, interaction_id=-1,
                              points=[], depositions=[])
        default_crthit = CRTHit(id=-1, t0_sec=-1, t0_ns=-1, t1_ns=-1,
                                position_x=-999, position_y=-999, position_z=-999)
        default_dca = -999
        # Return a list for iterability 
        return [MatchCandidate(default_track, default_crthit, default_dca)]

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
        track_startpoint, track_endpoint = track.get_endpoints(
            pca_radius, min_points_in_radius, direction_method
        )

    for crt_hit in crthits:
        closest_track_point = get_closest_track_point(crt_hit, track_startpoint, track_endpoint)
        if closest_track_point.tpc_region.name not in ['EE', 'EW', 'WE', 'WW']: continue
        dca = calculate_distance_of_closest_approach(
            closest_track_point, crt_hit, dca_method, trigger_timestamp, isdata
        )
        if dca > approach_distance_threshold: continue
        match_candidate = MatchCandidate(track, crt_hit, dca)
        match_candidates.append(match_candidate)

    return match_candidates

def get_closest_track_point(crt_hit, track_startpoint, track_endpoint):
    crt_hit_position = np.array([crt_hit.position_x, crt_hit.position_y, crt_hit.position_z])
    startpoint = np.array([track_startpoint.position_x, track_startpoint.position_y, track_startpoint.position_z])
    endpoint   = np.array([track_endpoint.position_x, track_endpoint.position_y, track_endpoint.position_z])

    distance_to_start = np.linalg.norm(crt_hit_position - startpoint)
    distance_to_end   = np.linalg.norm(crt_hit_position - endpoint)

    if distance_to_start <= distance_to_end:
        return track_startpoint
    else:
        return track_endpoint

def get_track_best_match(match_candidates):
    is_valid_list = all(isinstance(element, MatchCandidate) for element in match_candidates)
    if not is_valid_list:
        raise ValueError("""
            get_track_best_match method received an invalid list of match_candidates.
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

def get_crthit_best_matches(track_best_matches):
    return track_best_matches


        











