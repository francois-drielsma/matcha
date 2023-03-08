from sklearn.decomposition import PCA
from enum import Enum

# TODO list:
#   - What does "rescaled ADC units mean? (from Particle class)

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

    def __repr__(self):
        return f"Track({self.id}, {self.image_id}, {self.interaction_id}, {self.start_x}, {self.start_y}, {self.start_z}, {self.end_x}, {self.start_y}, {self.start_z}, {self.points}, {self.depositions})"

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

    #def get_track_endpoints(self, points, depositions, radius=20):
    def get_track_endpoints(self, radius=20):
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
        points = self.points
        depositions = self.depositions 
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

        print('Candidates len {} and type {}'.format(len(candidates), type(candidates)))
        print('Candidates:\n', candidates)

        return candidates

    def get_track_angles(points, depositions, vertex, radius=20):
        """
        Calculates the approximate angle of the track using a local
        PCA about each endpoint.

        Parameters
        ----------
        points: The 3D space points of the track
        depositions: The charge depositions corresponding to the points.
        vertex: The vertex of the parent interaction.
        radius: Radius used for local primary direction calculation.

        Return
        ------
        The primary components of the track (starting at both ends),
        a bool flagging the first endpoint as having the lowest local
        charge density, and the calculated endpoints.
        """
        pca = PCA(n_components=2)
        endpoints = get_endpoints(points, depositions, radius)
        ret = list()
        centroid = list()
        p0_localQ_lowest = True
        for p in endpoints:
            mask = cdist([p], points)[0] < radius
            if np.sum(mask) > 2:
                centroid.append(np.mean(points[mask], axis=0))
                primary = pca.fit(points[mask]).components_[0]
                ret.append(primary / np.linalg.norm(primary))
            else:
                ret.append(np.array([-9999.0, -9999.0, -9999.0]))
                centroid.append(np.array([0,0,0]))
        return ret, p0_localQ_lowest, endpoints





