import sys
from .track import Track
from .crthit import CRTHit

class MatchCandidate:
    """
    Represents a candidate match between a Track object and a CRTHit object.

    Attributes:
        track (Track): The Track instance in the candidate match.
        crthit (CRTHit): The CRTHit instance in the candidate match.
        distance_of_closest_approach (float, optional): The distance of closest 
                                                        approach between the Track 
                                                        and CRTHit objects in cm. 
                                                        Default: 0.

    Methods:
        None
    """
    def __init__(self, track_id, crthit_id, distance_of_closest_approach):
        if not isinstance(track, Track):
            raise TypeError('track parameter must be an instance of matcha.Track')
        if not isinstance(crthit, CRTHit):
            raise TypeError('crthit parameter must be an instance of matcha.CRTHit')
        self._track_id  = track_id
        self._crthit_id = crthit_id
        self._distance_of_closest_approach = distance_of_closest_approach

    def __str__(self):
        return (f"[MATCH_CANDIDATE] Track ID {self.track_id}, CRTHit ID {self.crthit_id}\n\t"
                f"DCA {self.distance_of_closest_approach}")

    @property
    def track_id(self):
        return self._track_id
    @track_id.setter
    def track_id(self, value):
        self._track_id = value

    @property
    def crthit_id(self):
        return self._crthit_id
    @crthit_id.setter
    def crthit_id(self, value):
        self._crthit_id = value

    @property
    def distance_of_closest_approach(self):
        return self._distance_of_closest_approach
    @distance_of_closest_approach.setter
    def distance_of_closest_approach(self, value):
        self._distance_of_closest_approach = value

