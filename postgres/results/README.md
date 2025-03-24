# Benchmark Report

> Benchmarked on Intel_R Core_TM i5-7400T (4) @ 3.00 GHz

## Index

- pool size = 4
- pool size = 8
- pool size = 16

## Result

> PostgreSQL Total Query Time Benchmark

### pool size = 4

| workers = 4 | workers = 16 | workers = 64 |
| ----------- | ------------ | ------------ |
| ![p04_w04]  | ![p04_w16]   | ![p04_w64]   |

### pool size = 8

| workers = 4 | workers = 16 | workers = 64 |
| ----------- | ------------ | ------------ |
| ![p08_w04]  | ![p08_w16]   | ![p08_w64]   |

### pool size = 16

| workers = 4 | workers = 16 | workers = 64 |
| ----------- | ------------ | ------------ |
| ![p16_w04]  | ![p16_w16]   | ![p16_w64]   |

[p04_w04]: /postgres/results/benchmark_p04_w004.svg
[p04_w16]: /postgres/results/benchmark_p04_w016.svg
[p04_w64]: /postgres/results/benchmark_p04_w064.svg
[p08_w04]: /postgres/results/benchmark_p08_w004.svg
[p08_w16]: /postgres/results/benchmark_p08_w016.svg
[p08_w64]: /postgres/results/benchmark_p08_w064.svg
[p16_w04]: /postgres/results/benchmark_p16_w004.svg
[p16_w16]: /postgres/results/benchmark_p16_w016.svg
[p16_w64]: /postgres/results/benchmark_p16_w064.svg
