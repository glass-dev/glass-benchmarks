# glass-benchmarks

Benchmarks for [glass-dev/glass](https://github.com/glass-dev/glass).

## Running a benchmark

To run a benchmark, first install the dependencies.

```sh
pip install -e . git+https://github.com/glass-dev/glass@<revision-to-benchmark>
```

Then run via pytest.

```sh
pytest
```

If you want to save the output to a file...

```sh
pytest --benchmark-autosave
```

## Regression tests

The benchmarks can be used to run a regression test of `glass`. To do this
a nox test is provided in [noxfile.py](./noxfile.py). To run the test...

```sh
BEFORE_REVISION=<initial-state-revision> \
AFTER_REVISION=<revision-to-compare-to-initial-state> \
nox -s regression-tests
```

> Note: BEFORE_REVISION defaults to `main`
