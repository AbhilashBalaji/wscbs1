# HOW TO RUN DOCKERFILES IN EACH MICROSERVICE


first we need build an image for each application using :

<code>docker build .</code>

after this command, image is created. so by running <code>docker images</code> we saw the list of images and retrieved the tag from the list. Then ran following command to give it a proper tag.

<code>docker tag 14f70b993a0b abhilashbalaji/wscbsa3:shortener</code>

It is worth mentioning that the image tag that we used was for dockerhub so later we can use it in kuberenetes.

Then we ran command <code>sudo docker run abhilashbalaji/wscbsa3:shortner</code> to create container for our image. Then to check the status of the container we ran following command: 

<code>docker ps -a</code>

Then we tested our application inside the container if it is working. After making sure the command is working, we needed to push it inside a repository to make use of it in kuberenetes.

We had two choices here, we either could run a local repository or push it into available online repositories like dockerhub. So we created an account on dockerhub and pushed our contianer in dockerhub by following command so we can use it in kubernetes later:

<code>sudo docker push abhilashbalaji/wscbsa3:shortner</code>

We ran same commands for our users shortener application.

------------------------------------------------------------------------

Now that we have our containers for users and shortener applications on dockerhub we can start with setting up kubernetes.

First We installed the kubernetes on the VM university provided us using following command and clusters and node using the provided k8s-setup-commands.pdf file by TA.

Then we installed git on VM so we can retrieve our yaml files for configuring the kuberenetes. Then by running following git command we cloned our repository for project.

<code>git clone https://github.com/AbhilashBalaji/wscbs1</code>

Then, in order to make a clean work and isolate groups of resources in a cluster, we created a namespace called "assignment3" so we can create all our objects related to this assignment in this namespace.

<code>kubectl create namespace assignment 3</code>

In each yaml file, we explained by details what each line meant to do. but first we need to deploy our application inside kubernetes. for that we created a <b>Deployment</b> for each microservice. after creating the deployment yaml files like [shortener-deployment.yaml](https://github.com/AbhilashBalaji/wscbs1/blob/main/assignment3/shortener/shortener-deployment.yaml), we used following command to apply it in kubernetes:

<code>kubectl apply -f shortener-deployment.yaml</code>

we did the same with our other deployment aswell. Then we checked to see if our pods with the container address that we gave from dockerhub, are being created and running or not by running following command.

<code>kubectl get pods --namespace=assignment3</code> or <code>kubectl get pods -n assignment3</code>

it took few seconds for them to reach the running status.

After all pods are running. we need to make them accessable to other resources or outside world. So we created a service for each deployment like [shortener-service.yaml](https://github.com/AbhilashBalaji/wscbs1/blob/main/assignment3/shortener/shortener-service.yaml). since we did not deploy the proxy inside the cluster, then we need to expose the deployment to outside world. that is why we used NodePort. then applied it with following command:

<code>kubectl apply -f shortener-service.yaml</code>

Then after that the kubernetes exposes our application to outside world using the <NodeIP>:<NodePort> we provided (30500 and 30600 for each or our deplotments).

Then inorder to scaleup services independently of each other during the peak time, we used HorizontalAutoScaler object so when ever we faced a resource like CPU faced an increased load, the autoscalers deploys another pod. and we applied it with the same apply command:
  
<code>kubectl apply -f shortener-horizontal-scaler.yaml</code>

we applied a minimum of 4 pods but in our deployment we mentioned 3 replicas. so when we applied our horizontal autoscaler, the kubernetes created one more pod for us to reach the requirement of minimum 4 replica for the deployment.
