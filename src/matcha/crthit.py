class CRTHit:
    """
    Class for storing CRT hit information

    Attributes
    ----------
    id : int, required
        Unique identifier for CRTHit
    total_pe : float
        Number of photoelectrons (PE) in the CRT hit. Default: 0
    t0_sec : float
        Seconds-only part of the timestamp. Default: 0
    t0_ns : float
        Timestamp of the CRT hit start time in nanoseconds from White Rabbit. Default: 0
    t1_ns : float
        Timestamp of the CRT hit with respect to the trigger time. Default: 0
    position_x : float 
        Position in x-direction (cm). Default: 0
    error_x : float
        Uncertainty in x-direction (cm). Default: 0
    position_y : float 
        Position in y-direction (cm). Default: 0
    error_y : float
        Uncertainty in y-direction (cm) Default: 0
    position_z : float 
        Position in z-direction (cm) Default: 0
    error_z : float
        Uncertainty in z-direction (cm) Default: 0
    plane: int, optional
        Integer identifying CRT wall (TODO Find documentation on this)
    tagger: string, optional
        String identifying CRT wall (TODO Find documentation on this)

    Methods
    -------
    TODO INSERT
    """
    def __init__(self, id, total_pe=0, t0_sec=0, t0_ns=0, t1_ns=0, 
                 position_x=0, position_y=0, 
                 position_z=0, error_x=0, error_y=0, error_z=0, 
                 plane=-1, tagger=''):
        self._id = id
        self._total_pe = total_pe
        self._t0_sec = t0_sec
        self._t0_ns  = t0_ns
        self._t1_ns = t1_ns
        self._position_x = position_x
        self._position_y = position_y
        self._position_z = position_z
        self._error_x = error_x
        self._error_y = error_y
        self._error_z = error_z
        self._plane  = plane
        self._tagger = tagger

    def __str__(self):
        return (f"[CRTHit] ID {self.id}, total_pe {self.total_pe}\n\t"
                f"xyz: ({self.position_x}, {self.position_y}, {self.position_z})\n\t"
                f"err: ({self.error_x}, {self.error_y}, {self.error_z})\n\t"
                f"plane self.plane{self.plane}, tagger {self.tagger}")

    ### Getters and setters ###
    @property
    def id(self):
        return self._id
    @id.setter
    def id(self, value):
        self._id = value

    @property
    def total_pe(self):
        return self._total_pe
    @total_pe.setter
    def total_pe(self, value):
        self._total_pe = value

    @property 
    def t0_sec(self):
        return self._t0_sec
    @t0_sec.setter
    def t0_sec(self, value):
        self._t0_sec = value

    @property 
    def t0_ns(self):
        return self._t0_ns
    @t0_ns.setter
    def t0_ns(self, value):
        self._t0_ns = value

    @property
    def t1_ns(self):
        return self._t1_ns
    @t1_ns.setter
    def t1_ns(self, value):
        self._t1_ns = value

    @property
    def position_x(self):
        return self._position_x
    @position_x.setter
    def position_x(self, value):
        self._position_x = value

    @property
    def position_y(self):
        return self._position_y
    @position_y.setter
    def position_y(self, value):
        self._position_y = value

    @property
    def position_z(self):
        return self._position_z
    @position_z.setter
    def position_z(self, value):
        self._position_z = value

    @property
    def error_x(self):
        return self._error_x
    @error_x.setter
    def error_x(self, value):
        self._error_x = value

    @property
    def error_y(self):
        return self._error_y
    @error_y.setter
    def error_y(self, value):
        self._error_y = value

    @property
    def error_z(self):
        return self._error_z
    @error_z.setter
    def error_z(self, value):
        self._error_z = value

    @property
    def plane(self):
        return self._plane
    @plane.setter
    def plane(self, value):
        self._plane = value

    @property
    def tagger(self):
        return self._tagger
    @tagger.setter
    def tagger(self, value):
        self._tagger = value

    def get_time_in_microseconds(self, trigger_timestamp=None, isdata=False):
        """
        CRTHit class method to retreive the "actual" time in microseconds.

        This function is essentially a python port of the GetCRTTime function 
        in the CRTUtils of icaruscode.

        Parameters
        ----------
        trigger_timestamp : float, optional
            Timestamp of the trigger. Needed for data events but not MC, where 
            we assume a timestamp of 0. Default: None
        isdata : bool, optional
            Boolean flag for running on data as opposed to MC. Default: False
        """
        import math
        crtTime = math.inf

        if isdata:
            if self.fTSMode == 1:
                crtTime = int(self.t1_ns) * 1e-3 
            else:
                crtTime = float(self.t0_ns - (trigger_timestamp%1_000_000_000))/1e3
                if crtTime < -0.5e6:
                    crtTime += 1e6
                elif crtTime >= 0.5e6:
                    crtTime -= 1e6
        else:
            crtTime = self.t0_ns/1e3

        return crtTime

    

