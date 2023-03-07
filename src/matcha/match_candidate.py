import sys
from .track import Track
from .crthit import CRTHit

MAX_FLOAT = sys.float_info.max

class MatchCandidate:
    """
    Represents a candidate match between a Track object and a CRTHit object.

    Attributes
    ----------
    index : int
        The index of the candidate match.
    track : matcha.Track
        The Track object in the candidate match.
    crthit : matcha.CRTHit
        The CRTHit object in the candidate match.
    distance_of_closest_approach : float, optional
        The distance of closest approach between the Track and CRTHit objects
        in cm. Default: 0.

    Methods
    -------
    None
    """
    def __init__(self, index, track, crthit, distance_of_closest_approach=MAX_FLOAT):
        if not isinstance(track, matcha.Track):
            raise TypeError('track parameter must be an instance of matcha.Track')
        if not isinstance(crthit, matcha.CRTHit):
            raise TypeError('crthit parameter must be an instance of matcha.CRTHit')
        self._index  = index
        self._track  = track
        self._crthit = crthit
        self._distance_of_closest_approach = distance_of_closest_approach

    @property
    def track(self):
        return self._track
    @track.setter
    def track(self, value):
        self._track = value

    @property
    def crthit(self):
        return self._crthit
    @crthit.setter
    def crthit(self, value):
        self._crthit = value

    @property
    def distance_of_closest_approach(self):
        return self._distance_of_closest_approach
    @distance_of_closest_approach.setter
    def distance_of_closest_approach(self, value):
        self._distance_of_closest_approach = value

class MatchMaker:
    """
    Class for matching CRT hits and TPC tracks.

    This class provides methods for determining candidate matches between a
    TPC track and a CRT hit object based on various matching criteria.

    Attributes
    ----------
    track : matcha.Track
        The Track object to be tested for matching.
    crthit : matcha.CRTHit
        The CRTHit object to be tested for matching.
    approach_distance_threshold : float, optional
        The minimum distance-of-closest-approach between the back-projected
        Track and the CRTHit coordinates for the two to be considered a
        possible match. Default: 50 cm.
    minimum_track_length : float, optional
        The minimum length of Track object to be considered for matching.
        Default: 50 cm.
    minimum_pe : float, optional
        The minimum number of photoelectrons (PE) of Track object to be
        considered for matching. Default: 50 PE.

    Methods
    -------
    calculate_distance_of_closest_approach(track, crthit): 
        Calculates distance of closest approach between a back-projected
        track and the CRT hit coordinates.
        Return: float
    get_crt_tpc_matches(tracks, crthits, approach_distance_threshold):
        Determines candidate matches between the Track and CRTHit objects based
        on the matching criteria specified by the class attributes. 
        Return: list of candidate matches.
    """
    def __init__(self, track, crthit, approach_distance_threshold=50, minimum_track_length=50, minimum_pe=50):
        self._track = track    
        self._crthit = crthit  
        self._approach_distance_threshold = approach_distance_threshold 
        self._minimum_track_length = minimum_track_length
        self._minimum_pe = minimum_pe 

    @property
    def track(self):
        return self._track
    @track.setter
    def track(self, value):
        self._track = value

    @property
    def crthit(self):
        return self._crthit
    @crthit.setter
    def crthit(self, value):
        self._crthit = value

    @property
    def approach_distance_threshold(self):
        return self._approach_distance_threshold
    @approach_distance_threshold.setter
    def approach_distance_threshold(self, value):
        self._approach_distance_threshold = value

    @property
    def minimum_track_length(self):
        return self._minimum_track_length
    @minimum_track_length.setter
    def minimum_track_length(self, value):
        self._minimum_track_length = value

    @property
    def minimum_pe(self):
        return self._minimum_pe
    @minimum_pe.setter
    def minimum_pe(self, value):
        self._minimum_pe = value

    @classmethod
    def calculate_distance_of_closest_approach(cls, track, crthit): 
        track_start_x = track.start_x
        track_start_y = track.start_y
        track_start_z = track.start_z

        track_direction_vector = track.get_track_angles()
        # Calculate distance of closest approach.
        # Requires shifting the track by -v*t and extrapolating to the 
        # CRT hit position.
        pass

    def get_crt_tpc_matches(self, tracks, crthits, approach_distance_threshold):
        # Loop over CRT hits, calculate DCA for each, determine matches
        # Return list of MatchCandidates
        match_candidates = []
        return match_candidates

    def get_best_match(self, match_candidates):
        # Determine which match is best based on minimum distance of closest 
        # approach
        return min(candidate.distance_of_closest_approach for candidate in match_candidates)


