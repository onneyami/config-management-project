# Управление конфигурацией в Kubernetes: от ConfigMap до Vault

Этот проект демонстрирует эволюцию подходов к управлению конфигурацией и секретами в Kubernetes.

## Содержание

- [Цель проекта](#цель-проекта)
- [Технологии](#технологии)
- [Структура](#структура)
- [Часть 1: Базовые ConfigMap и Secret](#часть-1-базовые-configmap-и-secret)
- [Часть 2: Динамическое обновление через volume mount](#часть-2-динамическое-обновление-через-volume-mount)
- [Часть 3: Внешние секреты с Vault и External Secrets Operator](#часть-3-внешние-секреты-с-vault-и-external-secrets-operator)
- [Часть 4: Автоматический рестарт подов с Reloader](#часть-4-автоматический-рестарт-подов-с-reloader)
- [Как использовать](#как-использовать)
- [Заключение](#заключение)

## Цель проекта

Показать комплексный подход к управлению конфигурацией:

- разделение конфигурации и кода;
- безопасное хранение секретов;
- динамическое обновление без простоя;
- интеграция с внешними системами секретов.

## Технологии

- Kubernetes (kind/minikube)
- ConfigMap / Secret
- HashiCorp Vault
- External Secrets Operator
- Reloader (stakater)
- Docker / Python (для демо-приложения)
- Git


## Часть 1: Базовые ConfigMap и Secret

Создаём ConfigMap с настройками окружения и Secret с API-ключом. Deployment получает их как переменные окружения.

```bash
kubectl apply -f 01-basics/configmap.yaml
kubectl apply -f 01-basics/secret.yaml
kubectl apply -f 01-basics/deployment-env.yaml
```

## Часть 2: Динамическое обновление через volume mount

```
docker build -t dynamic-app:latest 02-dynamic-update/test-app/
kind load docker-image dynamic-app:latest

kubectl apply -f 02-dynamic-update/configmap-dynamic.yaml
kubectl apply -f 02-dynamic-update/deployment-volume.yaml

kubectl edit configmap dynamic-config
kubectl logs -f deployment/dynamic-app

```

## Часть 3: Внешние секреты с Vault и External Secrets Operator

### Установка Vault (dev-режим)

```
kubectl apply -f 03-external-secrets/vault/vault-dev.yaml
./scripts/port-forward-vault.sh
# In other terminal:
export VAULT_ADDR=http://localhost:8200
export VAULT_TOKEN=root-token
vault kv put secret/demo-app api-key="vault-api-key-123" db-password="vault-db-pass"
```

### Установка External Secrets Operator

```
helm repo add external-secrets https://charts.external-secrets.io
helm install external-secrets external-secrets/external-secrets \
  -n external-secrets --create-namespace
```

### Создание SecretStore и ExternalSecret

```
kubectl apply -f 03-external-secrets/eso/secretstore.yaml
kubectl apply -f 03-external-secrets/eso/externalsecret.yaml
```

### Использование в поде

```
kubectl apply -f 03-external-secrets/deployment-with-eso.yaml
kubectl exec deployment/app-with-eso -- env | grep API_KEY
```

## Часть 4: Автоматический рестарт подов с Reloader

```
helm repo add stakater https://stakater.github.io/stakater-charts
helm install reloader stakater/reloader

kubectl apply -f 04-reloader/deployment-with-annotations.yaml
```
