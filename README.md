# Truck Routine
Check distance, time and fare for truck in South Korea

# Prerequisite
- This is based on SK T-MAP API. Therefore, please sign up https://tmapapi.sktelecom.com, and receive api key.

# How to use
1. Clone this repository
```shell
$ git clone git@github.com:aeuveritas/truck_routine.git
$ cd truck_routine
```

2. Make python virtual environment
```shell
$ python3 -m venv venv
```

3. Install required packages
```shell
$ pip install -r ./requirements.txt 
```

4. Copy locations_template.yaml to locations_my.yaml
```yaml
start:
  name: "my company"
  lat: 1.0
  long: 2.0
destinations:
  - name: "dest1"
    lat: 3.0
    long: 4.0
  - name: "dest2"
    lat: 5.0
    long: 6.0
  ...
```

5. Copy .env.template to .env.MY
```dotenv
API_KEY = <from https://tmapapi.sktelecom.com>
LOCATIONS_FILE = <from step 4>
CAR_TYPE = <one of car, mediumvan, largevan, largetruck, specialtruck, smallcar and twowheel>
TARGET_TIME = <no for periodic, or specific time like "2023/01/01 10:00">
```

6. Run main.py
```shell
$ python3 ./main.py --help
Usage: main.py [OPTIONS]

Options:
  --mode [periodic|specific]  [default: Mode.periodic]
  --env-file TEXT             [required]
  --help                      Show this message and exit.

# For periodic
$ python3 ./main.py --mode periodic --env-file=<from step 5>

# For specific
$ python3 ./main.py --mode specific --env-file=<from step 5>

```

