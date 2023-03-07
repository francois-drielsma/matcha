from sklearn.decomposition import PCA
from enum import Enum

# TODO list:
#   - Insert actual drift velocity
#   - What does "rescaled ADC units mean? (from Particle class)

V_DRIFT = None
TPC_X_BOUNDS = [-358.49, -210.215, -61.94, 61.94, 210.215, 358.49]

class TPCRegion(Enum):
    """
    Class for determining which TPC or region a track endpoint lies in.
    """
    WestOfWW    = 0
    InsideWW    = 1
    InsideWE    = 2
    BetweenTPCs = 3
    InsideEW    = 4
    InsideEE    = 5
    EastOfEE    = 6

class Track:
    """
    Class for storing TPC track information. The stored tracks are
    assumed to be muon candidates for CRT-TPC matching.

    Attributes
    ----------
    id : int, required
        Identifier for Track instance
    image_id : int
        Identifier for the detector image, or "event." Default: -1
    interaction_id : int
        Identifier for the parent interaction, or "vertex." Default: -1
    start_x : float
        x-position of the first track point in cm. Default: 0
    end_x : float
        x-position of the last track point in cm. Default: 0
    start_y : float
        y-position of the first track point in cm. Default: 0
    end_y : float
        y-position of the last track point in cm. Default: 0
    start_z : float
        z-position of the first track point in cm. Default: 0
    end_z : float
        z-position of the last track point in cm. Default: 0
    points : array-like (N, 3)
        List of 3D points comprising the track. Default: []
    depositions : array-like (N, 1)
        List of energy deposition values for each point in rescaled ADC units. Default: []
    Methods
    -------
    get_track_endpoints(points, depositions, radius=20):
        Calculates the start/end points of the track using local charge
        density to guess at the Bragg peak.
        Return: list of two numpy arrays of shape (3,) containing the start
        and end point, respectively.
    get_endpoint_angles():
        Calculate approximate angles of the track end points using PCA.
        Return: ordered pair of (startpoint_angle, endpoint_angle)
    """
    def __init__(self, id, image_id=-1, interaction_id=-1, 
                 start_x=0, start_y=0, start_z=0, 
                 end_x=0,   end_y=0,   end_z=0,
                 points=[], depositions=[]):

        self._id = id
        self._image_id       = image_id
        self._interaction_id = interaction_id
        self._start_x = start_x
        self._start_y = start_y
        self._start_z = start_z
        self._end_x   = end_x
        self._end_y   = end_y
        self._end_z   = end_z
        self._points = points
        self._depositions = depositions

    ### Getters and setters ###
    @property
    def id(self):
        return self._id
    @id.setter
    def id(self, value):
        self._id = value

    @property
    def image_id(self):
        return self._image_id
    @image_id.setter
    def image_id(self, value):
        self._image_id = value

    @property
    def interaction_id(self):
        return self._interaction_id
    @interaction_id.setter
    def interaction_id(self, value):
        self._interaction_id = value

    @property
    def start_x(self):
        return self._start_x
    @start_x.setter
    def start_x(self, value):
        self._start_x = value

    @property
    def start_y(self):
        return self._start_y
    @start_y.setter
    def start_y(self, value):
        self._start_y = value

    @property
    def start_z(self):
        return self._start_z
    @start_z.setter
    def start_z(self, value):
        self._start_z = value

    @property
    def end_x(self):
        return self._end_x
    @end_x.setter
    def end_x(self, value):
        self._end_x = value

    @property
    def end_y(self):
        return self._end_y
    @end_y.setter
    def end_y(self, value):
        self._end_y = value

    @property
    def end_z(self):
        return self._end_z
    @end_z.setter
    def end_z(self, value):
        self._end_z = value

    @property
    def points(self):
        return self._points
    @points.setter
    def points(self, value):
        self._points = value

    @property 
    def depositions(self):
        return self._depositions
    @depositions.setter
    def depositions(self, value):
        self._depositions = value

    def get_track_endpoints(self, points, depositions, radius=20):
        """
        Calculates the start/end points of the track using local charge
        density to guess at the Bragg peak.

        Parameters
        ----------
        points : array_like, shape (n_points, 3)
            The 3D space points of the track.
        depositions : array_like, shape (n_points,)
            The charge depositions corresponding to the points.
        radius : int, optional
            Radius (in voxels) for local charge density calculation.

        Return
        ------
        A list with two numpy arrays of shape (3,) containing the start
        and end point (respectively).
        """
        def get_local_density(candidates, points, depositions, radius):
            local_density = []
            for candidate in candidates:
                mask = cdist([candidate], points) < radius
                if np.sum(mask) > 10:
                    local_projection = pca.fit_transform(points[mask])
                    local_candidates = points[mask][np.argmin(local_projection[:, 0])], \
                                        points[mask][np.argmax(local_projection[:, 0])]
                    candidate = local_candidates[np.argmin(cdist([candidate], local_candidates))]
                    mask = cdist([candidate], points) < radius
                local_density.append(np.sum(depositions[mask]))
            return local_density

        pca = PCA(n_components=2)
        projection = pca.fit_transform(points)
        candidates = [points[np.argmin(projection[:, 0])], points[np.argmax(projection[:, 0])]]
        local_density = get_local_density(candidates, points, depositions, radius)
        if np.argmin(local_density) == 1:
            local_density.reverse()
            candidates.reverse()

        return candidates





