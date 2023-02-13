class Matcher():
    def __init__(self):
        distance_limit_cm = 100           # Distance of closest approach threshold in cm
        minimum_track_length_cm = 50 
        min_pe = 50                       # Minimum no. photoelectrons for CRT hit
        print('Initialized Matcher class')

    def calculate_dca(self, crthit): 
        # Calculate distance of closest approach.
        # Requires shifting the track by -v*t and extrapolating to the 
        # CRT hit position.
        pass

    def get_track_direction(self, track):
        # What's the input here? How do we load a track into this?

    def match_crt_hits(self, track):
        # Loop over CRT hits, calculate DCA for each, determine matches
