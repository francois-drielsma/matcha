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
    x_position : float 
        Position in x-direction (cm). Default: 0
    x_error : float
        Uncertainty in x-direction (cm). Default: 0
    y_position : float 
        Position in y-direction (cm). Default: 0
    y_error : float
        Uncertainty in y-direction (cm) Default: 0
    z_position : float 
        Position in z-direction (cm) Default: 0
    z_error : float
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
                 x_position=0, y_position=0, 
                 z_position=0, x_error=0, y_error=0, z_error=0, 
                 plane=-1, tagger=''):
        self._id = id
        self._total_pe = total_pe
        self._t0_sec = t0_sec
        self._t0_ns  = t0_ns
        self._t1_ns = t1_ns
        self._x_position = x_position
        self._y_position = y_position
        self._z_position = z_position
        self._x_error = x_error
        self._y_error = y_error
        self._z_error = z_error
        self._plane  = plane
        self._tagger = tagger

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
    def x_position(self):
        return self._x_position
    @x_position.setter
    def x_position(self, value):
        self._x_position = value

    @property
    def y_position(self):
        return self._y_position
    @y_position.setter
    def y_position(self, value):
        self._y_position = value

    @property
    def z_position(self):
        return self._z_position
    @z_position.setter
    def z_position(self, value):
        self._z_position = value

    @property
    def x_error(self):
        return self._x_error
    @x_error.setter
    def x_error(self, value):
        self._x_error = value

    @property
    def y_error(self):
        return self._y_error
    @y_error.setter
    def y_error(self, value):
        self._y_error = value

    @property
    def z_error(self):
        return self._z_error
    @z_error.setter
    def z_error(self, value):
        self._z_error = value

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

    def GetTimeInMicroseconds(self, trigger_timestamp=None, isdata=False):
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
                crtTime = int(self.ts1_ns) * 1e-3 
            else:
                crtTime = float(self.ts0_ns - (trigger_timestamp%1_000_000_000))/1e3
                if crtTime < -0.5e6:
                    crtTime += 1e6
                elif crtTime >= 0.5e6:
                    crtTime -= 1e6
        else:
            crtTime = self.ts0_ns/1e3

        return crtTime

    

