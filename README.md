# The Shared Identifiers Prototype

## Table of contents
* [General info](#general-info)
* [Getting Started](#getting-Started)
    *  [Prerequisites](#Prerequisites)
    *  [Installation](#Installation)
* [Related](#Related)
* [License](#License)

## General info
This prototype leverage the CSV file approach.

## Getting Started

Before getting started, make sure to correctly install the requirements, as described in the [Installation](#Installation) section.

To run the tests for this project, enter the following commands :
```
$ (env) pytest
```

To manually generate a test report for the project, enter the following commands :
```
$ (env) pytest --html=report.html
```

### How to conflate?

The script `conflate.py` allows you to conflate your stops to the MDB Stops following the first option steps, as described [here](https://github.com/MobilityData/mobility-database-interface/issues/338#issuecomment-999188292).

To run the script, you will need the [Installation](#Installation) to be completed and your virtual environment to be activated.

Enter the following command line to run the script:
```
$ python conflate.py -d $URL_OR_PATH_TO_YOUR_DATASET -D $YOUR_MDB_DATASET_ID -S $YOUR_MDB_SOURCE_ID -m $GET_STOPS_MODE -p $GET_STOPS_PARAMETERS -t $DISTANCE_THRESHOLD_IN_KM
```

The mode and parameter arguments are dependent. Make sure the parameters you provide are correct for the selected mode.

| Mode | Description | Argument | Parameters format |
|------|------|------|------|
| Standard | Get all the MDB Stops | 'std' | '{}' |
| By Boundary Box | Get the MDB Stops located in the boundary box | 'bounding_box' | '{"max_latitude": float, "min_latitude": float, "max_longitude": float, "min_longitude": float}' |
| By Stop ID | Get the MDB Stops for which a referenced stop has the given Stop ID | 'stop_id' | '{"stop_id": string}' |
| By Dataset ID | Get the MDB Stops for which a referenced stop has the given Dataset ID | 'dataset_id' | '{"dataset_id": string}' |
| By Source ID | Get the MDB Stops for which a referenced stop has the given Source ID | 'source_id' | '{"source_id": string}' |


### Operations

The package `tools` includes the operations for the prototype first option under `operations.py`, as described [here](https://github.com/MobilityData/mobility-database-interface/issues/338#issuecomment-999188292).

### Prerequisites

Please note that the software provided was developed and run on macOS Big Sur version 11.6.1 systems with Python 3.9.6.
While Python can run on a variety of systems, these instructions are written for the aforementioned specifications.
The repository does not contain the GTFS data, it must be downloaded.

### Installation

To correctly use and run this project, you must install all requirements. First, make sure Python 3.9+ and Pip are installed.
```
$ python3 --version
$ pip --version
```

If Python 3.9+ is not installed on your computer, get it with Homebrew (Mac) :
```
$ brew install python3.9
```
or with Apt (Linux) :
```
$ sudo apt-get install python3.9
```

If Pip is not installed on your computer, get it with the following commands :
```
curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
sudo python get-pip.py
```

Also, make sure you have both GDAL and RTree (Libspatialindex) libraries installed on your computer if you want to use the GTFS Kit library:
```
$ brew install GDAL
$ brew install spatialindex
```

It is suggested to set up a virtual environment before installing requirements. To set up and activate a Python 3.9 virtual environment, enter the following commands:
```
$ python3.9 -m venv env
$ source env/bin/activate
```

Once your virtual environment is activated, enter the following command to install the project requirements:
```
(env) $ pip install --default-timeout=120 -r requirements.txt
```

Note that you can get the [gtfs-kit library](https://pypi.org/project/gtfs-kit/) to help you manipulate GTFS datasets. To install it, enter the following command:
```
(env) $ pip install gtfs-kit
```

To deactivate your virtual environment, enter the following command:
```
(env) $ deactivate
```

If you are working with IntelliJ, it is possible to use this virtual environment within the IDE. To do so, follow the instructions to create a virtual environment in Intellij [here](https://www.jetbrains.com/help/idea/creating-virtual-environment.html).

## Related

- [gtfs-kit library](https://pypi.org/project/gtfs-kit/)

## License

TBD