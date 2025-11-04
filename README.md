# glass-benchmarks

Benchmarks for [glass-dev/glass](https://github.com/glass-dev/glass).

## Running a benchmark

To run a benchmark, first install nox.

```sh
pip install nox
```

Then run the benchmark via nox.

```sh
nox -s benchmark -- <revision-you-wish-to-benchmark>
```

## Regression tests

The benchmarks can be used to run a regression test of `glass`. To do this
a nox test is provided in [noxfile.py](./noxfile.py). To run the test...

```sh
nox -s regression-tests -- <initial-state-revision> <revision-to-compare-to-initial-state>
```

If you want to compare to the initial state of main you can simply run.

```sh
nox -s regression-tests -- <revision-to-compare-to-main>
```
