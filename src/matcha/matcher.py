from track import Track
from crthit import CRTHit

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
    closest_approach_distance : float, optional
        The distance of closest approach between the Track and CRTHit objects
        in cm. Default: 0.

    Methods
    -------
    None
    """
    def __init__(self, index, track, crthit, closest_approach_distance=0):
        self._index  = index
        self._track  = track
        self._crthit = crthit
        self._closest_approach_distance = closest_approach_distance

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
    def closest_approach_distance(self):
        return self._closest_approach_distance
    @closest_approach_distance.setter
    def closest_approach_distance(self, value):
        self._closest_approach_distance = value

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
        possible match. Default: 10 cm.
    minimum_track_length : float, optional
        The minimum length of Track object to be considered for matching.
        Default: 50 cm.
    minimum_pe : float, optional
        The minimum number of photoelectrons (PE) of Track object to be
        considered for matching. Default: 50 PE.

    Methods
    -------
    calculate_closest_approach_distance(track, crthit): 
        Calculates distance of closest approach between a back-projected
        track and the CRT hit coordinates.
        Return: float
    get_crt_tpc_matches(tracks, crthits, approach_distance_threshold):
        Determines candidate matches between the Track and CRTHit objects based
        on the matching criteria specified by the class attributes. 
        Return: list of candidate matches.
    """
    def __init__(self, track, crthit, approach_distance_threshold=10, minimum_track_length=50, minimum_pe=50):
        self._track = track    
        self._crthit = crthit  
        self._approach_distance_threshold = approach_distance_threshold 
        self._minimum_track_length = minimum_track_length
        self._minimum_pe = minimum_pe                            # Minimum no. photoelectrons for CRT hit

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

    def calculate_closest_approach_distance(self, track, crthit): 
        # Calculate distance of closest approach.
        # Requires shifting the track by -v*t and extrapolating to the 
        # CRT hit position.
        pass

    def get_crt_tpc_matches(self, tracks, crthits, approach_distance_threshold):
        # Loop over CRT hits, calculate DCA for each, determine matches
        # Return list of MatchCandidates
        pass

    def get_best_match():
        # Determine which match is best based on minimum distance of closest 
        # approach
        pass


