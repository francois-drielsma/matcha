import os
from .track import Track
from .track_point import TrackPoint
from .crthit import CRTHit
from .match_candidate import MatchCandidate
from .writer import write_to_file
from .dca_methods import calculate_distance_of_closest_approach, simple_dca
#import matcha.defaults as defaults
from matcha.loader import load_config
import numpy as np

# Set project root directory two directories up
MATCHA_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEFAULT_CONFIG_PATH = "{:s}/config/default.yaml".format(MATCHA_DIR)
DEFAULT_SAVE_CONFIG_PATH = "{:s}/config/default_file_save_config.yaml".format(MATCHA_DIR)

"""
Main functions for performing CRT-TPC matching
"""

def get_track_crthit_matches(tracks, crthits, config_path=DEFAULT_CONFIG_PATH):
    """
    Top-level match-making function that returns a list of MatchCandidates given
    a list of Track and CRTHit instances.

    Parameters:
        tracks (list): List of matcha.Track instances to be matched.
        crthits (list): List of matcha.CRTHit instances to be matched.
        config_path (str): Path to matcha config file

    Returns:
        list: List of MatchCandidates, at most one per Track, corresponding 
              to the MatchCandidate with the minimum DCA for that Track.
    """

    config = load_config(config_path)

    track_best_matches = []
    for track in tracks:
        track_match_candidates = get_track_match_candidates(track, crthits, config)
        if not track_match_candidates: continue
        track_best_match = get_track_best_match(track_match_candidates)
        track_best_matches.append(track_best_match)

    # TODO This is deprecated but kept here for compatibility. Should
    # be removed at some point.
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

    file_save_config = config['file_save_config']
    save_to_file     = file_save_config['save_to_file']
    save_file_path   = file_save_config['save_file_path']
    save_file_name   = file_save_config['save_file_name']
    write_to_file(tracks, crthits, match_candidates=best_matches, file_path=save_file_path, file_name=save_file_name)

    return best_matches

def get_track_match_candidates(track, crthits, config):
    """
    Given a Track, loop over CRT hits and calculate DCA for each. If DCA falls
    below threshold, create a MatchCandidate instance. 

    Parameters:
        track (Track): matcha.Track instances to be matched.
        crthits (list): List of matcha.CRTHit instances to be matched.
        config (dict): Dictionary from parsing matcha config file

    Returns: 
        list: list of MatchCandidates with DCA below approach_distance_threshold.
    """

    match_candidates = []
    dca_parameters = config['dca_parameters']
    pca_parameters = config['pca_parameters']
    approach_distance_threshold = dca_parameters['threshold']

    # Initialize start and end points with user-provided information.
    track_startpoint = TrackPoint(track_id=track.id, 
        position_x=track.start_x, position_y=track.start_y, position_z=track.start_z,
        direction_x=track.start_dir_x, direction_y=track.start_dir_y, direction_z=track.start_dir_z,
    )
    track_endpoint = TrackPoint(track_id=track.id, 
        position_x=track.end_x, position_y=track.end_y, position_z=track.end_z,
        direction_x=track.end_dir_x, direction_y=track.end_dir_y, direction_z=track.end_dir_z,
    )

    # If start and end point posistions and directions are not provided, estimate them. 
    if not track_startpoint.is_valid() or not track_endpoint.is_valid():
        track_startpoint, track_endpoint = track.get_endpoints(pca_parameters)

    # Loop all CRTHits and determine which are considered match candidates.
    # TODO I think we'll need to factorize the matching method for more than just DCA.
    for crt_hit in crthits:
        closest_track_point = get_closest_track_point(crt_hit, track_startpoint, track_endpoint)
        if closest_track_point.tpc_region.name not in ['EE', 'EW', 'WE', 'WW']: continue
        dca = calculate_distance_of_closest_approach(
            closest_track_point, crt_hit, dca_parameters
        )
        if dca > approach_distance_threshold: continue
        match_candidate = MatchCandidate(track, crt_hit, dca)
        match_candidates.append(match_candidate)

    return match_candidates

def get_closest_track_point(crt_hit, track_startpoint, track_endpoint):
    """
    Function to determine whether the Track start point or end point is closer
    to the CRTHit. Avoids mismatches where a Track end point is matched to a 
    CRTHit that is not compatible with it.

    Parameters:
        crt_hit (CRTHit): CRTHit instance.
        track_startpoint (TrackPoint): Track start point.
        track_endpoint (TrackPoint): Track end point.

    Returns:
        TrackPoint: Which of the two points is closest to the CRTHit.
    """

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
    """
    Determine which MatchCandidate has the minimum DCA for a list of MatchCandidates.

    Parameters:
        match_candidates (list): List of match_candidates.

    Returns:
        MatchCandidate: MatchCandidate instance with the minimum DCA for each Track.
    """
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
    """
    Deprecated, should be removed.
    """
    return track_best_matches

        











