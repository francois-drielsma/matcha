class CRTHit:
    """
    Class for storing CRT hit information

    Attributes
    ----------
    id : int, required
        Unique identifier for CRTHit
    feb_id : int, optional
        TODO What is this exactly?
        Identifier of the front-end board (FEB). Default value: -1.
    pesmap: dict, optional
        Maps FEB to local channel and PE (I think?). Default value: {}
    t0 : float
        Timestamp of the CRT hit start time in nanoseconds from White Rabbit. Default value: 0
    t1 : float
        Timestamp of the CRT hit with respect to the trigger time. Default value: 0
    total_pe : float
        TODO: Why float and not int?
        Number of photoelectrons (PE) in the CRT hit. Default value: 0
    x_position : float 
        Position in x-direction (cm). Default value: 0
    x_error : float
        Uncertainty in x-direction (cm). Default value: 0
    y_position : float 
        Position in y-direction (cm). Default value: 0
    y_error : float
        Uncertainty in y-direction (cm) Default value: 0
    z_position : float 
        Position in z-direction (cm) Default value: 0
    z_error : float
        Uncertainty in z-direction (cm) Default value: 0
    plane: int, optional
        Integer identifying CRT wall (TODO Find documentation on this)
    tagger: string, optional
        String identifying CRT wall (TODO Find documentation on this)

    Methods
    -------
    TODO INSERT
    """
    def __init__(self, id, feb_id=-1, pesmap={}, total_pe=0, t0=0, t1=0, 
                 x_position=0, x_error=0, y_position=0, y_error=0, z_position=0, z_error=0, 
                 plane=-1, tagger=''):
        """
        Constructor for CRTHit class

        Parameters
        ----------
        TODO Insert (redundant? But also good practice?)
        """
        self._id = id
        self._feb_id = feb_id
        self._pesmap = pesmap
        self._total_pe = total_pe
        self._t0 = t0
        self._t1 = t1
        self._x_position = x_position
        self._x_error    = x_error
        self._y_position = x_position
        self._y_error    = y_error
        self._z_position = x_position
        self._z_error    = z_error
        self._plane  = plane
        self._tagger = tagger

        print('Initialized CRTHit class')

    ### Getters ###
    def get_id(self):
        return self._id
    def get_feb_id(self):
        return self._feb_id
    def get_pesmap(self):
        return self._pesmap
    def get_total_pe(self):
        return self._total_pe
    def get_t0(self):
        return self._t0
    def get_t1(self):
        return self._t1
    def get_x_position(self):
        return self._x_position
    def get_x_error(self):
        return self._x_error
    def get_y_position(self):
        return self._y_position
    def get_y_error(self):
        return self._y_error
    def get_z_position(self):
        return self._z_position
    def get_z_error(self):
        return self._z_error
    def get_plane(self):
        return self._plane
    def get_tagger(self):
        return self._tagger

    ### Setters ###
    def set_id(self, id):
        self._id = id
    def set_feb_id(self, feb_id):
        self._feb_id = fed_ib
    def set_pesmap(self, pesmap):
        self._pesmap = pesmap
    def set_total_pe(self, total_pe):
        self._total_pe = total_pe
    def set_t0(self, t0):
        self._t0 = t0
    def set_t1(self, t1):
        self._t1 = t1
    def set_x_position(self, x_position):
        self._x_position = x_position
    def set_x_error(self, x_error):
        self._x_error = x_error
    def set_y_position(self, y_position):
        self._y_position = y_position
    def set_y_error(self, y_error):
        self._y_error = y_error
    def set_z_position(self, z_position):
        self._z_position = z_position
    def set_z_error(self, z_error):
        self._z_error = z_error
    def set_plane(self, plane):
        self._plane = plane
    def set_tagger(self, tagger):
        self._tagger = tagger

        ################### Available larcv::CRTHit fields: ######################

        #std::vector<uint8_t> _feb_id; ///< FEB address
        #std::map<uint8_t, std::vector<std::pair<int, float>>> _pesmap; ///< Saves signal hit information (FEB, local-channel and PE) .)
        #float _peshit; ///< Total photo-electron (PE) in a crt hit.)

        #int _plane; ///< Name of the CRT wall (in the form of numbers)

	#std::string _tagger; ///< Name of the CRT wall (in the form of strings)
