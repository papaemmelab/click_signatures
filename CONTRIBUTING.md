# Contributing

Contributions are welcome, and they are greatly appreciated! Every
little bit helps, and credit will always be given.

This project could always use more documentation, whether as part of the
README, in docstrings, or even on the web in blog posts articles, and such.

Please learn about [`semantic versioning`][semver].

## Development

Set up for local development:

1. Clone your click_signatures locally:

    ```
    git clone git@github.com:leukgen/click_signatures.git
    ```

2. Use our commit message template:

    ```
    git config commit.template .gitmessage
    ```

3. Checkout to development branch:

    ```
    git checkout development
    git pull
    ```

4. Create a branch for local development:

    ```
    git checkout -b name-of-your-bugfix-or-feature
    ```

    Now you can make your changes locally.

5. To check pep8 formatting:

    ```
    pep8 --statistics --ignore=E701,E125 --hang-closing click_signatures
    ```

6. Run pylint:

    ```
    pylint click_signatures --rcfile=`pwd`/.pylintrc
    ```

7. Create a test in:

    ```
    click_signatures/tests
    ```

8. When you're done making changes, run:

    ```
    py.test -s -vv --cov=click_signatures tests
    ```

9. Commit your changes and push your branch to GitHub (see .gitmessage for types and emoji requirements):

    ```
    git add .
    git commit -m ":emoji: <type>: your meaningful description"
    git push origin name-of-your-bugfix-or-feature
    ```

9. Submit a pull request through the GitHub website.

## Bug reports, Feature requests and feedback

Go ahead and file an issue at https://github.com/leukgen/click_signatures/issues.

If you are proposing a **feature**:

* Explain in detail how it would work.
* Keep the scope as narrow as possible, to make it easier to implement.
* Remember that this is a volunteer-driven project, and that code contributions are welcome :)

When reporting a **bug** please include:

* Your operating system name and version.
* Any details about your local setup that might be helpful in troubleshooting.
* Detailed steps to reproduce the bug.

## Pull Request Guidelines

If you need some code review or feedback while you're developing the code just make the pull request.

For merging, you should:

1. Include passing tests (run `tox`).
2. Update documentation when there's new API, functionality etc.

<!-- References -->

[semver]: http://semver.org/
