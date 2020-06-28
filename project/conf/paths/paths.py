import operator
import os

from django.conf import settings

need = {
    "base-dir":
    {
        "orbita":
        [
            "templates",
            "authentication",
            "welcome",
            "project"
        ],
    },
}

def directority(needs, dirname=None, dirpath=None, orbita=None, intersec=None):

    if orbita and intersec is not None or not orbita == intersec:
        try:
            settings.__setattr__(
                dirname, 
                dirpath
            )
        except AttributeError:
            pass
    
    try:
        dirname = next(needs.__iter__()).upper().replace('-', '_')
    except StopIteration:
        return
    
    orbita = needs.pop(
        next(needs.__iter__())
    )["orbita"]

    dirpath = os.path.dirname(
        os.path.dirname(
            os.path.dirname(
                os.path.dirname( 
                    os.path.abspath(
                        __file__
                    )
                )
            )
        )
    )

    intersec = sorted(
        list(
            set(
                orbita
                ).intersection(
                set(
                    os.listdir(
                        dirpath
                    )
                )
            )
        )
    )

    directority(
        needs, 
        dirname, 
        dirpath, 
        orbita, 
        intersec
    )

def config():
    return directority(need)
