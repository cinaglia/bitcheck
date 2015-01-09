from docopt import docopt
from .bitcheck import Bitcheck
from . import __doc__, __title__, __version__


def main():
    args = docopt(__doc__, version="{} {}".format(__title__, __version__))
    check = Bitcheck(args)
    check.run()

if __name__ == "__main__":
    main()
    