import os
from .track import Track
from .track_point import TrackPoint
from .crthit import CRTHit
from .match_candidate import MatchCandidate
import numpy as np

def write_tracks_to_file(tracks, file_path='.'):
    """
    Write a list of Track instances to a NumPy file.

    Parameters:
        tracks (list): A list of Track instances.
        file_path (str, optional): Output path to store the Numpy file. Default: '.' 
                                   (current working directory).

    Returns:
        None.
    """
    data = {
        'id': [],
        'image_id': [],
        'interaction_id': [],
        'start_x': [],
        'start_y': [],
        'start_z': [],
        'end_x': [],
        'end_y': [],
        'end_z': [],
        'points': [],
        'depositions': []
    }

    # Convert track objects to dictionary of lists
    for track in tracks:
        data['id'].append(track.id)
        data['image_id'].append(track.image_id)
        data['interaction_id'].append(track.interaction_id)
        data['start_x'].append(track.start_x)
        data['start_y'].append(track.start_y)
        data['start_z'].append(track.start_z)
        data['end_x'].append(track.end_x)
        data['end_y'].append(track.end_y)
        data['end_z'].append(track.end_z)
        data['points'].append(track.points)
        data['depositions'].append(track.depositions)
    
    np.save(file_path+'/tracks.npy', data, allow_pickle=True)
    print('Track data saved to', file_path+'/tracks.npy')

def write_crthits_to_file(crthits, file_path='.'):
    """
    Write a list of CRTHit instances to a NumPy file.

    Parameters:
        crthits (list): A list of CRTHit instances.
        file_path (str, optional): Output path to store the Numpy file. Default: '.' 
                                   (current working directory).

    Returns:
        None.
    """
    data = {
        'id': [],
        'total_pe': [],
        't0_sec': [],
        't0_ns': [],
        't1_ns': [],
        'position_x': [],
        'position_y': [],
        'position_z': [],
        'error_x': [],
        'error_y': [],
        'error_z': [],
        'plane': [],
        'tagger': [] 
    }
    
    for crthit in crthits:
        data['id'].append(crthit.id)
        data['total_pe'].append(crthit.total_pe)
        data['t0_sec'].append(crthit.t0_sec)
        data['t0_ns'].append(crthit.t0_ns)
        data['t1_ns'].append(crthit.t1_ns)
        data['position_x'].append(crthit.position_x)
        data['position_y'].append(crthit.position_y)
        data['position_z'].append(crthit.position_z)
        data['error_x'].append(crthit.error_x)
        data['error_y'].append(crthit.error_y)
        data['error_z'].append(crthit.error_z)
        data['plane'].append(crthit.plane)
        data['tagger'].append(crthit.tagger)
    
    np.save(file_path+'/crthits.npy', data, allow_pickle=True)
    print('CRTHit data saved to', file_path+'/crthits.npy')

def write_match_candidates_to_file(match_candidates=[], file_path='.'):
    """
    Write a list of MatchCandidate instances to a NumPy file. If the 
    MatchCandidates list is empty, no file is saved.

    Parameters:
        match_candidates (list): A list of MatchCandidate instances. Default: empty list.
        file_path (str, optional): Output path to store the Numpy file. Default: '.' 
                                   (current working directory).

    Returns:
        None.
    """
    if not match_candidates:
        print('MatchCandidates list is empty. No output file will be saved.')
        return

    data = {
        'trackID': [],
        'crthitID': [],
        'distance_of_closest_approach': []
    }

    for match_candidate in match_candidates:
        data['trackID'].append(match_candidate.track.id)
        data['crthitID'].append(match_candidate.crthit.id)
        data['distance_of_closest_approach'].append(match_candidate.distance_of_closest_approach)

    np.save(file_path+'/match_candidates.npy', data, allow_pickle=True)
    print('MatchCandidate data saved to', file_path+'/match_candidates.npy')

def write_to_file(tracks, crthits, match_candidates=[], file_path='.'):
    """
    Write tracks, CRT hits, and match candidates to separate NumPy files.

    Parameters:
        tracks (list): List of tracks to be written to a file.
        crthits (list): List of CRT hits to be written to a file.
        match_candidates (list, optional): List of match candidates. Default: empty list.
        file_path (str, optional): Path to the directory where the files will be written. 
                                   Default: current directory.

    Returns: None
        This function does not return any value.
    """
    if not os.path.exists(file_path):
        print('WARNING Output file path', file_path, 'does not exist. Defaulting to current directory')
        file_path = ''
    write_tracks_to_file(tracks, file_path)
    write_crthits_to_file(crthits, file_path)
    write_match_candidates_to_file(match_candidates, file_path)



