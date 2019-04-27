# ☠️ Skeleton Environment Project ☠️

The goal of this project was to build a simple Python App and encase it in a docker environment which could also be deployed to Mini-Kube. I also decided to add Bazel Build functionality and integrate the project for use with circle CI. The environment also contains an instance of Prometheus and Grafana for monitoring metrics.

For learning purposes I have split the various stages of this into different branches and commits so others may also follow how I have set this up and that I may look back on the steps I took

#### Python App 🐍

The starting point is the Python app it's self. Using the http.Server library the program returns a JSON of data when a GET request is made to the endpoint `/trees` 🌳

I have set up pipenv for this project to self contain it's requirements, you can access the virtual environments shell through the command: `pipenv shell` 

🔗 You can read more about Python virtual environments here : https://docs.python-guide.org/dev/virtualenvs/

To run the program use the command `python main.py` from inside the `python_server` folder.

The port for the application is `8001` therefore if you run this locally you will be able to access the service at `localhost:8001/trees`


There are tests that run with [pytest](https://docs.pytest.org/en/latest/) for this program you can run them with the command `python -m pytest tests/`