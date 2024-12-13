.. _Documentation_Usage:

Documentation Usage Guide
=========================

This guide provides detailed instructions for building and updating the documentation, common use cases, a FAQ section, and known issues & solutions.

Building Documentation
----------------------

To build the documentation, use the `//docs:docs` target with Bazel:

```sh
$ bazel build //docs:docs
```

The output directory can be found under `bazel-bin/docs/docs/_build/html`.

Updating Pip Dependencies
-------------------------

If you need to update pip dependencies, after modifying the requirements file, regenerate the lock file:

```sh
$ bazel run //docs:requirements.update
```

To update all existing dependencies, run:

```sh
$ bazel run //docs:requirements.update -- --upgrade
```

Incremental Build
-----------------

For a faster, incremental build, use the following command:

```sh
$ bazel run //docs:incremental
```

The generated output will be in the `_build` directory.

IDE Integration
---------------

For IDE support with documentation, run the following command:

```sh
$ bazel run //docs:ide_support
```

After doing so and installing the recommended esbonio extension, you should have a preview available when you edit a `.rst` file (VS Code only). When doing this the first time, you may need to restart your IDE.

For Python to detect datatypes in documentation-related `.py` files, you may need to point your IDE to the generated virtual environment at `.venv_docs`.

You need to re-run this command when any dependencies, including our own extensions (metamodel, warnings, etc.), change.

Common Use Cases
----------------

1. Building the documentation for the first time.
2. Updating documentation after making changes.
3. Running an incremental build for quick previews.
4. Integrating documentation support in your IDE.

FAQ
---

**Q: How do I build the documentation?**
A: Use the `//docs:docs` target with Bazel: `$ bazel build //docs:docs`.

**Q: Where can I find the output of the documentation build?**
A: The output directory can be found under `bazel-bin/docs/docs/_build/html`.

**Q: How do I update pip dependencies?**
A: After modifying the requirements file, regenerate the lock file with `$ bazel run //docs:requirements.update`. To update all existing dependencies, run `$ bazel run //docs:requirements.update -- --upgrade`.

**Q: How can I perform an incremental build?**
A: Use the command `$ bazel run //docs:incremental` for a faster, incremental build. The generated output will be in the `_build` directory.

**Q: How do I integrate documentation support in my IDE?**
A: Run the command `$ bazel run //docs:ide_support` and install the recommended esbonio extension. You may need to restart your IDE for the changes to take effect.

Known Issues & Solutions
------------------------

1. **Issue:** Slow documentation build times.
   **Solution:** Use the incremental build command `$ bazel run //docs:incremental` for faster builds.

2. **Issue:** IDE not detecting documentation-related datatypes.
   **Solution:** Point your IDE to the generated virtual environment at `.venv_docs` and restart your IDE.

3. **Issue:** Changes to dependencies not reflected in the documentation build.
   **Solution:** Re-run the command `$ bazel run //docs:ide_support` when any dependencies, including our own extensions, change.
