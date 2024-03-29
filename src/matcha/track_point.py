import numpy as np
from .crthit import CRTHit

DRIFT_VELOCITY = 0.1571 # MC 
#DRIFT_VELOCITY = 0.157565 # DATA
TPC_X_BOUNDS = [358.49, 210.215, 61.94, -61.94, -210.215, -358.49]
from enum import Enum

class TPCRegion(Enum):
    """
    Class for determining which TPC or region a track endpoint lies in.

    Possible values:
        WestOfWW: Endpoint is west of the west-west TPC (outside TPCs).
        WW: Endpoint is within the west-west TPC.
        WE: Endpoint is within the west-east TPC.
        BetweenTPCs: Endpoint is between the TPCs (outside TPCs).
        EW: Endpoint is within the east-west TPC.
        EE: Endpoint is within the east-east TPC.
        EastOfEE: Endpoint is east of the EE cryostat (outside TPCs).
    """
    WestOfWW    = 0
    WW          = 1
    WE          = 2
    BetweenTPCs = 3
    EW          = 4
    EE          = 5
    EastOfEE    = 6

class TrackPoint:
    """
    Class for storing and managing track point information, particularly
    start and end points and their directions.

    Attributes:
        track_id (int): ID of the corresponding track this point came from.
        position_x (float): x-position of the point in cm.
        position_y (float): y-position of the point in cm.
        position_z (float): z-position of the point in cm.
        direction_x (float): x-direction of the point in cm.
        direction_y (float): y-direction of the point in cm.
        direction_z (float): z-direction of the point in cm.
        tpc_region (Enum): Enum class that gives the TPC drift region,
            e.g., EE, EW, etc. Initialized in the constructor based
            on the TrackPoint position_x.
        drift_direction (int): +1 or -1, depending on which TPC region the
            point lies in. 

    Methods:
        shift_position_x(t0, isdata):
            Shifts the point position_x based on t0 and drift velocity.
    """

    def __init__(self, track_id,
                 position_x, position_y, position_z,
                 direction_x, direction_y, direction_z):
        self._track_id    = track_id
        self._position_x  = position_x
        self._position_y  = position_y
        self._position_z  = position_z
        self._direction_x = direction_x
        self._direction_y = direction_y
        self._direction_z = direction_z
        if self.position_x is not None:
            self._tpc_region  = self._get_tpc_region(self.position_x)
            self._drift_direction = self._get_drift_direction(self.tpc_region)

    def __str__(self):
        return (f"[TrackPoint]: track_id {self.track_id}\n\t"
                f"xyz: ({self.position_x}, {self.position_y}, {self.position_z})\n\t"
                f"dir: ({self.direction_x}, {self.direction_y}, {self.direction_z})\n\t"
                f"TPC region: {self.tpc_region}, drift direction: {self.drift_direction}")

    ### Getters and setters ###
    @property
    def track_id(self):
        return self._track_id
    @track_id.setter
    def track_id(self, value):
        self._track_id = value

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
    def direction_x(self):
        return self._direction_x
    @direction_x.setter
    def direction_x(self, value):
        self._direction_x = value

    @property
    def direction_y(self):
        return self._direction_y
    @direction_y.setter
    def direction_y(self, value):
        self._direction_y = value

    @property
    def direction_z(self):
        return self._direction_z
    @direction_z.setter
    def direction_z(self, value):
        self._direction_z = value

    @property
    def drift_direction(self):
        return self._drift_direction
    @drift_direction.setter
    def drift_direction(self, value):
        self._drift_direction = value

    @property
    def tpc_region(self):
        return self._tpc_region
    @tpc_region.setter
    def tpc_region(self, value):
        self._tpc_region = value

    def is_valid(self):
        """
        Check if TrackPoint position and direction attributes are filled. Used to determine
        whether or not to estimate endpoint positions and directions using PCA.

        Returns:
            bool: True if all positions and directions are filled, False otherwise.
        """
        if self.position_x is None or self.position_y is None or self.position_z is None \
        or self.direction_x is None or self.direction_y is None or self.direction_z is None:
            return False

        return True

    def _get_tpc_region(self, point_x):
        """
        Method to determine the TPC region in which a given point lies based on its x-coordinate.
        The x-coordinate boundaries for each region are defined by the TPC_X_BOUNDS list.

        Parameters:
            point_x (float): x-coordinate of the point in cm.

        Returns:
            TPCRegion: Enum class representing the TPC region in which the point lies.
        """
        point_region = np.digitize(point_x, TPC_X_BOUNDS)
        region = TPCRegion(point_region)
        return region

    def _get_drift_direction(self, tpc_region):
        """
        Method to determine which direction the ionization electrons from a point
        will drift based on which TPC it resides in. In ICARUS, the origin is between
        the two TPCs. The x-values run negative-to-positive east-to-west, so a point
        in a west-drifting TPC will have a positive value, and vice versa. The region
        x-boundaries in cm are assumed to be [-358.49, -210.215, -61.94, 61.94, 210.215, 358.49].

        Parameters:
            tpc_region (Enum): TPC region in which the point lies. Determined from _get_tpc_region.

        Returns:
            int or None: +1 or -1 if the point is inside an active TPC volume, else None.
        """

        region_name = tpc_region.name
        # West-drifting TPCs
        if region_name == 'WW' or region_name == 'EW': 
            return 1
        # East-drifting TPCs
        elif region_name == 'EE' or region_name == 'WE': 
            return -1
        # Outside TPCs
        else:
            return None

    def shift_position_x(self, t0, isdata=False):
        """
        Method to shift the x-position of the track endpoint along the drift direction
        based on t0 and drift velocity.

        Parameters:
            t0 (float): t0 of the track point. If the corresponding track does not cross
                        the cathode, the t0 is assumed to be the CRT hit time for the
                        purpose of shifting the track and determining whether it matches
                        the CRT hit.
            isdata (bool, optional): Flag indicating whether the code is running on data
                                     (True) or simulation (False). It affects the drift 
                                     velocity value used for the shift. Default: False

        Returns:
            float: Shifted x-position of the track endpoint.
        """
        global DRIFT_VELOCITY
        if isdata:
            DRIFT_VELOCITY = 0.157565

        position_x = self.position_x
        drift_direction = self.drift_direction

        shifted_x = position_x + DRIFT_VELOCITY * t0 * drift_direction

        return shifted_x




