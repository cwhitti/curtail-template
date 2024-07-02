# Curtail Template
Maintained by Claire Whittington

## Purpose
The purpose of this repository is to introduce a basic setup for the ReGrade tool. 
In this repository, I will explain the moving parts of the tool and document important things to change.

## Template Overview
This template is set up to allow for the interchangeable testing of multiple files. 

For example, a basic HTTP Python server may use a HTTP handler defined in another file.
In the event that the developer wants to add features to the HTTP file, they may store the 
current handler inside of the `staging` directory and the new handler inside of the `dev` directory.

The `docker-compose.yaml` file interacts with `Dockerfile` by establishing the working directory `WKG_DIR`,
port `PORT`, and executable `SERVERFILE`. 


### Important Files
| File        | Purpose           | 
| ------------- |:-------------:| 
| Dockerfile      | Sets up containers to test different environments. It is set up to receive three arguments: `SERVERFILE`, `PORT` and `WKG_DIR` | 
| dockerfile-compose.yaml      | Establishes 5 containers: The Curtail Sensor, Curtail UI, Curtail Database, staging container, and development container. For the most part, the first three are not meant to be touched.   | 
| private/congig.json | are neat      | 


### Optional Files
| File        | Purpose           | 
| ------------- |:-------------:| 
| traffic.sh | are neat      | 
| zebra stripes | are neat      | 
| zebra stripes | are neat      | 
| zebra stripes | are neat      | 
| zebra stripes | are neat      | 
| zebra stripes | are neat      | 
| zebra stripes | are neat      | 
| zebra stripes | are neat      | 
| zebra stripes | are neat      | 
| zebra stripes | are neat      | 
| zebra stripes | are neat      | 
