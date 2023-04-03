import os
from .track import Track
from .track_point import TrackPoint
from .crthit import CRTHit
from .match_candidate import MatchCandidate
import numpy as np

def write_tracks_to_file(tracks, file_path):
    """
    Write a list of Track instances to a NumPy file 

    Args
    ----
    tracks : list 
        A list of Track instances.
    file_path : str 
        Output path to store the Numpy file. Defaults to current directory if
        file_path does not exist

    Returns:
        None.
    """
    data = {
        'track_id': [],
        'track_image_id': [],
        'track_interaction_id': [],
        'track_start_x': [],
        'track_start_y': [],
        'track_start_z': [],
        'track_end_x': [],
        'track_end_y': [],
        'track_end_z': [],
        'track_points': [],
        'track_depositions': []
    }

    # Convert track objects to dictionary of lists
    for track in tracks:
        data['track_id'].append(track.id)
        data['track_image_id'].append(track.image_id)
        data['track_interaction_id'].append(track.interaction_id)
        data['track_start_x'].append(track.start_x)
        data['track_start_y'].append(track.start_y)
        data['track_start_z'].append(track.start_z)
        data['track_end_x'].append(track.end_x)
        data['track_end_y'].append(track.end_y)
        data['track_end_z'].append(track.end_z)
        data['track_points'].append(track.points)
        data['track_depositions'].append(track.depositions)
    
    np.save(file_path+'/tracks.npy', data, allow_pickle=True)

def write_crthits_to_file(crthits, file_path):
    """
    Write a list of CRTHit instances to a NumPy file

    Args
    ----
    crthits : list 
        A list of CRTHit instances.
    file_path : str 
        Output path to store the NumPy file. Defaults to current directory if
        file_path does not exist

    Returns:
        None.
    """
    data = {
        'crthit_id': [],
        'crthit_total_pe': [],
        'crthit_t0_sec': [],
        'crthit_t0_ns': [],
        'crthit_t1_ns': [],
        'crthit_position_x': [],
        'crthit_position_y': [],
        'crthit_position_z': [],
        'crthit_error_x': [],
        'crthit_error_y': [],
        'crthit_error_z': [],
        'crthit_plane': [],
        'crthit_tagger': [] 
    }
    
    for crthit in crthits:
        data['crthit_id'].append(crthit.id)
        data['crthit_total_pe'].append(crthit.total_pe)
        data['crthit_t0_sec'].append(crthit.t0_sec)
        data['crthit_t0_ns'].append(crthit.t0_ns)
        data['crthit_t1_ns'].append(crthit.t1_ns)
        data['crthit_position_x'].append(crthit.position_x)
        data['crthit_position_y'].append(crthit.position_y)
        data['crthit_position_z'].append(crthit.position_z)
        data['crthit_error_x'].append(crthit.error_x)
        data['crthit_error_y'].append(crthit.error_y)
        data['crthit_error_z'].append(crthit.error_z)
        data['crthit_plane'].append(crthit.plane)
        data['crthit_tagger'].append(crthit.tagger)
    
    np.save(file_path+'/crthits.npy', data, allow_pickle=True)

def write_match_candidates_to_file(match_candidates, file_path):
    """
    Write a list of MatchCandidate instances to a NumPy file. Raises a
    ValueError if the match_candidates list is empty.

    Args
    ----
    match_candidates : list 
        A list of Track instances.
    file_path : str 
        Output path to store the Numpy file. Defaults to current directory if
        file_path does not exist

    Returns:
        None.
    """
    if not match_candidates:
        raise ValueError("Match candidates list is empty")

    data = {
        'track': [],
        'crthit': [],
        'distance_of_closest_approach': []
    }

    for match_candidate in match_candidates:
        data['track'].append(match_candidate.track)
        data['crthit'].append(match_candidate.crthit)
        data['distance_of_closest_approach'].append(match_candidate.distance_of_closest_approach)

    np.save(file_path+'/match_candidates.npy', data, allow_pickle=True)

def write_to_file(tracks, crthits, match_candidates=[], file_path='.'):
    if not os.path.exists(file_path):
        print('WARNING Output file path', file_path, 'does not exist. Defaulting to current directory')
        file_path = ''
    print('Saving matcha class files to', file_path)
    write_tracks_to_file(tracks, file_path)
    write_crthits_to_file(crthits, file_path)
    write_match_candidates_to_file(match_candidates, file_path)
    print('Done saving')



