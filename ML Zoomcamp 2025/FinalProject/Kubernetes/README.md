# Kubernetes Deployment (kubectl)

This folder contains Kubernetes manifests to deploy the FastAPI model server.

## Prerequisites

- A Kubernetes cluster (minikube / kind / EKS / GKE / AKS)
- `kubectl` configured to talk to your cluster
- A built & pushed container image for the API (or loaded into your local cluster)


## 1) Apply manifests

From the repo root:

```bash
kubectl apply -f Kubernetes/deployment.yaml
kubectl apply -f Kubernetes/service.yaml
```

## 3) Verify

```bash
kubectl get pods
kubectl get deploy
kubectl get svc
```

## 4) Access the service

### Option A: Port-forward (works everywhere)

```bash
kubectl port-forward service/airbnb-ml-api 8000:80
```

Then open:

- `http://127.0.0.1:8000/`

### Option B: LoadBalancer / minikube

If you are using minikube:

```bash
minikube service airbnb-ml-api --url
```

## 5) Clean up

```bash
kubectl delete -f Kubernetes/service.yaml
kubectl delete -f Kubernetes/deployment.yaml
```
