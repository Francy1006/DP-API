#!/bin/sh

set -e

echo "1/2 Ejecutando tests y coverage..."
./scripts/coverage.sh

echo "2/2 Ejecutando SonarScanner..."
./scripts/sonar-scan.sh

echo "QA completado correctamente."