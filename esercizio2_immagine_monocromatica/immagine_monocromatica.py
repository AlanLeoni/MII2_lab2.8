from sys import float_repr_style
from img_lib_v0_51 import affianca_verticale, altezza_immagine, immagine_vuota, larghezza_immagine, sovrapponi, rettangolo, Immagine, visualizza_immagine
from testing_util import affianca_molte, controlla_valore_atteso
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
    
# Test
controlla_valore_atteso(larghezza_immagine(render_pixel("rgb(255,0,0)")), PIXEL_SIZE + 2)
controlla_valore_atteso(altezza_immagine(render_pixel("rgb(255,0,0)")), PIXEL_SIZE + 2)


# Mappa di pixel rappresentati come interi 0..255
bitmap_monocromatico = [
    [255, 255, 255],
    [255, 0, 255],
    [255, 255, 255]
]

def colore_monocromatico(pixel: int) -> str:
    pass
def render_bitmap_monocromatico(bitmap: List[List[int]]) -> Immagine:
    pass
