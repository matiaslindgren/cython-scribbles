from os import getenv

from hypothesis import settings, Verbosity

settings.register_profile("debug", max_examples=10, verbosity=Verbosity.verbose)
settings.register_profile("default", max_examples=100)
settings.register_profile("fuzz", max_examples=4000)
settings.load_profile(getenv("HYPOTHESIS_PROFILE", "default"))
