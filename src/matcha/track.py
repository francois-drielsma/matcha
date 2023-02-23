class Track:
    def __init__(self, id=-1, points_xyz_cm=None, start_xyz_cm=None, end_xyz_cm=None, average_direction=None):
        self._id = id
        self._points_xyz_cm = points_xyz_cm 
        self._start_xyz_cm  = start_xyz_cm
        self._end_xyz_cm    = end_xyz_cm
        self._average_direction = average_direction
        print('Initialized Track class')

    def track_pca(self, track):
        pass

