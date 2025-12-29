#!/bin/bash
# ============================================
# UtopiaHire - Docker Management Script
# ============================================
# Usage: ./docker.sh [command]
# ============================================

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
NC='\033[0m' # No Color

# Project name
PROJECT_NAME="utopiahire"

print_header() {
    echo -e "${PURPLE}============================================${NC}"
    echo -e "${BLUE}🚀 UtopiaHire - Docker Management${NC}"
    echo -e "${PURPLE}============================================${NC}"
}

print_help() {
    print_header
    echo ""
    echo -e "${GREEN}Available commands:${NC}"
    echo ""
    echo -e "  ${YELLOW}dev${NC}        - Start development environment"
    echo -e "  ${YELLOW}prod${NC}       - Start production environment"
    echo -e "  ${YELLOW}build${NC}      - Build all Docker images"
    echo -e "  ${YELLOW}stop${NC}       - Stop all containers"
    echo -e "  ${YELLOW}restart${NC}    - Restart all containers"
    echo -e "  ${YELLOW}logs${NC}       - View logs (follow mode)"
    echo -e "  ${YELLOW}logs-backend${NC}  - View backend logs only"
    echo -e "  ${YELLOW}logs-frontend${NC} - View frontend logs only"
    echo -e "  ${YELLOW}status${NC}     - Show container status"
    echo -e "  ${YELLOW}shell-backend${NC}  - Open shell in backend container"
    echo -e "  ${YELLOW}shell-db${NC}   - Open PostgreSQL shell"
    echo -e "  ${YELLOW}clean${NC}      - Stop and remove all containers, networks, volumes"
    echo -e "  ${YELLOW}prune${NC}      - Remove unused Docker resources"
    echo ""
    echo -e "${GREEN}Examples:${NC}"
    echo "  ./docker.sh dev        # Start development"
    echo "  ./docker.sh logs       # View all logs"
    echo "  ./docker.sh shell-db   # Access database"
    echo ""
}

check_env() {
    if [ ! -f ".env" ] && [ ! -f ".env.docker" ]; then
        echo -e "${YELLOW}⚠️  No .env file found!${NC}"
        echo -e "${YELLOW}   Creating from .env.docker template...${NC}"
        if [ -f ".env.docker" ]; then
            cp .env.docker .env
            echo -e "${GREEN}✅ Created .env from .env.docker${NC}"
            echo -e "${YELLOW}   Please edit .env with your API keys!${NC}"
        else
            echo -e "${RED}❌ No .env.docker template found!${NC}"
            exit 1
        fi
    fi
}

dev() {
    print_header
    echo -e "${GREEN}🔧 Starting development environment...${NC}"
    check_env
    docker-compose up -d
    echo ""
    echo -e "${GREEN}✅ Development environment started!${NC}"
    echo ""
    echo -e "${BLUE}📍 Services:${NC}"
    echo -e "   Frontend:  ${GREEN}http://localhost:3000${NC}"
    echo -e "   Backend:   ${GREEN}http://localhost:8000${NC}"
    echo -e "   API Docs:  ${GREEN}http://localhost:8000/docs${NC}"
    echo -e "   Database:  ${GREEN}localhost:5432${NC}"
    echo ""
    echo -e "${YELLOW}💡 Tip: Run './docker.sh logs' to view logs${NC}"
}

prod() {
    print_header
    echo -e "${GREEN}🚀 Starting production environment...${NC}"
    check_env
    docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d
    echo ""
    echo -e "${GREEN}✅ Production environment started!${NC}"
}

build() {
    print_header
    echo -e "${GREEN}🔨 Building Docker images...${NC}"
    docker-compose build --no-cache
    echo -e "${GREEN}✅ Build complete!${NC}"
}

stop() {
    print_header
    echo -e "${YELLOW}⏹️  Stopping containers...${NC}"
    docker-compose down
    echo -e "${GREEN}✅ Containers stopped${NC}"
}

restart() {
    print_header
    echo -e "${YELLOW}🔄 Restarting containers...${NC}"
    docker-compose restart
    echo -e "${GREEN}✅ Containers restarted${NC}"
}

logs() {
    docker-compose logs -f
}

logs_backend() {
    docker-compose logs -f backend
}

logs_frontend() {
    docker-compose logs -f frontend
}

status() {
    print_header
    echo -e "${GREEN}📊 Container Status:${NC}"
    echo ""
    docker-compose ps
}

shell_backend() {
    echo -e "${GREEN}🐚 Opening shell in backend container...${NC}"
    docker-compose exec backend /bin/bash
}

shell_db() {
    echo -e "${GREEN}🗄️  Opening PostgreSQL shell...${NC}"
    docker-compose exec db psql -U ${DB_USER:-utopiahire} -d ${DB_NAME:-utopiahire}
}

clean() {
    print_header
    echo -e "${RED}⚠️  This will remove all containers, networks, and volumes!${NC}"
    read -p "Are you sure? (y/N) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        echo -e "${YELLOW}🧹 Cleaning up...${NC}"
        docker-compose down -v --rmi local
        echo -e "${GREEN}✅ Cleanup complete${NC}"
    else
        echo -e "${YELLOW}Cancelled${NC}"
    fi
}

prune() {
    print_header
    echo -e "${YELLOW}🧹 Pruning unused Docker resources...${NC}"
    docker system prune -f
    echo -e "${GREEN}✅ Prune complete${NC}"
}

# Main
case "${1:-help}" in
    dev)
        dev
        ;;
    prod)
        prod
        ;;
    build)
        build
        ;;
    stop)
        stop
        ;;
    restart)
        restart
        ;;
    logs)
        logs
        ;;
    logs-backend)
        logs_backend
        ;;
    logs-frontend)
        logs_frontend
        ;;
    status)
        status
        ;;
    shell-backend)
        shell_backend
        ;;
    shell-db)
        shell_db
        ;;
    clean)
        clean
        ;;
    prune)
        prune
        ;;
    help|--help|-h|*)
        print_help
        ;;
esac
