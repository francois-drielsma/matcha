import matcha.defaults as defaults

class CRTHit:
    """
    Class for storing CRT hit information

    Attributes:
        id (int): Unique identifier for CRTHit instance. 
        t0_sec (float): Seconds-only part of the timestamp. 
        t0_ns (float): Timestamp of the CRT hit start time in nanoseconds from White Rabbit. 
        t1_ns (float): Timestamp of the CRT hit with respect to the trigger time. 
        position_x (float): Position in x-direction (cm). 
        position_y (float): Position in y-direction (cm). 
        position_z (float): Position in z-direction (cm). 
        error_x (float, optional): Uncertainty in x-direction (cm). Default: 0
        error_y (float, optional): Uncertainty in y-direction (cm). Default: 0
        error_z (float, optional): Uncertainty in z-direction (cm). Default: 0
        total_pe (float, optional): Number of photoelectrons (PE) in the CRT hit. Default: -1
        plane (int, optional): Integer identifying CRT wall. Default: -1
                               (TODO Find documentation on this)
        tagger (string, optional): String identifying CRT wall. Default: ''
                                   (TODO Find documentation on this)

    Methods:
        get_time_in_microseconds(self, trigger_timestamp=None, isdata=False):
            Get CRTHit time in microseconds from configured t0 values and
            trigger timestamp (only if running on data).

        Raises: 
            ValueError: If isdata=True and trigger_timestamp is not provided.
        
    """
    def __init__(self, id, t0_sec, t0_ns, t1_ns, 
                 position_x, position_y, position_z, 
                 error_x=0, error_y=0, error_z=0, 
                 total_pe=-1, plane=-1, tagger=''):
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
                f"t0_sec: ({self.t0_sec}, t0_ns: {self.t0_ns}, t1_ns: {self.t1_ns})\n\t"
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

    def get_time_in_microseconds(self, 
                                 trigger_timestamp = defaults.DEFAULT_TRIGGER_TIMESTAMP,
                                 isdata            = defaults.DEFAULT_ISDATA):
        """
		This method is a Python port of the GetCRTTime function in the CRTUtils of icaruscode.

        Parameters:
            trigger_timestamp (float, optional): Timestamp of the trigger. Needed for data events but not MC,
                where we assume a timestamp of 0. Default: None
            isdata (bool, optional): Boolean flag for running on data as opposed to MC. Default: False

        Returns:
            float: The "actual" time in microseconds.
        """
        import math
        crt_time = math.inf

        if isdata:
            if not trigger_timestamp:
                raise ValueError('If isdata=True, you need to provide a trigger_timestamp')
            if self.fTSMode == 1:
                crt_time = int(self.t1_ns) * 1e-3 
            else:
                crt_time = float(self.t0_ns - (trigger_timestamp%1_000_000_000))/1e3
                if crt_time < -0.5e6:
                    crt_time += 1e6
                elif crt_time >= 0.5e6:
                    crt_time -= 1e6
        else:
            crt_time = self.t0_ns/1e3

        return crt_time

    

