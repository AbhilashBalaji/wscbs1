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
