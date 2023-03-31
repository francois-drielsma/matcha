from .track import Track
from .track_point import TrackPoint
from .crthit import CRTHit
from .match_candidate import MatchCandidate
from .writer import write_to_file
import numpy as np

def write_tracks_to_file(tracks):
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
    
    np.save('tracks.npy', data)

def write_crthits_to_file(tracks):
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

    # TODO Make ChatGPT do this lul
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
    
    np.save('tracks.npy', data)
