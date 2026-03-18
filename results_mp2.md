## Parallellized Mandebrot Set Computation Times
```bash
| Workers | Time (s) | Speedup | Efficiency (%) |
|---------|----------|---------|----------------|
1 workers: 0.0712 s, speedup=1.00x, efficiency=100.0%
2 workers: 0.0407 s, speedup=1.75x, efficiency=87.5%
3 workers: 0.0544 s, speedup=1.31x, efficiency=43.6%
4 workers: 0.0448 s, speedup=1.59x, efficiency=39.7%
5 workers: 0.0425 s, speedup=1.68x, efficiency=33.5%
6 workers: 0.0394 s, speedup=1.81x, efficiency=30.1%
7 workers: 0.0311 s, speedup=2.29x, efficiency=32.7%
8 workers: 0.0328 s, speedup=2.17x, efficiency=27.2%
```

## Chunk Sweeping Optimization
**8 Workers:**
```bash
Serial: 0.0620 s

| Chunks | Time (s) | Speedup | Efficiency (%) | LIF |
|--------|----------|---------|----------------|-----|
   8 chunks ( 1x workers): 0.0256 s, speedup=2.42x, efficiency=30.3%, LIF=2.302
  16 chunks ( 2x workers): 0.0157 s, speedup=3.95x, efficiency=49.4%, LIF=1.025
  32 chunks ( 4x workers): 0.0163 s, speedup=3.81x, efficiency=47.6%, LIF=1.102
  48 chunks ( 6x workers): 0.0145 s, speedup=4.29x, efficiency=53.6%, LIF=0.866
  64 chunks ( 8x workers): 0.0161 s, speedup=3.86x, efficiency=48.2%, LIF=1.075
 128 chunks (16x workers): 0.0178 s, speedup=3.48x, efficiency=43.5%, LIF=1.300
```

**7 Workers:**
```bash
Serial: 0.0619 s

| Chunks | Time (s) | Speedup | Efficiency (%) | LIF |
|--------|----------|---------|----------------|-----|
   7 chunks ( 1x workers): 0.0297 s, speedup=2.09x, efficiency=29.8%, LIF=2.353
  14 chunks ( 2x workers): 0.0179 s, speedup=3.47x, efficiency=49.5%, LIF=1.019
  28 chunks ( 4x workers): 0.0171 s, speedup=3.63x, efficiency=51.8%, LIF=0.931
  42 chunks ( 6x workers): 0.0149 s, speedup=4.15x, efficiency=59.3%, LIF=0.687
  56 chunks ( 8x workers): 0.0152 s, speedup=4.07x, efficiency=58.1%, LIF=0.722
 112 chunks (16x workers): 0.0159 s, speedup=3.89x, efficiency=55.5%, LIF=0.801
```