#!/bin/bash

# Couleurs pour les messages
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[0;33m'
NC='\033[0m' # No Color

echo -e "${YELLOW}=== TalentMatch Backend Setup ===${NC}"

# Vérifier si Python est installé
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}Python 3 n'est pas installé. Veuillez l'installer avant de continuer.${NC}"
    exit 1
fi

# Vérifier si Docker et docker-compose sont installés
if ! command -v docker &> /dev/null || ! command -v docker-compose &> /dev/null; then
    echo -e "${RED}Docker et/ou docker-compose ne sont pas installés. Veuillez les installer avant de continuer.${NC}"
    exit 1
fi

# Si un environnement virtuel existe déjà, le supprimer pour une installation propre
if [ -d "venv" ]; then
    echo -e "${YELLOW}Suppression de l'environnement virtuel existant...${NC}"
    rm -rf venv
fi

# Créer un nouvel environnement virtuel
echo -e "${YELLOW}Création de l'environnement virtuel...${NC}"
python3 -m venv venv

# Activer l'environnement virtuel
echo -e "${YELLOW}Activation de l'environnement virtuel...${NC}"
source venv/bin/activate

# Mettre à jour pip
echo -e "${YELLOW}Mise à jour de pip...${NC}"
pip install --upgrade pip

# Installer les dépendances
echo -e "${YELLOW}Installation des dépendances...${NC}"
pip install -r requirements.txt

# Modifier le fichier .env pour utiliser le port 5433 pour PostgreSQL
echo -e "${YELLOW}Configuration du port PostgreSQL alternatif (5433)...${NC}"
sed -i.bak 's/POSTGRES_PORT=5432/POSTGRES_PORT=5433/g' .env 2>/dev/null || sed -i '' 's/POSTGRES_PORT=5432/POSTGRES_PORT=5433/g' .env

# Créer un script temporaire pour modifier docker-compose.yml
echo -e "${YELLOW}Configuration du port PostgreSQL dans docker-compose.yml...${NC}"
cat > ../update_docker_compose.sh << 'EOF'
#!/bin/bash
# Modifier le port PostgreSQL dans docker-compose.yml
if grep -q '"\${POSTGRES_PORT:-5432}:5432"' ../docker-compose.yml; then
    sed -i.bak 's/"\${POSTGRES_PORT:-5432}:5432"/"\${POSTGRES_PORT:-5433}:5432"/g' ../docker-compose.yml 2>/dev/null || \
    sed -i '' 's/"\${POSTGRES_PORT:-5432}:5432"/"\${POSTGRES_PORT:-5433}:5432"/g' ../docker-compose.yml
    echo "Port PostgreSQL modifié dans docker-compose.yml"
fi
EOF

# Rendre le script exécutable et l'exécuter
chmod +x ../update_docker_compose.sh
../update_docker_compose.sh
rm ../update_docker_compose.sh

# Rendre le script d'initialisation de la base de données exécutable
chmod +x init_db.py

# Démarrer les services avec Docker Compose (depuis la racine du projet)
echo -e "${YELLOW}Démarrage des services Docker (PostgreSQL, Redis, MinIO)...${NC}"
cd ..
docker-compose down -v postgres redis minio 2>/dev/null
docker-compose up -d postgres redis minio

# Attendre que PostgreSQL soit prêt
echo -e "${YELLOW}Attente de la disponibilité de PostgreSQL...${NC}"
sleep 15

# Initialiser la base de données avec notre script customisé
cd backend
echo -e "${YELLOW}Initialisation de la base de données...${NC}"
python init_db.py

if [ $? -eq 0 ]; then
    echo -e "${GREEN}Base de données initialisée avec succès!${NC}"
else
    echo -e "${RED}Erreur lors de l'initialisation de la base de données. Vérifiez les logs pour plus de détails.${NC}"
    echo -e "${YELLOW}Conseil: Assurez-vous que PostgreSQL est en cours d'exécution et accessible sur le port 5433.${NC}"
    echo -e "${YELLOW}Vous pouvez vérifier avec: docker ps | grep postgres${NC}"
fi

echo -e "${GREEN}Configuration terminée! Vous pouvez démarrer le backend avec:${NC}"
echo -e "${GREEN}cd backend && source venv/bin/activate && uvicorn app.main:app --reload --host 0.0.0.0 --port 8000${NC}"