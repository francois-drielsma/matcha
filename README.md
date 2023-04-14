# matcha
This package contains data structures and algorithms for matching tracks and cosmic ray tagger (CRT) objects in liquid argon time projection chamber (LArTPC) data.

# Matching Algorithm Overview

The matching algorithm contained in this repository is a Python port of [code already developed in LArSoft for the ICARUS experiment](https://github.com/SBNSoftware/icaruscode/blob/develop/icaruscode/CRT/CRTUtils/CRTT0MatchAlg.h). While the implentation here may differ slightly, the credit for algorithm development goes to the original authors of the LArSoft code. 

The purpose of the matching algorithm is to identify tracks in the LArTPC which are cosmogenic in origin, as opposed to neutrino-induced. Tracks identified as cosmic can then be rejected as background, thereby enhancing the signal "purity" of the neutrino sample. To this end, modern LArTPCs generally use cosmic ray tagger (CRT) planes surrounding the detector to identify particles that originated outside the active detector volume. This matching algorithm seeks to determine if tracks in the detector are likely cosmics by checking if the track timing and geometry are consistent with a CRT "hit."

For each track in a LArTPC image (or "event"), the track start and end points, as well as their direction unit vectors, are estimated using [principal component analysis](https://en.wikipedia.org/wiki/Principal_component_analysis) (PCA). Each point and unit vector then defines a line in 3D space. For each CRT hit, we then calculate the distance of closest approach (DCA) between the extrapolated track line and the CRT hit. If the DCA falls below some configurable threshold, the pair is considered a match candidate. The "best" match is then determined to be the pair with the minimum DCA. 

Due to the inherent ambiguity in the drift coordinate in a LArTPC (typically denoted as the `x` coordinate), each track end point must first be shifted according to the measured (or at least estimated) ionization electron drift velocity and the track entry time, or `t0`. Since our goal is to determine potential matches between tracks and CRT hits, the track `t0` is assumed to be the CRT hit time. The shifted `x` coordinate is therefore calculated as
```
x_shifted = drift_direction * drift_velocity * t0
```

where `drift_direction` is either `+1` or `-1`, depending on the coordinate system and the region of the LArTPC in which the track point is located.

# Installation

Though intentionally lightweight, `matcha` does include some external dependencies which should be installed in a virtual environment to avoid conflicts with other packages. If you have access to anaconda, create a virtual environment as follows:

```
conda create -n my_environment
conda activate my_environment
```

Or, using Python's built-in `venv` module:

```
cd /path/to/virtual/environments 
python3 -m venv my_environment
source /path/to/virtual/environments/my_environment/bin/activate
```

Once your environment is setup, `matcha` can be installed simply by using `pip`:
```
cd /path/to/matcha
python3 -m pip install .
```

## Optional `nbstripout` Install

[nbstripout](https://github.com/kynan/nbstripout) is a handy Python package for "stripping out" cell output and metadata from Jupyter notebooks. While not necessary for running the Jupyter code in matcha, this tool makes committing and pushing Jupyter notebooks to Github much easier. If you plan to modify and submit pull requests for any Jupyter notebooks contained in this repository, please first install and run `nbstripout` to avoid superfluous conflicts. See the [contributing.md](https://github.com/andrewmogan/matcha/blob/main/contributing.md) file for more information. 

To install `nbstripout` from within matcha, simply run

```
python3 -m pip install matcha[nbstripout]
```

# Usage
The matching algorithm is called from `match_maker.py`. Before running the matching, however, you'll need to fill the `Track` and `CRTHit` classes. 

## `CRTHit` Class
The available attributes in the `matcha.CRTHit` class is based on the implementation in [larcv](https://github.com/DeepLearnPhysics/larcv2/blob/develop/larcv/core/DataFormat/CRTHit.h), which is in turn based on the implementation in [sbnobj](https://github.com/SBNSoftware/sbnobj/blob/develop/sbnobj/Common/CRT/CRTHit.hh). The _required_ attributes are
- `id`: unique instance identifier
- `t0_sec`: seconds part of the hit t0. For Monte Carlo (MC), this will be 0. 
- `t0_ns`: nanoseconds part of the hit t0, relative to `t0_sec`. 
- `t1_ns`: timestamp of the CRT hit relative to the trigger timestamp. Only needed for data, not MC.
- `position_x`: x-position in cm.
- `position_y`: y-position in cm.
- `position_z`: z-position in cm.

The _optional_ attributes are
- `error_x`: x-position error in cm. Only necessary for alternative DCA calculations. Default value is 0.
- `error_y`: y-position error in cm. Only necessary for alternative DCA calculations. Default value is 0.
- `error_z`: z-position error in cm. Only necessary for alternative DCA calculations. Default value is 0.
- `total_pe`: Total number of photoelectrons (PE). Default value is -1.
- `plane`: Integer identifying the CRT wall. Default value is -1.
- `tagger`: String idenifying the CRT wall. Default value is `''`.

All of these attributes should be available from the larcv or sbnobj CRTHit instances. 

`CRTHit` contains one internatl method, `get_time_in_microseconds`, which uses the provided t0 information and converts it to a value in microseconds. This is called automatically when running `get_track_crthit_matches`. 

## `Track` Class
The `Track` class attributes are based on the `Particle` class from [lartpc_mlreco3d](https://github.com/DeepLearnPhysics/lartpc_mlreco3d/blob/develop/analysis/classes/Particle.py). The _required_ attributes are
- `id`: unique instance identifier
- `image_id`: identifier of the track image (or "event").
- `interaction_id`: identifier of the track interaction (or "vertex").
- `points`: (N, 3) array of 3D track points in cm.
- `depositions`: (N, 3) array of track point energy depositions. This array is used for determining track track and end points based on which end of the track has greater average energy within a given radius. Since this is relative, the specific unit used doesn't matter.

The _optional_ Track attributes correspond to track start and end point positions and directions. If _all_ of these are not provided, the start and end points, as well as their directions, are estimated using PCA on each track end within a user-defined radius. 
- `start_x`: x-position of start point in cm. Default value is None.
- `start_y`: y-position of start point in cm. Default value is None.
- `start_z`: z-position of start point in cm. Default value is None.
- `start_dir_x`: x-direction of start point. Default value is None.
- `start_dir_y`: y-direction of start point. Default value is None.
- `start_dir_z`: z-direction of start point. Default value is None.
- `end_x`: x-position of end point in cm. Default value is None.
- `end_y`: y-position of end point in cm. Default value is None.
- `end_z`: z-position of end point in cm. Default value is None.
- `end_dir_x`: x-direction of end point. Default value is None.
- `end_dir_y`: y-direction of end point. Default value is None.
- `end_dir_z`: z-direction of end point. Default value is None.

## `MatchCandidate` Class

When a match between a `Track` and `CRTHit` is found, the matched instances are stored in a `MatchCandidate` class instance. The attributes of this class are
- `track`: the matched `Track` instance.
- `crthit`: the matched `CRTHit` instance.
- `distance_of_closest_approach`: calculated DCA between the matched `Track` and `CRTHit`. 

## Running the Match-Making Algorithm

Once you have a list of `Track`s and `CRTHit`s, the match making can be run as
```
from matcha import match_maker
track_crthit_matches = match_maker.get_track_crthit_matches(tracks, crthits)
```

This returns a list of `MatchCandidate` instances. While each track end point can in principle have multiple match candidates, this function only returns the "best" match, i.e., the one with the minimum DCA for that `Track`. This means that the list `track_crthit_matches` will contain at most one `MatchCandidate` per `Track`. 

To tune the match making algorithm, you can pass any of the following optional parameters:
- `approach_distance_threshold`: Minimum DCA (in cm) required for a `MatchCandidate` instance to be created. Default value is 50.
- `dca_method`: Method of calculating DCA to use. Default value is `'simple'`. See `dca_methods.py` for other methods.
- `pca_radius`: If using PCA to determine track start and end points, the radius (in number of track points) to consider about each end. Default value is 10.
- `min_points_in_radius`: Minimum number of points within the PCA radius for PCA to be performed. Default value is 10. 
- `trigger_timestamp`: Timestamp value for the event trigger. Used for shifting CRT hit time values when running on data (i.e., requires `isdata=True`). Default value is `None`.
- `isdata`: Boolean flag indicating whether the input values are from simulation or from real data. Default value is `False`. Must be set to `True` if you supply a `trigger_timestamp` value. 
- `save_to_file`: Boolean flag indicating whether the output will be saved to a numpy `.npy` file. These files can be loaded into the `visualizer.ipynb` notebook. Default value is `False`.
- `file_path`: Path in which to save the `.npy` file. Default value is `'.'` (current directory). 

# Contributing

Please read the [contributing.md](https://github.com/andrewmogan/matcha/blob/main/contributing.md) file for information on how you can contribute.

# License
Distributed under the MIT License. See LICENSE for more information.

`




















