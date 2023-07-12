import os
from .track import Track
from .track_point import TrackPoint
from .crthit import CRTHit
from .match_candidate import MatchCandidate
import numpy as np
import pickle

def write_to_file(tracks, crthits, match_candidates=[], file_path='./', file_name='matcha_output.pkl'):
    """
    Write tracks, CRT hits, and match candidates to a single pickle file.

    Parameters:
        tracks (list): List of tracks to be written to a file.
        crthits (list): List of CRT hits to be written to a file.
        match_candidates (list, optional): List of match candidates. Default: empty list.
        file_path (str, optional): Directory to store output file. Default: './' (cwd)
        file_name (str, optional): Name of output file. Default: 'matcha_output.pkl'

    Returns: None
        This function does not return any value.
    """
    if not os.path.exists(file_path):
        print('WARNING Output file path', file_path, 'does not exist. Defaulting to current directory')
        file_path = ''

    file_name = file_path + '/' + file_name
    output_data = {
        'tracks': tracks,
        'crthits': crthits,
        'match_candidates': match_candidates
    }
    with open(file_name, 'wb') as file:
        pickle.dump(output_data, file)

    print('matcha output saved to', file_name)





