class CRTHit:
    def __init__(self, id=-1, t0=0, xyz_cm=[], xyz_err_cm=[], total_pe=0, plane=-1, tagger=''):
        self.id = id
        self.t0 = t0
        self.xyz_cm = xyz_cm
        self.xyz_err_cm = xyz_err_cm
        self.total_pe = total_pe
        self.plane = plane
        self.tagger = tagger
        print('Initialized CRTHit class')
