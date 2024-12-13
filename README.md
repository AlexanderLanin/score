# Score Platform

## Building

### Supported environment
The build currently supports Linux environments.

### Use bazelisk for bazel version management
Follow [instructions](https://github.com/bazelbuild/bazelisk) and setup bazelisk to manage your bazel version based on the .bazelversion file.

### Check and fix formatting
```
$ bazel test //:format.check
$ bazel run //:format.fix
```

## Documentation

Use //docs:docs target to build the documentation.
```
$ bazel build //docs:docs
```

The output directory can be found under ```bazel-bin/docs/docs/_build/html```.

If you need to update pip dependencies, after modifying the requirements file, regenerate the lock file:
```
bazel run //docs:requirements.update
```

To update all existing dependencies, run:
```
bazel run //docs:requirements.update -- --upgrade
```

For more detailed usage instructions, common use cases, FAQ, and known issues & solutions, please refer to the [Documentation Usage Guide](docs/tutorials/docs.rst).

### Alternative incremental build

While the above command is the most straightforward and official way to build the documentation,
it can be slow, especially if you have many minor changes to the documentation and want to see the
result quickly.
The generated output will be in the _build directory.

```sh
bazel run //docs:incremental
```

### IDE integration

For your IDE to support you with documentation, you need to run the following command.

After doing so and installing the recommended esbonio extension, you should have e.g. a preview
available when you edit a `.rst` file (VS Code only). When doing this the first time, you may need
to restart your IDE.

For python to detect datatypes in documentation-related `.py` files, you may need to point your
IDE to the generated virtual environment at `.venv_docs`.

You need to re-run this command, when any dependencies
including our own extensions (metamodel, warnings, ...) change.

```sh
bazel run //docs:ide_support
```
