import sys
from PIL.Image import Image
from img_lib_v0_51 import (
    triangolo,
    testo,
    rettangolo,
    affianca,
    immagine_vuota,
    larghezza_immagine)


def controlla_valore_atteso(valore, valore_atteso):
    if valore != valore_atteso:
        print("Test fallito! Il valore attuale", valore, "differisce dal valore atteso", valore_atteso,
              file=sys.stderr)
    # else:
    #     print("Test passato")


def affianca_molte(immagini: list) -> Image:
    """
    Affianca le immagini elencate all'interno di una lista.

    :param immagini: lista di immagini

    :returns: un'immagine composta da varie immagini affiancate
    """
    affiancate = immagine_vuota()
    for immagine in immagini:
        affiancate = affianca(affiancate, immagine)
    return affiancate
