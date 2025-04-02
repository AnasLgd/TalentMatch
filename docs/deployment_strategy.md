# Stratégie de Déploiement pour TalentMatch

Ce document décrit la stratégie de déploiement de TalentMatch sur le VPS Hostinger KVM2 avec n8n préinstallé.

## Architecture de Déploiement

TalentMatch est déployé en utilisant Docker et Docker Compose avec les services suivants :

- **Backend FastAPI** : API REST pour toutes les fonctionnalités
- **Frontend Next.js** : Interface utilisateur
- **PostgreSQL** : Base de données principale
- **Redis** : Cache et file d'attente
- **MinIO** : Stockage d'objets pour les fichiers (CV, portfolios, etc.)
- **n8n** : Moteur de workflow pour l'automatisation

## Prérequis

- VPS Hostinger KVM2 avec Ubuntu 24.04.2 LTS
- Docker et Docker Compose installés
- n8n préinstallé (port modifié de 5678 à 5679)

## Étapes de Déploiement

### 1. Préparation du Code Source

1. Cloner le dépôt TalentMatch depuis GitHub
2. Configurer les variables d'environnement
3. Construire les images Docker

### 2. Configuration de la Base de Données

1. Initialiser la base de données PostgreSQL
2. Exécuter les migrations Alembic
3. Charger les données initiales (si nécessaire)

### 3. Déploiement des Services

1. Démarrer les services avec Docker Compose
2. Vérifier que tous les services sont opérationnels
3. Configurer les workflows n8n

### 4. Configuration du Réseau

1. Configurer Nginx comme proxy inverse
2. Mettre en place SSL avec Let's Encrypt
3. Configurer les règles de pare-feu

## Scripts de Déploiement

Les scripts suivants sont fournis pour faciliter le déploiement :

- `deploy.sh` : Script principal de déploiement
- `backup.sh` : Script de sauvegarde de la base de données et des fichiers
- `update.sh` : Script de mise à jour de l'application

## Surveillance et Maintenance

- Mise en place de la surveillance avec Prometheus et Grafana
- Configuration des alertes
- Planification des sauvegardes régulières

## Rollback

En cas de problème lors du déploiement, la procédure de rollback est la suivante :

1. Arrêter les services défectueux
2. Restaurer la dernière sauvegarde fonctionnelle
3. Redémarrer les services

## Considérations de Sécurité

- Toutes les communications sont chiffrées avec SSL
- Les secrets sont stockés dans des variables d'environnement
- L'accès à la base de données est limité aux services internes
- Les données sensibles sont chiffrées au repos
