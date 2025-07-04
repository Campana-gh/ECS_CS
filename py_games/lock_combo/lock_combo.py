"""

Just an idea at this point -- 
Lock combination is a N digit number they have to guess. A hash to check if they got it right.
A more complex version is to do this with passwords.
"""

from collections.abc import Sequence

from absl import app


def main(argv: Sequence[str]) -> None:
  if len(argv) > 1:
    raise app.UsageError("Too many command-line arguments.")


if __name__ == "__main__":
  app.run(main)
