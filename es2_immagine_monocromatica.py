"""
Il file contiene funzioni per:
- creare quadrati di colore monocromatico
- costruire stringhe che rappresentano colori monocromatici
- costruire immagini composte da quadrati di colore monocromatico
"""

from sys import float_repr_style
from lib.img_lib_v0_51 import affianca_verticale, altezza_immagine, immagine_vuota, larghezza_immagine, sovrapponi, rettangolo, Immagine, visualizza_immagine
from lib.testing_util import affianca_molte, controlla_valore_atteso
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
    [192, 255, 255],
    [255, 0, 255],
    [255, 255, 255]
]


def colore_monocromatico(pixel: int) -> str:
    """
    Funzione che restituisce una stringa che rappresenta la tonalita' di colore monocromatica
    
    param: un numero intero tra 0 e 255 corrispondente all'intensita di colore monocromatico
    returns: una stringa rappresentate l'intensità di rosso, verde e blu
    """
    tonalita = str(pixel)
    colore = "rgb("+tonalita+","+tonalita+","+tonalita+")"
    return colore        


# Test
controlla_valore_atteso(colore_monocromatico(0), "rgb(0,0,0)")
controlla_valore_atteso(colore_monocromatico(57), "rgb(57,57,57)")
controlla_valore_atteso(colore_monocromatico(255), "rgb(255,255,255)")


def render_bitmap_monocromatico(bitmap: List[List[int]]) -> Immagine:
    """
    Funzione che restituisce una immagine composta da quadrati monocromatici affiancati orizzontalmente e verticalmente
    
    param bitmap: Una lista contenente una seconda lista composta dai numeri interi tra 0 e 255
    returns: una immagine composta da quadrati monocromatici affiancati orizzontalmente e verticalmente
    """
    riga_prec = immagine_vuota()
    for riga in bitmap:
        lista_immagini = [
            render_pixel(colore_monocromatico(pixel))
            for pixel in riga
            ]
        composizione_riga = affianca_molte(lista_immagini)
        composizione_immagine = affianca_verticale(riga_prec, composizione_riga)
        riga_prec = composizione_immagine
    return composizione_immagine


# Test
controlla_valore_atteso(larghezza_immagine(render_bitmap_monocromatico([[0, 0, 0], [0, 0, 0]])), (PIXEL_SIZE + 2)* 3)
controlla_valore_atteso(altezza_immagine(render_bitmap_monocromatico([[0, 0, 0], [0, 0, 0]])), (PIXEL_SIZE + 2)* 2) 
controlla_valore_atteso(larghezza_immagine(render_bitmap_monocromatico([[0, 0, 0]])), (PIXEL_SIZE + 2)* 3)
controlla_valore_atteso(altezza_immagine(render_bitmap_monocromatico([[0, 0, 0]])), PIXEL_SIZE + 2 )
controlla_valore_atteso(altezza_immagine(render_bitmap_monocromatico([[]])), 0)


#visualizza_immagine(render_bitmap_monocromatico(bitmap_monocromatico))