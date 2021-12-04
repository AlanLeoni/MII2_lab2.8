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
    

#controlla_valore_atteso(larghezza_immagine(render_pixel("rgb(255,0,0)")), PIXEL_SIZE + 2)
#controlla_valore_atteso(altezza_immagine(render_pixel("rgb(255,0,0)")), PIXEL_SIZE + 2)

# Mappa di pixel booleani (bianco == True, nero == False)
bitmap_bianco_nero = [
    [True, True, True],
    [True, False, True],
    [True, True, True]
]


def colore_bianco_nero(pixel: bool) -> str:
    bianco = "rgb(255, 255, 255)"
    nero = "rgb(0, 0, 0)"
    if pixel == True:
        return bianco
    else:
        return nero
        
def render_bitmap_bianco_nero(bitmap: List[List[bool]]) -> Immagine:
    riga_prec = immagine_vuota()
    for riga in bitmap_bianco_nero:
        lista_immagini = [
            render_pixel(colore_bianco_nero(pixel))
            for pixel in riga
            ]
        composizione_riga = affianca_molte(lista_immagini)
        composizione_immagine = affianca_verticale(riga_prec, composizione_riga)
        riga_prec = composizione_immagine

    return composizione_immagine

visualizza_immagine(render_bitmap_bianco_nero(bitmap_bianco_nero))

# def render_bitmap_bianco_nero(bitmap: List[List[bool]]) -> Immagine:
#     riga_prec = immagine_vuota()
#     riga = immagine_vuota()
#     for lista in bitmap:
#         composizione =affianca_verticale(riga_prec, riga)
#         riga_prec = composizione
#         # costruisco la lista di immagini a partire dai True e False
#         lista_immagini = [
#             render_pixel(elemento)
#             for elemento in lista
#             ]
#         affianca_molte(lista_immagini)
#     return composizione
# visualizza_immagine(render_bitmap_bianco_nero(bitmap_bianco_nero))