# Simulate-openfoam



#### Testing

```
bash run_tests.sh
```

The script will run all required docker containers (job manager, simulator) and run pytest from a third container.

To shortcut the build process (i.e. useful when running many tests during development), use

```
docker-compose -p simulate-test run test
```

