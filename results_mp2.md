## Parallellized Mandebrot Set Computation Times (L04)
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

## Chunk Sweeping Optimization (L05)
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

## Full Performance Comparison at 1024x1024, max_iter=100
```bash
| Implementation | Time (s) | Speedup |
|----------------|----------|---------|
Naive Python     4.0889 s,   speedup=1.00x
Numpy Vectorized 0.9811 s,   speedup=4.17x
Numba (@njit)    0.0620 s,   speedup=65.95x
Multiprocessing  0.0145 s,   speedup=281.99x
Dask(6 workers, 32 chunks) 0.1276 s, speedup=32.04x
Dask(6 workers, 12 chunks) 0.0780 s, speedup=52.42x
```

## Discussion
**Speedup vs core-count**\
Using Amdahl back-solving at p=7, the original worker-only version with a speedup of 2.29x gives an implied serial fraction of s=0.343. With chunking enabled at 7 workers and 42 chunks, the speedup increases to 4.15x, which lowers the implied serial fraction to s=0.114. This indicated that the chunking strategy substantially improved load balance and reduced the apparent serial/overhead component of the parallel execution.

**What settings give the best time:**\
I tested both 7 and 8 workers, and found that 7 workers with 42 chunks (6x workers) gave the best performance in terms of efficiency and LIF, while 8 workers with 48 chunks (6x workers) performed the fastest, with a speedup of 4.29x and efficiency of 53.6%, and a LiF of 0.866.

**Is parallelisation worth it on your hardware:**\
Yes, the parallelized version with optimized chunking, njit compilation, and multiprocessing achieved a significant speedup of up to 281.99x compared to the naive Python implementation, making it well worth the effort on my hardware. This is also compared to the Numba-optimized single-threaded version, which was already much faster than the naive implementation, but the parallelized version still provided a substantial improvement.

## L06: Dask Best Performance

```bash
Serial baseline T1: 0.0670 s

n_chunks | time (s) | vs 1x | speedup | LIF
----------------------------------------------
       6 |   0.1052 |  1.57x |    0.64x | 8.423
      12 |   0.0780 |  1.16x |    0.86x | 5.982
      24 |   0.0885 |  1.32x |    0.76x | 6.926
      36 |   0.1319 |  1.97x |    0.51x | 10.819
      48 |   0.1564 |  2.33x |    0.43x | 13.008
      96 |   0.2489 |  3.72x |    0.27x | 21.293

Record:
n_chunks_optimal = 12
t_min            = 0.0780 s
LIF_min          = 5.982
checksum(best)   = 22018211
```

# Discussion
**How does Dask local compare to multiprocessing at the same worker count?**\
Dask is significantly slower than multiprocessing. This is indicated by the best Dask time of 0.0780 s with 12 chunks, which is still much slower than the multiprocessing time of 0.0145 s. The overhead of Dask's task scheduling and communication between workers likely contributes to this performance gap, especially for a workload that may not be large enough to overrun these costs.

**What does the overhead difference tell you about when to choose each tool?**\
The overhead difference suggests that multiprocessing is more suitable for workloads that require low-latency execution and have a smaller number of tasks, while Dask may be more appropriate for larger, more complex workloads that can benefit from its dynamic task scheduling and distributed computing capabilities. For smaller tasks or those with tight performance requirements, multiprocessing may be the better choice due to its lower overhead.