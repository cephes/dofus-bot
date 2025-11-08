#!/bin/bash
set -e

echo "Building retroproto porter..."
go build -o porter main.go

echo "Running porter..."
./porter

echo "Porter run complete."