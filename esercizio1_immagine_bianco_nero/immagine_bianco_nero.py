from img_lib_v0_51 import altezza_immagine, larghezza_immagine, sovrapponi, rettangolo, Immagine
from testing_util import controlla_valore_atteso
from typing import List

PIXEL_SIZE = 100

def render_pixel(colore: str) -> Immagine:
    """
    Crea un'immagine che rappresenta un pixel di un certo colore,
    con attorno un bordo di 2 pixel grigio.

    :param colore: colore di riempimento dell'immagine
    :returns: un'immagine rappresentante un pixel colorato
     """ 
    return sovrapponi(
        rettangolo(PIXEL_SIZE, PIXEL_SIZE, colore),
        rettangolo(PIXEL_SIZE + 2, PIXEL_SIZE + 2, "grey"))

controlla_valore_atteso(larghezza_immagine(render_pixel("rgb(255,0,0)")), PIXEL_SIZE + 2)
controlla_valore_atteso(altezza_immagine(render_pixel("rgb(255,0,0)")), PIXEL_SIZE + 2)

# Mappa di pixel booleani (bianco == True, nero == False)
bitmap_bianco_nero = [
    [True, True, True],
    [True, False, True],
    [True, True, True]
]


def colore_bianco_nero(pixel: bool) -> str:
    pass

def render_bitmap_bianco_nero(bitmap: List[List[bool]]) -> Immagine:
    pass