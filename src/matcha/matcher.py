from track import Track
from crthit import CRTHit
class Match:
    def __init__(self, track:Track(), crthit:CRTHit()):
        self.track  = track
        self.crthit = crthit
        print('Matched Track ID {} with CRTHit ID {}'.format(track.id(), crthit.id()))

class Matchmaker:
    def __init__(self, distance_limit_cm=100, minimum_track_length_cm=50, minimum_pe=50):
        self.distance_limit_cm = distance_limit_cm           # Distance of closest approach threshold in cm
        self.minimum_track_length_cm = minimum_track_length_cm
        self.minimum_pe = minimum_pe                   # Minimum no. photoelectrons for CRT hit
        print('Initialized Matcher class')

    def calculate_dca(self, crthit): 
        # Calculate distance of closest approach.
        # Requires shifting the track by -v*t and extrapolating to the 
        # CRT hit position.
        pass

    def get_track_direction(self, track):
        # What's the input here? How do we load a track into this?
        pass

    def match_crt_hits(self, track):
        # Loop over CRT hits, calculate DCA for each, determine matches
        pass
