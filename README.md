# Big-Data-Portfolio

## Matrikelnummern der mitarbeitenden Studenten: 
7894464, 5562028, 7305370, 5763624, 8687786

## Grundsätzliche Idee der Anwendung: 
Die Grundlegende Idee der Anwendung war es eine Website zu bauen, die Tweets beschafft um daraus dann verschiedene Musik Genres herauszufiltern. Diese Tweets sollten dann je nach Genre gezählt werden, um herauszufinden, welches Genre am häufigsten in den Tweets erwähnt wird. Das Ergebnis dieser Zählung wird schließlich als Ranking auf der Startseite der Webanwendung angezeigt, wo sowohl die besten zehn Genres geordnet als auch alle anderen Genres abgefragt werden können. Sobald ein Genre aufgerufen wird, wird der Nutzer der Anwendung auf eine zweite Seite weitergeleitet. Dort ist dann eine kurze Beschreibung des Genre zu finden sowie generelle Informationen zur Seite. Die Gruppe entschloss sich für diese Idee aufgrund der Tatsache, dass festgestellt wurde, dass alle Gruppenmitglieder zwar eine Vorliebe für Musik, aber durchaus für verschiedene Genres teilen, weshalb auch das Enddesign des Frontends eine Homage an Spotify ist.

## Entwurf der Anwendung

### Startseite der Anwendung

![Startseite der App](/Anwendung_Startseite.jpg?raw=true 'Startseite der App')

#### Nähere Beschreibung der Komponenten & ihrer Funktionsweise

Die Idee der Startseite bestand darin, einen Überblick über verschiedene Musik Genres geben zu können. Im oberen Teil dieser Seite werden die zehn bekannsten Genres anhand der Anzahl ihrer Views absteigend vom Populärsten geordnet. Ein weiteres Element der Startseite ist die Auflistung aller Verfügbaren Genre. Diese können angeklickt werden, um eine nähere Beschreibung zur ausgewählten Musikrichtung zu erhalten. Ebenso werden im unteren Abschnitt der Seite weitere Informationen, wie beispielsweise Host, Datum, Memcached Servers, zur generierten Seite angezeigt.

### Zweite Seite der Anwendung

![Zweite Seite der App](/Anwedung_zweite_Seite.jpg?raw=true 'Genre Beschreibung auf Seite 2')

#### Nähere Beschreibung der Komponenten & ihrer Funktionsweise

Die zweite Seite gibt einen Überblick über das ausgewählte Genre, wie hier zum Beispiel Country. Unterhalb des Genres befindet sich eine kurze Beschreibung und ein Link mit dem man zur Startseite zurückkehren kann um ein anders Genre auswählen zu können.
Gleichermaßen wie auf der Startseite sind auf der zweiten Seite weitere Informationen zur generierten Seite zu finden.

## Code der zum Start & Inbetriebnahme der Anwendung notwendig ist

### Erste Schritte

- Docker Desktop starten
- Kubernetes aktivieren & starten
- cmd: `minikube start`

### Vorraussetzungen

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

###  Starten der App: (innerhalb des Ordners working der skaffold.yaml enthält) CMD

`skaffold dev`

Alternative:

- `skaffold run` für production --> Code changes werden nicht automatisch erneuert
- `skaffold debug`

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





## Wahl der Lizenz
Wir in der Gruppe haben uns dafür entschieden die Software mit der MIT-License zu lizenzieren.
Diese Lizenz beinhaltet, dass die Software weiterverbreitet und genutzt (kopiert, modifiziert, veröffentlicht, ...) werden kann, sofern jemand eine Kopie erhält. Die zugehörige Software befindet sich zu diesem Zeitpunkt in einem öffentlichen Github-Projekt. Wir gehen davon aus, dass die Software nur zu Benotungszwecken ausgeführt/weiterverbreitet wird. Sollte dies nicht der Fall sein, verfügt die Lizenz allerdings über einen Paragrafen, der sämtliche Gewährleistungsansprüche an die Ersteller des Repository zurückweist. Das ist uns ein wichtiges Anliegen, da mit der Software ein Twitteraccount verbunden ist. Darum wird an dieser Stelle nochmals ausdrücklich darum gebeten, die Software ausschließlich zu Benotungszwecken für das vorliegende Projekt zu verwenden. Als Lizenzgeber wird Max Bernauer genannt, da er derjenige ist, dem der verknüpfte Twitteraccount gehört.
