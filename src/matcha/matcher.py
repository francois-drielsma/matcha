from track import Track
from crthit import CRTHit

class Match:
    def __init__(self, index, track, crthit):
        self._index  = index
        self._track  = track
        self._crthit = crthit
        print('Matched Track ID {} with CRTHit ID {}'.format(track.id(), crthit.id()))

class Matchmaker:
    def __init__(self, track, crthit, distance_limit=100, minimum_track_length=50, minimum_pe=50):
        self._track = track    
        self._crthit = crthit  
        self._distance_limit = distance_limit              # Distance of closest approach threshold in cm
        self._minimum_track_length = minimum_track_length
        self._minimum_pe = minimum_pe                            # Minimum no. photoelectrons for CRT hit
        print('Initialized Matcher class')

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
    def distance_limit(self):
        return self._distance_limit
    @distance_limit.setter
    def distance_limit(self, value):
        self._distance_limit = value

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

    def calculate_dca(self, track, crthit): 
        # Calculate distance of closest approach.
        # Requires shifting the track by -v*t and extrapolating to the 
        # CRT hit position.
        pass

    def get_track_direction(self, track):
        # What's the input here? How do we load a track into this?
        pass

    def get_crt_tpc_matches(self, tracks, crthits, distance_limit):
        # Loop over CRT hits, calculate DCA for each, determine matches
        pass
