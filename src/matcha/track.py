import numpy as np
from sklearn.decomposition import PCA
from scipy.spatial.distance import cdist
from .track_point import TrackPoint

# TODO list:
#   - What does "rescaled ADC units mean? (from Particle class)

class Track:
    """
    Class for storing TPC track information. The stored tracks are
    assumed to be muon candidates for CRT-TPC matching.

	Attributes:
        id (int): Identifier for Track instance.
        image_id (int): Identifier for the detector image, or "event". 
        interaction_id (int): Identifier for the parent interaction, or "vertex". 
        points (array-like): List of 3D points comprising the track. 
        depositions (array-like): List of energy deposition values for each point 
                                  in rescaled ADC units.
        start_x (float, optional): x-position of the first track point in cm. Default: None.
        start_y (float, optional): y-position of the first track point in cm. Default: None.
        start_z (float, optional): z-position of the first track point in cm. Default: None.
        start_dir_x (float, optional): x-direction of the first track point. Default: None.
        start_dir_y (float, optional): y-direction of the first track point. Default: None.
        start_dir_z (float, optional): z-direction of the first track point. Default: None.
        end_x (float, optional): x-position of the last track point in cm. Default: None.
        end_y (float, optional): y-position of the last track point in cm. Default: None.
        end_z (float, optional): z-position of the last track point in cm. Default: None.
        end_dir_x (float, optional): x-direction of the first track point. Default: None.
        end_dir_y (float, optional): y-direction of the first track point. Default: None.
        end_dir_z (float, optional): z-direction of the first track point. Default: None.

    Methods:
        get_endpoints(points, depositions, radius=20):
            Calculates the start and end point positions and directions of the 
                track using PCA if (and only if) the user does not provide them. 
            Returns: list of two TrackPoint instances containing the start
            and end point positions and unit vectors.
    """
    def __init__(self, id, image_id, interaction_id, 
                 points, depositions,
                 start_x=None, start_y=None, start_z=None, 
                 start_dir_x=None, start_dir_y=None, start_dir_z=None, 
                 end_x=None, end_y=None, end_z=None,
                 end_dir_x=None, end_dir_y=None, end_dir_z=None):

        self._id = id
        self._image_id       = image_id
        self._interaction_id = interaction_id
        self._points = points
        self._depositions = depositions
        self._start_x = start_x
        self._start_y = start_y
        self._start_z = start_z
        self._start_dir_x = start_dir_x
        self._start_dir_y = start_dir_y
        self._start_dir_z = start_dir_z
        self._end_x = end_x
        self._end_y = end_y
        self._end_z = end_z
        self._end_dir_x = end_dir_x
        self._end_dir_y = end_dir_y
        self._end_dir_z = end_dir_z

    def __str__(self):
        return (f"[Track] ID {self.id}, image_id {self.image_id}, interaction_id {self.interaction_id}\n\t"
                f"start xyz: ({self.start_x}, {self.start_y}, {self.start_z})\n\t"
                f"end xyz: ({self.end_x}, {self.end_y}, {self.end_z})")

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
    def start_dir_x(self):
        return self._start_dir_x
    @start_dir_x.setter
    def start_dir_x(self, value):
        self._start_dir_x = value

    @property
    def start_dir_y(self):
        return self._start_dir_y
    @start_dir_y.setter
    def start_dir_y(self, value):
        self._start_dir_y = value

    @property
    def start_dir_z(self):
        return self._start_dir_z
    @start_dir_z.setter
    def start_dir_z(self, value):
        self._start_dir_z = value

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
    def end_dir_x(self):
        return self._end_dir_x
    @end_dir_x.setter
    def end_dir_x(self, value):
        self._end_dir_x = value

    @property
    def end_dir_y(self):
        return self._end_dir_y
    @end_dir_y.setter
    def end_dir_y(self, value):
        self._end_dir_y = value

    @property
    def end_dir_z(self):
        return self._end_dir_z
    @end_dir_z.setter
    def end_dir_z(self, value):
        self._end_dir_z = value

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

    def get_endpoints(self, pca_params):
        """
        Calculates the start/end points of the track using local charge
        density to guess at the Bragg peak.

		Parameters:
            pca_params (dict): Dictionary of PCA parameters from loaded matcha config file

        Returns:
            list: A list containing two numpy arrays of shape (3,), representing 
                  the start and end points of the track, respectively.
        """
        if not self.points.any():
            raise ValueError('Track points attribute must be filled before calling get_endpoints')
        if not self.depositions.any():
            raise ValueError('Track depositions attribute must be filled before calling get_endpoints')

        radius = pca_params['radius']
        min_points_in_radius = pca_params['min_points_in_radius']
        direction_method = pca_params['direction_method']

        def get_local_density(candidates, points, depositions, radius, min_points_in_radius):
            """
            Calculates the local density around each candidate point based on 
            the neighboring points.

            Parameters:
                candidates (numpy.ndarray): A numpy array of shape (N, 3) 
                                            containing the candidate points.
                points (numpy.ndarray): A numpy array of shape (M, 3) 
                                        containing all the points.
                depositions (numpy.ndarray): A numpy array of shape (M,) 
                                             containing the energy deposition 
                                             values for each point.
                radius (float): Radius (in units of distance) used to define 
                                the neighborhood around each candidate point.
                min_points_in_radius (int): Minimum number of points in the 
                                            neighborhood of a candidate point 
                                            for density calculation.

            Returns:
                numpy.ndarray: A numpy array of shape (N,) containing the local 
                density around each candidate point.
            """
            local_density = []
            for candidate in candidates:
                mask = cdist([candidate], points)[0] < radius
                if np.sum(mask) > min_points_in_radius:
                    local_projection = pca.fit_transform(points[mask])
                    local_candidates = points[mask][np.argmin(local_projection[:, 0])], \
                                       points[mask][np.argmax(local_projection[:, 0])]
                    candidate = local_candidates[np.argmin(cdist([candidate], local_candidates))]
                    mask = cdist([candidate], points)[0] < radius
                local_density.append(np.sum(depositions[mask]))
            return local_density

        points = self.points
        depositions = self.depositions
        pca = PCA(n_components=2)
        projection = pca.fit_transform(points)
        candidates = np.array([points[np.argmin(projection[:, 0])], 
                               points[np.argmax(projection[:, 0])]])
        local_density = get_local_density(candidates, points, depositions, radius, min_points_in_radius)

        # If the second point (assumed to be the end point) has lower charge
        # density, flip the candidates
        if np.argmin(local_density) == 1:
            candidates = np.flip(candidates, axis=0)

        start_point, end_point = candidates[0], candidates[1]
        angles = self.get_track_point_angles(start_point, end_point, points, 
                                             radius, min_points_in_radius, direction_method)

        start_direction, end_direction = angles[0], angles[1]

        # Update parent track attributes
        self.start_x, self.start_y, self.start_z = start_point[0], start_point[1], start_point[2]
        self.end_x, self.end_y, self.end_z = end_point[0], end_point[1], end_point[2]

        # Construct TrackPoint instances to store the position and direction
        track_start_point = TrackPoint(
            track_id=self.id,
            position_x=start_point[0],
            position_y=start_point[1],
            position_z=start_point[2],
            direction_x=start_direction[0],
            direction_y=start_direction[1],
            direction_z=start_direction[2]
        )

        track_end_point = TrackPoint(
            track_id=self.id,
            position_x=end_point[0],
            position_y=end_point[1],
            position_z=end_point[2],
            direction_x=end_direction[0],
            direction_y=end_direction[1],
            direction_z=end_direction[2]
        )

        return track_start_point, track_end_point

    def get_track_point_angles(self, start_point, end_point, points, 
                               radius, min_points_in_radius, direction_method):
        """
		Parameters:
            start_point (numpy.ndarray): A numpy array of shape (3,) representing 
                                         the start point of the track.
            end_point (numpy.ndarray): A numpy array of shape (3,) representing 
                                       the end point of the track.
            points (numpy.ndarray): A numpy array of shape (N, 3) containing the 
                                    track points.
            radius (int): Radius (in cm) used to determine a neighborhood of points 
                          around a candidate start/end point for angle calculation.
            min_points_in_radius (int): Minimum number of points in the neighborhood 
                                        of a candidate start/end point in order for 
                                        angle calculation to be performed.
            direction_method (str): Method for determining the track direction.

        Returns:
            numpy.ndarray: A numpy array of shape (2, 3) containing the angles 
                           of the track points with respect to the start and 
                           end points of the track.
        """
        angles = np.zeros(shape=(2,3))

        if direction_method == 'pca':
            angles = self.get_track_point_angles_from_pca(
                start_point, end_point, points, radius, min_points_in_radius
            )
        else:
            raise ValueError('Invalid direction_method in Track.get_track_point_angles')

        return angles


    def get_track_point_angles_from_pca(self, start_point, end_point, points, 
                                        radius, min_points_in_radius):
        """
        Calculates the angles of the track points with respect to the start 
        and end point directions using PCA.

        Parameters:
            start_point (numpy.ndarray): A numpy array of shape (3,) 
                                         representing the start point of the track.
            end_point (numpy.ndarray): A numpy array of shape (3,) 
                                       representing the end point of the track.
            points (numpy.ndarray): A numpy array of shape (N, 3) containing the 
                                    track points.
            radius (int): Radius (in cm) used to determine a neighborhood of points 
                          around a candidate start/end point for PCA calculation.
            min_points_in_radius (int): Minimum number of points in the neighborhood 
                                        of a candidate start/end point in order for 
                                        PCA calculation to be performed.

        Returns:
            numpy.ndarray: A numpy array of shape (2, 3) where each row corresponds 
                           to the start and end point directions, respectively.
        """
        pca = PCA(n_components=2)
        directions = []
        for point in (start_point, end_point):
            mask = cdist([point], points)[0] < radius
            if np.sum(mask) < min_points_in_radius:
                directions.append(np.array([-9999.0, -9999.0, -9999.0]))
                continue
            # The first component of the PCA will be the direction
            # of greatest variance, i.e., a direction vector
            primary = pca.fit(points[mask]).components_[0]
            directions.append(primary / np.linalg.norm(primary))
        return directions

