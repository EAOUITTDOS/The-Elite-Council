#!/bin/bash

# Clone all 62 repos
echo "Cloning all 62 repositories..."
python -c "from elite_council_loader import EliteCouncilLoader; EliteCouncilLoader()._clone_all()"

# Build index
echo "Building code index from all 62 repos..."
python -c "from elite_council_loader import EliteCouncil; EliteCouncil()"

# Start server
echo "Starting Elite Council API..."
uvicorn fastapi_server_elite:app --host 0.0.0.0 --port 8000 --workers 4
