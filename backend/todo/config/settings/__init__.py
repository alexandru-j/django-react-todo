from os import getenv

if getenv("BUILD"):
    from .prod import *  # noqa: F401, F403
else:
    from .dev import *  # noqa: F401, F403
