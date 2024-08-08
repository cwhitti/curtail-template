# Curtail Template
Maintained by Claire Whittington

## Purpose
The purpose of this repository is to introduce a basic setup for the ReGrade tool. 
The ReGrade tool acts as a reverse-proxy between the user and tool, where it listens for requests and duplicates 
them to send to the different verions under test.
In this repository, I will explain the moving parts of the tool and its initial set-up.

**Keywords**
-
* Staging: The current official version of an application
* Dev    : The pieces of an application under development
* Version: The different files under review

**Directories**
-
| Directory                   | Purpose       |Required          | 
| -------------          | ------------- |  :-------------: |
| root       | Oversees the containerization of the ReGrade tool and the application under development | Yes | 
| private    | Holds config.json and stores the product key  | Yes |
| app        | One directory to hold all of the code for the application under development  | Recommended |
| app/source | Code that remains constant in all versions under test. By putting it in its own folder, it saves the developer from having to duplicate the same file for both versions. |  Recommended |
| app/staging| Holds the staging code.  |  Recommended |
| app/dev    | Holds the dev code.      |  Recommended |

**Files**
-
| File                   | Purpose       |Required          | 
| -------------          | ------------- |  :-------------: |
| dockerfile-compose.yaml| Establishes 5 containers: the ReGrade sensor, the ReGrade UI, the ReGrade database, the staging environment, and the dev environment | Yes | 
| Dockerfile             | Builds the staging and dev containers with the appropriate files.  | Yes |
| config.json            | Holds the settings for the ReGrade UI and most importantly the product key.  | Yes |
| server.py             | A general (or specialized) server which serves various endpoints that ReGrade can send traffic to. | Yes |
| traffic.sh             | Can be used to automate the process of sending traffic.  |  No |
| urls.sh                | Can be used to detect the IP:port of the sensor and UI.  |  No |
| run.py                 | Can be used by the Dockerfile to easily run the server upon starting the custom containers. Any language! |  No |

For example, a basic HTTP Python server may use a HTTP handler defined in another file.
In the event that the developer wants to add features to the HTTP file, they may store the 
current handler inside of the `staging` directory and the new handler inside of the `dev` directory.

## Getting Started
The basic structure for a new application for ReGrade to analyze can be found in the template directory of this repository. 

### config.json
 * Defines helpful parameters for the ReGrade UI.
 * SETUP: Configure `LicenseKey` as your license key.

### Dockerfile
 * After establishing the base image (gcc, python3.12, etc), the Dockerfile(s) will set up any required testing environments. In this template, it is set up to receive three arguments: `SERVERFILE`, `PORT` and `WKG_DIR`. These arguments will control which versions – dev or staging – that the environemt will test, on what port, and with which files. After building the image into a container, it will start the container.

### dockerfile-compose.yaml
* The configuration file for all containers. This file interacts with **Dockerfile** by establishing the working directory `WKG_DIR`,
port `PORT`, and executable `SERVERFILE`. 

* **curtail** 
  * Settings for the ReGrade sensor. Accessed from port 10081.
  * SETUP: Configure `DATABASE_URL` to your URL.

* **curtui**
  * Settings for the ReGrade UI. Accessed from port 14430.
  * SETUP: Configure `DATABASE_URL` to your URL.

* **curtdb**
  * Settings for the ReGrade database. Access from port 5434.
  * SETUP: Configure `POSTGRES_PASSWORD`

* **nginx**
  * Custom container to run the staging environment.
  * SETUP: Configure `SERVERFILE`, `WKG_DIR`, and `PORT`. This setup assumes you are developing two seperate files, with this container accessing the staging files.
  * _Note that the port argument should match the internal mapping._

* **envoy**
  * Custom container to run the dev environment.
  * SETUP: Configure `SERVERFILE`, `WKG_DIR`, and `PORT`. This setup assumes you are developing two seperate files, with this container accessing the dev files.
  * _Note that the port argument should match the internal mapping._

## Compiling Containers
Once your application has been integrated, you can now run all of the containers using `docker compose up`.
Take down the containers by using `docker compose down`.

Docker will cache any dependent files not explicitly mentioned in the docker-compile.yaml file. If you make changes to any files not in compose, you will have to force a new build with `docker compose up --build`.

# Examples
I have provided three examples in this repository that help showcase how to connect with ReGrade. Each example is built with an api "wrapper" which can ReGrade can communicate with. The API then can connect to a pre-existing application.

## Example A
A basic server setup with no intersting app connected to it. This was my first test to see if I could even get ReGrade to connect to any API.

## Examble B
Showcases how you could monitor SQL queries and use ReGrade to monitor a new patch. The API connects to a custom application which fetches and retrieves data. All traffic is controlled in traffic.sh which simulates grabbing data. 

The dbClass.py handles SQL commands and has two versions: secure (dev), and insecure. The secure version protects against an injection attack, the insecure version does not and will drop the SQL table on accident.

## Example C
Showcases how you could test a new release of an open-source or public tool. In this example, both codebases are the same, but one runs on python3.9.4 and the other runs on python3.12. The earlier version contains a bug that has been fixed in later versions. See: https://www.youtube.com/watch?v=lIniq12cMK0

