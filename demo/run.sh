#!/usr/bin/env bash

python3 scripts/run_pipeline.py --pseudo ../pseudo/Basic_intrinsics/Vector_arithmetic/vaddq_s8.pseudo --json ../advsimd.json --source test/test_vaddq_s8.c --exporter bin/FactExporter
