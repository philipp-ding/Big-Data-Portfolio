# Big-Data-Portfolio

start docker desktop and make sure your docker engine is running

navigate in the right folder via
cd container_test

to build the container run:
docker build -t pysparktest .

to run the container and see the output from the python code run
docker run -it pysparktest

kubectl get pods
kubectl delete -f pod-mysql_v3.yaml
kubectl apply -f pod-mysql_v3.yaml
kubectl exec -ti mariadb-deployment-f9c5768f8-pqsfn -- mysql -u root --password=mysecretpw sportsdb

=> Select \* from missions;
