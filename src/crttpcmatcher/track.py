def Track():
    def __init__(self, points_xyz_cm=[], start_xyz_cm=[], end_xyz_cm=[], average_direction=[]):
        self.points_xyz_cm = points_xyz_cm 
        self.start_xyz_cm  = start_xyz_cm
        self.end_xyz_cm    = end_xyz_cm
        self.average_direction = average_direction
        print('Initialized Track class')

    def track_pca(self, track):
        pass

