# starten der App: (innerhalb des Ordners der skaffold.yaml enthält)

skaffold dev

# Alternative: skaffold run für production --> Code changes werden nicht automatisch erneuert

# skaffold debug

# port forwarding: Open new cmd and type

kubectl port-forward service/my-super-app-service 8080:8080

# Clean-Up

1. Ctrl + C
2. skaffold

# Error handling
nginx error: https://stackoverflow.com/questions/61616203/nginx-ingress-controller-failed-calling-webhook

Handling: 
1. kubectl get validatingwebhookconfigurations
2. kubectl delete validatingwebhookconfigurations [configuration-name]
