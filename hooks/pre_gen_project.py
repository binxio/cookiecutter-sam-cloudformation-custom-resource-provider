import re
import sys


if not re.match(r'^[_a-zA-Z][\-_a-zA-Z0-9]+$', '{{ cookiecutter.project_name }}'):
    print("ERROR: invalid project name. Must start with a letter followed by letter, digits, underscores or dashs")
    sys.exit(1)
