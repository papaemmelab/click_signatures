"""
Module that contains the command line app.

Why does this file exist, and why not put this in __main__?
You might be tempted to import things from __main__ later, but that will
cause problems, the code will get executed twice:

    - When you run `python -m click_signatures` python will execute
      `__main__.py` as a script. That means there won't be any
      `click_signatures.__main__` in `sys.modules`.

    - When you import __main__ it will get executed again (as a module) because
      there's no `click_signatures.__main__` in `sys.modules`.

Also see (1) from http://click.pocoo.org/5/setuptools/#setuptools-integration
"""

from click_signatures.commands import mutationalpatterns as main


if __name__ == "__main__":
    main()  # pylint: disable=no-value-for-parameter
