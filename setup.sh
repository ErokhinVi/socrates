#! /bin/bash

# colors
RED='\033[0;31m'
GREEN='\033[0;32m'
GRAY='\033[0;30m'
NC='\033[0m'

# python3 / python
PYTHON=""
echo -e "${GRAY}Checking if python3 or python is installed${NC}"
if command -v python3 &> /dev/null; then
    PYTHON="python3"
    echo -e "${GREEN}✅ python3${NC}"
elif command -v python &> /dev/null; then
    PYTHON="python"
    echo -e "${GREEN}✅ python${NC}"
else
    echo -e "${RED}❗️ Python is not installed${NC}"
    exit 1
fi

# Set up the environment
echo -e "${GRAY}Setting up .env${NC}"

if [ -f ".env" ]; then
    echo -e "${RED}❗️ .env already exists${NC}"
else
    cp .env.example .env && echo -e "${GREEN}✅ .env${NC}"
fi


# Create a virtual environment
echo -e "${GRAY}Creating .venv${NC}"

if [ -d ".venv" ]; then
    echo -e "${RED}❗️ .venv already exists${NC}"
else
    $PYTHON -m venv .venv && echo -e "${GREEN}✅ .venv${NC}"
fi


# Install the required packages
echo -e "${GRAY}Installing the required packages${NC}"

. .venv/bin/activate && echo -e "${GREEN}✅ .venv/bin/activate${NC}"
pip install -r requirements.txt && echo -e "${GREEN}✅ requirements.txt${NC}"



echo -e "${GRAY}\n--- --- --- --- ---\n${NC}"
echo -e "${GREEN}✅ Setup complete\n${NC}"%
