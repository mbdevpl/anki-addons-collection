import os
# import pathlib
import sys

from anki import version as anki_version
anki_version = tuple([int(_) for _ in anki_version.split('.')])

if anki_version[:2] >= (2, 1):
    sys.path.append(os.path.join(os.path.dirname(__file__), 'night_mode'))
    # sys.path.append(pathlib.Path(__file__).parent.joinpath('night_mode'))

    import night_mode
else:
    sys.path.append(os.path.join(os.path.dirname(__file__), 'night_mode_legacy'))
    # sys.path.append(pathlib.Path(__file__).parent.joinpath('night_mode_legacy'))

    import Night_Mode
