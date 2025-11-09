#!/bin/bash
# CareerStar - Database Setup Script
# Creates PostgreSQL database and runs all migrations

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Get the absolute path to the project root
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo ""
echo -e "${PURPLE}========================================${NC}"
echo -e "${BLUE}🗄️  CareerStar - Database Setup${NC}"
echo -e "${PURPLE}========================================${NC}"
echo ""

# Load environment variables
if [ -f "$PROJECT_ROOT/.env" ]; then
    echo -e "${GREEN}📋 Loading environment variables...${NC}"
    export $(cat "$PROJECT_ROOT/.env" | grep -v '^#' | xargs)
    echo -e "${GREEN}✅ Environment loaded${NC}"
else
    echo -e "${YELLOW}⚠️  .env file not found${NC}"
    echo -e "${YELLOW}   Copying from .env.example...${NC}"
    if [ -f "$PROJECT_ROOT/.env.example" ]; then
        cp "$PROJECT_ROOT/.env.example" "$PROJECT_ROOT/.env"
        echo -e "${GREEN}✅ .env file created${NC}"
        echo -e "${YELLOW}⚠️  Please edit .env with your PostgreSQL credentials${NC}"
        echo ""
        echo -e "${BLUE}Required settings in .env:${NC}"
        echo "  DATABASE_URL=postgresql://user:password@localhost:5432/careerstar_db"
        echo "  POSTGRES_USER=your_username"
        echo "  POSTGRES_PASSWORD=your_password"
        echo "  POSTGRES_DB=careerstar_db"
        echo ""
        read -p "Press Enter after editing .env file..."
        export $(cat "$PROJECT_ROOT/.env" | grep -v '^#' | xargs)
    else
        echo -e "${RED}❌ .env.example not found${NC}"
        exit 1
    fi
fi

# Extract database credentials from DATABASE_URL or use individual variables
if [ -n "$DATABASE_URL" ]; then
    # Parse DATABASE_URL: postgresql://user:password@host:port/dbname
    DB_USER=$(echo $DATABASE_URL | sed -n 's|.*://\([^:]*\):.*|\1|p')
    DB_PASS=$(echo $DATABASE_URL | sed -n 's|.*://[^:]*:\([^@]*\)@.*|\1|p')
    DB_HOST=$(echo $DATABASE_URL | sed -n 's|.*@\([^:]*\):.*|\1|p')
    DB_PORT=$(echo $DATABASE_URL | sed -n 's|.*:\([0-9]*\)/.*|\1|p')
    DB_NAME=$(echo $DATABASE_URL | sed -n 's|.*/\([^?]*\).*|\1|p')
else
    DB_USER=${POSTGRES_USER:-postgres}
    DB_PASS=${POSTGRES_PASSWORD}
    DB_HOST=${POSTGRES_HOST:-localhost}
    DB_PORT=${POSTGRES_PORT:-5432}
    DB_NAME=${POSTGRES_DB:-careerstar_db}
fi

echo ""
echo -e "${BLUE}📊 Database Configuration:${NC}"
echo -e "   Host: ${DB_HOST}"
echo -e "   Port: ${DB_PORT}"
echo -e "   Database: ${DB_NAME}"
echo -e "   User: ${DB_USER}"
echo ""

# Check if PostgreSQL is installed
if ! command -v psql &> /dev/null; then
    echo -e "${RED}❌ PostgreSQL is not installed${NC}"
    echo ""
    echo -e "${YELLOW}Install PostgreSQL:${NC}"
    echo "  Ubuntu/Debian: sudo apt-get install postgresql postgresql-contrib"
    echo "  macOS: brew install postgresql"
    echo "  Fedora: sudo dnf install postgresql-server"
    echo ""
    exit 1
fi

echo -e "${GREEN}✅ PostgreSQL found: $(psql --version)${NC}"
echo ""

# Check if PostgreSQL service is running
if ! pg_isready -h "$DB_HOST" -p "$DB_PORT" &> /dev/null; then
    echo -e "${YELLOW}⚠️  PostgreSQL service is not running${NC}"
    echo ""
    echo -e "${BLUE}Start PostgreSQL:${NC}"
    echo "  Ubuntu/Debian: sudo systemctl start postgresql"
    echo "  macOS: brew services start postgresql"
    echo ""
    read -p "Press Enter after starting PostgreSQL..."
fi

# Test connection
echo -e "${GREEN}🔍 Testing database connection...${NC}"
export PGPASSWORD="$DB_PASS"

if psql -h "$DB_HOST" -p "$DB_PORT" -U "$DB_USER" -d postgres -c '\q' 2>/dev/null; then
    echo -e "${GREEN}✅ Connected to PostgreSQL${NC}"
else
    echo -e "${RED}❌ Failed to connect to PostgreSQL${NC}"
    echo -e "${YELLOW}   Please check your credentials in .env${NC}"
    exit 1
fi

# Check if database exists
echo ""
echo -e "${GREEN}🔍 Checking if database exists...${NC}"
DB_EXISTS=$(psql -h "$DB_HOST" -p "$DB_PORT" -U "$DB_USER" -d postgres -tAc "SELECT 1 FROM pg_database WHERE datname='$DB_NAME'")

if [ "$DB_EXISTS" = "1" ]; then
    echo -e "${YELLOW}⚠️  Database '$DB_NAME' already exists${NC}"
    read -p "Do you want to drop and recreate it? (y/N): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        echo -e "${YELLOW}🗑️  Dropping database...${NC}"
        psql -h "$DB_HOST" -p "$DB_PORT" -U "$DB_USER" -d postgres -c "DROP DATABASE IF EXISTS $DB_NAME;" || exit 1
        echo -e "${GREEN}✅ Database dropped${NC}"
    else
        echo -e "${BLUE}Skipping database creation, will run migrations on existing database${NC}"
    fi
fi

# Create database if it doesn't exist
DB_EXISTS=$(psql -h "$DB_HOST" -p "$DB_PORT" -U "$DB_USER" -d postgres -tAc "SELECT 1 FROM pg_database WHERE datname='$DB_NAME'")
if [ "$DB_EXISTS" != "1" ]; then
    echo -e "${GREEN}📦 Creating database '$DB_NAME'...${NC}"
    psql -h "$DB_HOST" -p "$DB_PORT" -U "$DB_USER" -d postgres -c "CREATE DATABASE $DB_NAME;" || exit 1
    echo -e "${GREEN}✅ Database created${NC}"
fi

# Run SQL schema files
echo ""
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${BLUE}📋 Running SQL Schema Files${NC}"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""

SCHEMA_FILES=(
    "$PROJECT_ROOT/config/schema.sql"
    "$PROJECT_ROOT/config/footprint_schema.sql"
    "$PROJECT_ROOT/config/interview_schema.sql"
)

for schema_file in "${SCHEMA_FILES[@]}"; do
    if [ -f "$schema_file" ]; then
        schema_name=$(basename "$schema_file")
        echo -e "${GREEN}📄 Running $schema_name...${NC}"
        psql -h "$DB_HOST" -p "$DB_PORT" -U "$DB_USER" -d "$DB_NAME" -f "$schema_file"
        if [ $? -eq 0 ]; then
            echo -e "${GREEN}✅ $schema_name applied successfully${NC}"
        else
            echo -e "${RED}❌ Failed to apply $schema_name${NC}"
            exit 1
        fi
        echo ""
    else
        echo -e "${YELLOW}⚠️  Schema file not found: $schema_file${NC}"
    fi
done

# Run Python migration scripts (as backup/alternative)
echo ""
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${BLUE}🐍 Running Python Migrations${NC}"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""

# Activate virtual environment
if [ -d "$PROJECT_ROOT/venv" ]; then
    echo -e "${GREEN}📦 Activating virtual environment...${NC}"
    source "$PROJECT_ROOT/venv/bin/activate"
else
    echo -e "${YELLOW}⚠️  Virtual environment not found${NC}"
    echo -e "${YELLOW}   Run: ./install_dependencies.sh${NC}"
    exit 1
fi

# Set PYTHONPATH
export PYTHONPATH="$PROJECT_ROOT:$PROJECT_ROOT/backend:$PYTHONPATH"

MIGRATION_FILES=(
    "$PROJECT_ROOT/backend/migrations/create_resumes_table.py"
    "$PROJECT_ROOT/backend/migrations/create_jobs_table.py"
    "$PROJECT_ROOT/backend/migrations/create_interview_tables.py"
    "$PROJECT_ROOT/backend/migrations/create_footprint_tables.py"
)

for migration_file in "${MIGRATION_FILES[@]}"; do
    if [ -f "$migration_file" ]; then
        migration_name=$(basename "$migration_file")
        echo -e "${GREEN}🐍 Running $migration_name...${NC}"
        cd "$PROJECT_ROOT/backend/migrations"
        python "$migration_file"
        if [ $? -eq 0 ]; then
            echo -e "${GREEN}✅ $migration_name completed${NC}"
        else
            echo -e "${YELLOW}⚠️  $migration_name had issues (may be normal if tables exist)${NC}"
        fi
        echo ""
    fi
done

# Verify tables were created
echo ""
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${BLUE}🔍 Verifying Database Tables${NC}"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""

TABLES=$(psql -h "$DB_HOST" -p "$DB_PORT" -U "$DB_USER" -d "$DB_NAME" -tAc "
    SELECT tablename 
    FROM pg_tables 
    WHERE schemaname = 'public' 
    ORDER BY tablename;
")

if [ -n "$TABLES" ]; then
    echo -e "${GREEN}✅ Database tables created:${NC}"
    echo "$TABLES" | while read table; do
        echo "   • $table"
    done
else
    echo -e "${RED}❌ No tables found in database${NC}"
    exit 1
fi

# Get table counts
echo ""
echo -e "${GREEN}📊 Table Statistics:${NC}"
psql -h "$DB_HOST" -p "$DB_PORT" -U "$DB_USER" -d "$DB_NAME" -c "
    SELECT 
        schemaname,
        tablename,
        pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename)) AS size
    FROM pg_tables 
    WHERE schemaname = 'public'
    ORDER BY tablename;
"

echo ""
echo -e "${PURPLE}========================================${NC}"
echo -e "${GREEN}✅ Database Setup Complete!${NC}"
echo -e "${PURPLE}========================================${NC}"
echo ""
echo -e "${BLUE}📋 Database Information:${NC}"
echo -e "   Database: $DB_NAME"
echo -e "   Host: $DB_HOST:$DB_PORT"
echo -e "   User: $DB_USER"
echo ""
echo -e "${BLUE}🚀 Next Steps:${NC}"
echo -e "   1. Start backend: cd backend && ./start.sh"
echo -e "   2. Start frontend: cd frontend && npm run dev"
echo -e "   3. Access API docs: http://127.0.0.1:8000/docs"
echo ""
echo -e "${PURPLE}========================================${NC}"
echo ""

unset PGPASSWORD
