import sys
from .track import Track
from .crthit import CRTHit

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
    def __init__(self, track, crthit, distance_of_closest_approach):
        if not isinstance(track, Track):
            raise TypeError('track parameter must be an instance of matcha.Track')
        if not isinstance(crthit, CRTHit):
            raise TypeError('crthit parameter must be an instance of matcha.CRTHit')
        self._track  = track
        self._crthit = crthit
        self._distance_of_closest_approach = distance_of_closest_approach

    def __str__(self):
        return (f"[MATCH_CANDIDATE] Track ID {self.track.id}, CRTHit ID {self.crthit.id}\n\t"
                f"DCA {self.distance_of_closest_approach}")

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

