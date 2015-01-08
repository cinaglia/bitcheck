import functools
import datetime


def measure(func):
    @functools.wraps(func)
    def measure(self, *args, **kwargs):
        # Skip measurement if verbosity is disabled
        if not self.args.get('--verbose'):
            return func(self, *args, **kwargs)

        # Calculate time and output
        start = datetime.datetime.now()
        print "Retrieving exchange // {} ..".format(func.__name__),
        output = func(self, *args, **kwargs)
        diff = (datetime.datetime.now() - start).total_seconds()
        print " took {} seconds".format(diff)

        return output
    return measure
