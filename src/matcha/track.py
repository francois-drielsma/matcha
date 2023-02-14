class Track:
    def __init__(self, id=-1, points_xyz_cm=None, start_xyz_cm=None, end_xyz_cm=None, average_direction=None):
        self.id = id
        self.points_xyz_cm = points_xyz_cm 
        self.start_xyz_cm  = start_xyz_cm
        self.end_xyz_cm    = end_xyz_cm
        self.average_direction = average_direction
        print('Initialized Track class')

    def track_pca(self, track):
        pass

