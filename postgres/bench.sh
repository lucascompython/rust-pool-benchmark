#!/bin/bash

BASE_DIR=$(pwd)

> ${BASE_DIR}/benchmark.txt

for dir in */; do
    if [ "$dir" != "results/" ]; then
        echo "Running benchmarks in ${dir}..."
        
        cd "$dir"

        cargo bench
        
        cd "$BASE_DIR"
    fi
done

find . -maxdepth 2 -name "*result.txt" -execdir cat {} \; > benchmark.txt

echo "Generating visualizations..."
python3 visualizer.py

echo "Benchmark complete. Results saved and visualizations generated."