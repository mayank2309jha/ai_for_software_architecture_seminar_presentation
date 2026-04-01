#!/bin/sh

# Use 'seq' to generate the numbers 1 through 20
for i in $(seq 1 20)
do
  curl -X POST http://localhost:3000/task \
  -H "Content-Type: application/json" \
  -d "{\"num\": $i}" &
done

# Wait for all background processes to finish
wait
echo "All tasks submitted."