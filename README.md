# ☠️ Skeleton Environment Project ☠️

The goal of this project was to build a simple Python App and encase it in a docker environment which could also be deployed to Mini-Kube. I also decided to add Bazel Build functionality and integrate the project for use with circle CI. The environment also contains an instance of Prometheus and Grafana for monitoring metrics.

For learning purposes I have split the various stages of this into different branches and commits so others may also follow how I have set this up and that I may look back on the steps I took.


----

### [Step One: Python App](https://github.com/sleepypioneer/skeleton-environment/tree/step_one_python_app) 🐍

The starting point is the Python app it's self. Using the http.Server library the program returns a JSON of data when a GET request is made to the endpoint `/trees` 🌳 any other endpoint returns `404` error.

I have set up pipenv for this project to self contain it's requirements, you can access the virtual environments shell through the command: `pipenv shell` 

🔗 You can read more about Python virtual environments here : https://docs.python-guide.org/dev/virtualenvs/

To run the program use the command `python main.py` from inside the `python_server` folder.

The port for the application is `8001` therefore if you run this locally you will be able to access the service at `localhost:8001/trees`


There are tests inside `./python_server/tests` that run with [pytest](https://docs.pytest.org/en/latest/) for this program you can run them with the command `python -m pytest tests/`


----

### [Step Two: Adding the App to our environment with Docker-Compose](https://github.com/sleepypioneer/skeleton-environment/tree/step_two_docker_compose) 🐋

By adding a `dockerfile` to python_server we can define the app’s environment, so it can be reproduced anywhere. We can then use docker-compose to run our app in an isolated environment with the command `docker-compose up` don't forget to add the flag `--build` if changes have been made.


----


### [Step three: Building our project with Bazel](https://github.com/sleepypioneer/skeleton-environment/tree/step_three_bazel_build) 💚 

We can use the build tool [Bazel](https://bazel.build/) in our environment so we can easily build our Python App and any additional services we decide to add in our environment.

First we need a `WORKSPACE` file at the root, here are all the archive/ git repositories for python the main ones would be the `io_bazel_rules_python` but we will also need the `io__bazel_rules_docker` for running our app through docker.

We will also already set up [Gazelle](https://github.com/bazelbuild/bazel-gazelle) a build file generator, primary for GO projects it will create the necessary files for our environment to be built using Bazel.

When the archive has been imported and rule set loaded Gazelle can be run with `bazel run gazelle`.

To run the Python App we will need to add to the `WORKSPACE` the necessary archives for python, the main ones being `io_bazel_rules_python` but we will also need the `io__bazel_rules_docker` for running our app through docker. Take a look through the complete ``WORKSPACE` file to see how this is done.

We also need to add a `BUILD.bazel` file in the application folder. Here we define our rules. 

```
py_binary(
    name = "server",
    srcs = ["main.py"],
    main = "main.py",
    deps = [
        # This takes the name as specified in requirements.txt
        requirement("requests"),
        requirement("prometheus_client"),
    ],
    python_version = "PY3",
  )
```

Here we are stipulating we want to use Python 3 to get this to run correctly at runtime we also need to add a runtime rule *(otherwise you can hit problems where the Python being used is not the one stipulated)*

```
py_runtime(
    name = "myruntime",
    interpreter_path = select({
        # Update paths as appropriate for your system.
        "@bazel_tools//tools/python:PY2": "/usr/bin/python",
        "@bazel_tools//tools/python:PY3": "/usr/bin/python3",
    }),
    files = [],
)
```

To build the Python app with Bazel:

`bazel run //python_server:server --python_top=//python_server:myruntime`

The port will be the same as above and when run locally should be as before reachable at `localhost:8001/trees`.

Our Docker version can be run with:

`bazel run //python_server:server.image --python_top=//python_server:myruntime`

In this case we will not see the logging until the process is stopped with `control c` but can check it's working at the same URL.


----

### [Adding Metrics to our App with the Python Prometheus Client](https://github.com/sleepypioneer/skeleton-environment/tree/step_four_adding_metrics) 🔥

Using the [Python Prometheus Client](https://github.com/prometheus/client_python) we can scrape metrics from our Python App. First we will need to add an endpoint to view them on. Instead of [BaseHTTPRequest](https://docs.python.org/2/library/basehttpserver.html) we can use MetricsHandle](https://github.com/prometheus/client_python/blob/3cb4c9247f3f08dfbe650b6bdf1f53aa5f6683c1/prometheus_client/exposition.py#L141) wrapper class. This allow us to then set a `/metrics` endpoint.

```
elif endpoint == '/metrics':  
  return super(HTTPRequestHandler, self).do_GET()
```

*(Be wary of issues with HTTP 1:1 : https://github.com/prometheus/client_python/issues/299)*

We can now implement a metric in our Python App using the prometheus metric types, we will start with the counter.

#### Counter ⏲️
Counters go up, and reset when the process restarts.

```
from prometheus_client import Counter
c = Counter('my_failures', 'Description of counter')
c.inc()     # Increment by 1
c.inc(1.6)  # Increment by given value
```

https://github.com/prometheus/client_python#counter


#### labels 🏷️

... Labels can also be passed as keyword-arguments:

```
from prometheus_client import Counter
c = Counter('my_requests_total', 'HTTP Failures', ['method', 'endpoint'])
c.labels(method='get', endpoint='/').inc()
c.labels(method='post', endpoint='/submit').inc()
```

https://github.com/prometheus/client_python#labels

`c = Counter('requests_total', 'requests', ['status', 'endpoint'])`

#### Adding the counter to our App 📈

We add the following to where we want to increment our counter, in this case when a request to the `/trees` endpoint is made. In this example the values for the labels are hardcoded in.

`c.labels(status='200', endpoint='/trees').inc()`


----

### [Adding Prometheus 🔥 and Grafana 📈 to our environment](https://github.com/sleepypioneer/skeleton-environment/tree/step_five_prometheus_and_grafana)

Now that we have metrics running in our App we can add Prometheus to our environment so we can capture the metrics and query them. We will also add Grafana to the environment so we can create a dashboard. We do so by adding instances of both to our docker-compose file. 

Now when we start the docker environment with `docker-compose up --build`

The Python Server App is available at port: `8001`
Prometheus is available at port: `9090`
Grafana is available at port: `3000`

In the `prometheus.yaml` we set Prometheus up to scrape the metrics from our Python App. Grafana is set up to scrape from prometheus. It requires a login this is defined in the `docker-compose.yaml`.


----

### [Deploying to Kubernetes](https://github.com/sleepypioneer/skeleton-environment/tree/step_six_deploying_to_kubernetes) ⚙️

In this step we will deploy our Python App in [Kubernetes](https://kubernetes.io/) locally using [MiniKube](https://kubernetes.io/docs/setup/minikube/).

First we need to build an image of our Python App using the `docker build -t sleepypioneer/pythonserver .` command inside the Python App folder which follows what we have defined in our `dockerfile`. we choose the tag sleepypioneer/pythonserver as it responds to <docker-hub-name>/<project-name> this is an optimisation for when we want to publish the image to [Docker Hub](https://hub.docker.com) with `docker push`.

We can then push this to Docker Hub with the following command pattern:

`docker login` log into docker hub account

`docker push sleepypioneer/pythonserver`

We will need to install MiniKube and additionaly we will need [kubectl](https://kubernetes.io/docs/tasks/tools/install-kubectl/).

To start MiniKube run `minikube start`.

If we now run `kubectx` we will see that we are now in the `minikube` context.

#### Create deployment:
`kubectl create deployment pythonserver --image=sleepypioneer/pythonserver`

`kubectl get deployments`  
`kubectl get pods`

#### Create service:
`kubectl expose deployment pythonserver --type=LoadBalancer --port=8001`

*"The --type=LoadBalancer flag indicates that you want to expose your Service outside of the cluster."*

###### Useful commands
`kubectl get services`  
`kubectl cluster-info`  
`kubectl delete service pythonserver`

#### Run the Minikube Dashboard:
`minikube dashboard` Opens the dashboard in the browser, you can use it to see your services/deployments/pods and check the health of your cluster as well workloads.

#### Run service:
`minikube service pythonserver` Will open the service up inside the browser. You can also use the `--url=true` flag to return the URL the service is running at instead of opening it in the default browser.

#### Scale up - add more replicas(pods) of our service:
`kubectl scale deploy pythonserver --replicas=2` 

### Diagram of how our cluster looks:
<img src="/documentation/images/skeleton-project-cluster-diagram.png"/>


---

### [Deploying Prometheus to Kubernetes & exposing Services](https://github.com/sleepypioneer/skeleton-environment/tree/step_seven_prometheus_in_kubernetes) ⚙️

Now we have our service running in the cluster we want to add Prometheus and eventually Grafana. We will also need to make sure our Python Server is configured to expose it's metrics. To this we will use a number of `yaml` files to create ClusterRoles, Configmaps, Deployments, and Services.

We will start with the Python Server inside the folder `python_server` there are two files `deployment.yaml` and `service.yaml` we can use these to deploy our Python Server instead of using the bash commands we used in the previous section.

First we will remove the previous deployment by running the command:  
```bash
kubectl delete deployment/pythonserver
```  
*(This will delete the deployment, service and pods we created in the last section.)*

Now we will create the new deployment using the `deployment.yaml` file we do so by running the following file inside the `python_server` folder: 
```bash 
kubectl apply -f deployment.yaml  
```

In the same folder now run:  
```bash
kubectl apply -f service.yaml
```

This will create the service and pods for the Python Server deployment, they will be almost identical to what we created previously the only difference is that we have now added annotations to the pods to allow prometheus to scrape the `/metrics` endpoint. This can be seen in the `deployments.yaml` file in the template section.

```yaml
template:  
     metadata:  
        annotations:  
          prometheus.io/scrape: 'true'  
```

Now that we have the Python Server running in the cluster with prometheus scrape annotation we can move on to deploying the Prometheus Service itself. We will set up a `monitoring` namespace for our Prometheus and Grafana pods to live in, to do this run the following command from inside the `/system/monitoring/` folder.

```bash
kubectl apply -f namespace.yaml
```

Now if you run `kubens` you will see there is a namespace called `monitoring`. We also need to create a ClusterRole so that Prometheus has the correct permissions to be able to scrape other resources. Still in the `/system/monitoring/` folder run:  

```bash
kubectl apply -f rbac.yml
```

Next we will create the configmap if you look at the `prometheus-configmap.yaml` you will see that this file used regex to be able to scrape different resources and assign them labels (when we look in prometheus you will see where these labels get used). *Note that we assign it to the monitoring namespace.*

```bash
kubectl apply -f prometheus-configmap.yaml --namespace=monitoring
```

Now we can create the Prometheus deployment:  
```bash
kubectl apply -f prometheus-deployment.yaml --namespace=monitoring
```

And Prometheus Service:  
```bash
kubectl apply -f prometheus-service.yaml --namespace=monitoring
```

If we run `minikube service prometheus-service  --namespace=monitoring` prometheus will now open in the default browser. If we search for the `request_total` metric which we created for our Python Server we should see it, unless you have been making calls to the Python Server endpoint there will be no values for the metric.

Next we will deploy Grafana in a similar pattern. We do not need a ClusterRole for this one just a deployment and service. Still inside the `/system/monitoring/` folder run:  

```bash
kubectl apply -f grafana-deployment.yaml --namespace=monitoring  
kubectl apply -f grafana-service.yaml --namespace=monitoring  
```

We can run the service with `minikube service grafana  --namespace=monitoring` you will still need to sign in as before (default username and password is admin/admin you will then be asked to change it).

Inside the Grafana UI we can now set a data source and create Dashboards with the metrics from our Python Server App. You can follow along some instructions [here](/documentation/grafana-tutorial.md) to get started and if you would like to find out more I can reccomend the [Grafana documentation](https://grafana.com/docs/guides/getting_started/).