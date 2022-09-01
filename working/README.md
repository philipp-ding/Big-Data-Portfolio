# Code der zum Start & Betriebnahme der Anwendung notwendig ist

### Erste Schritte

- Docker Desktop starten
- Kubernetes aktivieren & starten
- `minikube start`

## Vorraussetzungen

Laufender Strimizi.io Kafka operator

```
helm repo add strimzi http://strimzi.io/charts/
helm install my-kafka-operator strimzi/strimzi-kafka-operator
kubectl apply -f https://farberg.de/talks/big-data/code/helm-kafka-operator/kafka-cluster-def.yaml
```

Ein laufendes Hadoop cluster mit YARN

```
helm repo add stable https://charts.helm.sh/stable
helm install --namespace=default --set hdfs.dataNode.replicas=1 --set yarn.nodeManager.replicas=1 --set hdfs.webhdfs.enabled=true my-hadoop-cluster stable/hadoop
```

### starten der App: (innerhalb des Ordners working der skaffold.yaml enthält)

`skaffold dev`

Alternative:

- skaffold run für production --> Code changes werden nicht automatisch erneuert
- skaffold debug

skaffold.exe muss auf dem Computer zum ausführen dises Befehls vorhanden sein

### port forwarding: Open new cmd and type

`kubectl port-forward service/my-super-app-service 8080:8080`

### Clean-Up

1. Ctrl + C
2. `skaffold delete`

### Error handling

nginx error: https://stackoverflow.com/questions/61616203/nginx-ingress-controller-failed-calling-webhook

Handling:

1. `kubectl get validatingwebhookconfigurations`
2. `kubectl delete validatingwebhookconfigurations [configuration-name]`
