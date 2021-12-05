"""
Libreria di funzioni per lavorare con le immagini (ispirata a 2htdp/image in
Racket).
Contiene funzioni per:

- creare un'immagine vuota
- creare forme basilari (rettangolo, triangolo equilatero, cerchio, settore
  circolare, scena vuota);
- combinare immagini esistenti creandone di più complesse (sovrapponendole,
  affiancandole verticalmente o orizzontalmente, ruotandole);
- combinare immagini esistenti componendole arbitrariamente usando i loro
  punti di riferimento, che possono essere modificati;
- creare immagini contenenti testo;
- determinare larghezza e altezza di un'immagine;
- visualizzare un'immagine;
- creare una GIF animata usando una lista di immagini.

Versione 0.51
"""

from dataclasses import dataclass
from math import sqrt
from typing import Any, List, Optional, Tuple
from PIL import Image as ImageMod, ImageDraw, ImageFont as ImageFontMod
from PIL.Image import Image
from PIL.ImageFont import ImageFont


@dataclass
class Immagine:
    """
    Rappresenta un'immagine (con un punto di riferimento).

    Il punto di riferimento viene usato nelle operazioni di:

    - rotazione (per determinare il centro di rotazione)
    - composizione di due immagini, che vengono composte allineando i loro
      punti di riferimento.
    """
    img: Image
    punto_riferimento: Tuple[int, int]

    def _riferimento_default(self) -> Tuple[int, int]:
        # Il riferimento predefinito è al centro dell'immagine (approssimato al
        # pixel più vicino).
        return (round(larghezza_immagine(self) / 2),
                round(altezza_immagine(self) / 2))

    def __init__(self, img: Image, punto_rif=None) -> None:
        self.img = img
        self.punto_riferimento = punto_rif if punto_rif is not None \
            else self._riferimento_default()

    # Usiamo:
    # - metodi per funzioni "interne",
    # - funzioni "globali" per l'API pubblica.

    def get_image(self) -> Image:
        """
        Ritorna l'immagine Pillow.

        :returns: un'istanza della classe Image in Pillow
        :meta private:
        """
        return self.img

    def get_punto_riferimento(self) -> Tuple[int, int]:
        """
        Ritorna il punto di riferimento di questa immagine, come coppia di
        coordinate (x, y).

        :returns: punto di riferimento
        :meta private:
        """
        return self.punto_riferimento

    def is_immagine_vuota(self) -> bool:
        """
        Ritorna se questa immagine è vuota (dimensione 0 pixel per 0 pixel).

        :returns: True se l'immagine è vuota, False altrimenti
        :meta private:
        """
        return self.get_image().size == (0, 0)

    def ritaglia_bounding_box(self) -> "Immagine":
        """
        Ritaglia (crop) un'immagine in modo che sia grande il minimo necessario
        per contenere la sua bounding box. Questo ha l'effetto di eliminare
        eventuali bordi trasparenti.
        L'immagine risultante avrà il punto di riferimento nel centro
        dell'immagine ritagliata.

        :returns: una nuova immagine, ritagliata
        :meta private:
        """
        return Immagine(self.img.crop(self.img.getbbox()))

    def _key(self) -> Tuple[Any, ...]:
        """
        Ritorna i field importanti per __eq__ e __hash__ come tupla.

        La tupla risultante deve contenere valori confrontabili e hashabili,
        pertanto viene trattato con attenzione il caso dell'immagine vuota
        (su cui invocare .tobytes() genera un'eccezione).

        :returns: una tupla con i valori dei field importanti per determinare
                  l'uguaglianza
        """
        return (self.get_image().tobytes() if not self.is_immagine_vuota()
                else None,
                self.get_punto_riferimento())

    def __eq__(self, other: object) -> bool:
        """
        Confronta un'immagine con un'altra immagine.
        Due immagini sono considerate uguali se sono entrambe vuote oppure
        se hanno uguale contenuto e uguale punto di riferimento.

        :returns: True se le due immagini sono considerate uguali, False
        altrimenti
        """
        if not isinstance(other, type(self)):
            return NotImplemented
        return self._key() == other._key()

    def __hash__(self) -> int:
        """
        Calcola l'hash di questa immagine, sfruttando il metodo _key() e la
        funzione built-in hash().

        :returns l'hash per questa immagine
        """
        return hash(self._key())


def visualizza_immagine(immagine: Immagine):
    """
    Visualizza un'immagine a schermo (tranne quando è l'immagine vuota).

    :param immagine: l'immagine da visualizzare
    """
    if not immagine.is_immagine_vuota():
        immagine.get_image().show()


def crea_gif(nome_file: str, immagini: List[Immagine]):
    """
    Crea una GIF animata partendo da una lista di immagini e la memorizza come
    file.

    Le immagini verranno riprodotte in sequenza (25 frame per secondo) in loop.
    Le immagini con lo sfondo trasparente non sono supportate.

    :param nome_file: nome del file (senza estensione)
    :param immagini: lista di immagini da salvare come GIF
    """
    if len(immagini) == 0:
        raise ValueError("La lista delle immagini non può essere vuota")
    pil_imgs = list(map(Immagine.get_image, immagini))
    pil_imgs[0].save(f"{nome_file}.gif", save_all=True,
                     append_images=pil_imgs[1:],
                     duration=40,  # 40 ms per frame results in 25 fps
                     loop=0)   # loop 0 means "loop indefinitely"


def larghezza_immagine(immagine: Immagine) -> int:
    """
    Ritorna la larghezza di un'immagine in pixel.

    :param img: immagine di cui si vuole sapere la larghezza
    :returns: la largheza dell'immagine in pixel
    """
    return immagine.get_image().width


def altezza_immagine(immagine: Immagine) -> int:
    """
    Ritorna l'altezza di un'immagine in pixel.

    :param img: immagine di cui si vuole sapere l'altezza
    :returns: l'altezza dell'immagine in pixel
    """
    return immagine.get_image().height


def rettangolo(larghezza: int, altezza: int,
               colore_riempimento: str) -> Immagine:
    """
    Crea un rettangolo delle dimensioni indicate, riempito con un colore.

    :param larghezza: larghezza del rettangolo in pixel
    :param altezza: altezza del rettangolo in pixel
    :param colore_riempimento: stringa che indica il colore con cui riempire il
                               rettangolo
    :returns: un'immagine contenente il rettangolo
    """
    _valida_dimensione(larghezza)
    _valida_dimensione(altezza)
    return Immagine(ImageMod.new(_IMAGE_MODE, (larghezza, altezza),
                                 colore_riempimento))


def cambia_punto_riferimento(immagine: Immagine, punto_orizzontale: str,
                             punto_verticale: str) -> Immagine:
    """
    Cambia il punto di riferimento di un'immagine, ritornando un'immagine
    con lo stesso contenuto ma con un nuovo punto di riferimento.

    La posizione del nuovo punto di riferimento è determinata dai parametri
    punto_orizzontale e punto_verticale.

    :param immagine: immagine originale
    :param punto_orizzontale: "left", "middle" o "right" per indicare
           rispettivamente sinistra, centro o destra
    :param punto_verticale: "top", "middle" o "bottom" per indicare
           rispettivamente in alto, centro o in basso
    :returns: un'immagine con il nuovo punto di riferimento
    """
    x_mapping = {
        "left": 0,
        "middle": round(larghezza_immagine(immagine) / 2),
        "right": larghezza_immagine(immagine)
    }
    y_mapping = {
        "top": 0,
        "middle": round(altezza_immagine(immagine) / 2),
        "bottom": altezza_immagine(immagine)
    }
    return Immagine(immagine.get_image(), (x_mapping[punto_orizzontale],
                                           y_mapping[punto_verticale]))


def affianca(img_sinistra: Immagine, img_destra: Immagine) -> Immagine:
    """
    Affianca due immagini in orizzontale, posizionandole nell'immagine
    risultante una a sinistra e una a destra.
    Le immagini vengono allineate lungo i loro centri.

    :param img_sinistra: immagine da posizionare a sinistra
    :param img_destra: immagine da posizionare a destra
    :returns: un'immagine composta dalle due immagini affiancate
    """
    return componi(cambia_punto_riferimento(img_sinistra, "right", "middle"),
                   cambia_punto_riferimento(img_destra, "left", "middle"))


def affianca_verticale(img_sopra: Immagine, img_sotto: Immagine) -> Immagine:
    """
    Affianca due immagini in verticale, posizionandole nell'immagine
    risultante una sopra e una sotto.
    Le immagini vengono allineate lungo i loro centri.

    :param img_sopra: immagine da posizionare sopra
    :param img_sotto: immagine da posizionare sotto
    :returns: un'immagine composta dalle due immagini affiancate in verticale
    """
    return componi(cambia_punto_riferimento(img_sopra, "middle", "bottom"),
                   cambia_punto_riferimento(img_sotto, "middle", "top"))


def ruota(immagine: Immagine, gradi: int) -> Immagine:
    """
    Ruota un'immagine del numero di gradi specificato in senso antiorario
    attorno al suo punto di riferimento.
    Il punto di riferimento dell'immagine risultante sarà al centro di
    quest'ultima.

    :param img: immagine da ruotare
    :param gradi: numero di gradi con cui l'immagine deve essere ruotata
    :returns: un'immagine come quella fornita, ruotata
    """
    img = immagine.get_image()
    # Quando la rotazione non è attorno al centro, Pillow non gestisce
    # correttamente l'espansione dell'immagine. Per aggirare questa
    # limitazione, riposizioniamo l'immagine su un rettangolo trasparente in
    # modo che il punto di riferimento dell'immagine di cui stiamo eseguendo la
    # rotazione si trovi al centro del rettangolo.
    rif = immagine.get_punto_riferimento()
    altezza = altezza_immagine(immagine)
    larghezza = larghezza_immagine(immagine)
    extra_top = max(0, altezza - 2 * rif[1])
    extra_bottom = max(0, 2 * rif[1] - altezza)
    extra_left = max(0, larghezza - 2 * rif[0])
    extra_right = max(0, 2 * rif[0] - larghezza)
    img_centrata = ImageMod.new(_IMAGE_MODE,
                                (larghezza + extra_left + extra_right,
                                 altezza + extra_top + extra_bottom),
                                _TRANSPARENT_COLOR)
    img_centrata.paste(img, (extra_left, extra_top))
    ruotata = Immagine(img_centrata.rotate(gradi, expand=True,
                                           fillcolor=_TRANSPARENT_COLOR))
    # Quando l'immagine (rettangolare) viene ruotata di un numero di gradi non
    # multiplo di 90, l'immagine ruotata viene espansa per accomodare la
    # rotazione dell'intero rettangolo. Solo nel caso in cui l'immagine
    # risultante diventa più grande di quella originale (in almeno una
    # dimensione), eliminiamo l'area trasparente ritagliando l'immagine.
    espansa = larghezza_immagine(ruotata) > img.width or \
        altezza_immagine(ruotata) > img.height
    return ruotata.ritaglia_bounding_box() if espansa else ruotata


def sovrapponi(img_primopiano: Immagine,
               img_secondopiano: Immagine) -> Immagine:
    """
    Sovrappone due immagini una sopra l'altra, sovraimponendo la prima sulla
    seconda.
    Le immagini vengono sovrapposte usando i rispettivi centri.

    :param img_primopiano: immagine da mettere in primo piano
    :param img_secondopiano: immagine da mettere in secondo piano
    :returns: un'immagine contenente le due immagini fornite sovrapposte
    """
    return componi(
        cambia_punto_riferimento(img_primopiano, "middle", "middle"),
        cambia_punto_riferimento(img_secondopiano, "middle", "middle"))


def componi(img_pp: Immagine, img_sp: Immagine) -> Immagine:
    """
    Compone due immagini (tenendo la prima in primo piano e la seconda in
    secondo piano), allineando i rispettivi punti di riferimento.

    Tale punto di riferimento diventa anche il punto di riferimento
    dell'immagine risultante.

    :param img_primopiano: immagine da mettere in primo piano
    :param img_secondopiano: immagine da mettere in secondo piano
    :returns: un'immagine composta con le due immagini fornite
    """
    img_pp_rif = img_pp.get_punto_riferimento()
    img_sp_rif = img_sp.get_punto_riferimento()
    sopra = max(img_pp_rif[1],
                img_sp_rif[1])
    sotto = max(altezza_immagine(img_pp) - img_pp_rif[1],
                altezza_immagine(img_sp) - img_sp_rif[1])
    sinistra = max(img_pp.get_punto_riferimento()[0],
                   img_sp.get_punto_riferimento()[0])
    destra = max(larghezza_immagine(img_pp) - img_pp_rif[0],
                 larghezza_immagine(img_sp) - img_sp_rif[0])
    img_ris = ImageMod.new(_IMAGE_MODE, (sinistra + destra, sopra + sotto),
                           _TRANSPARENT_COLOR)
    img_ris.paste(img_sp.get_image(),
                  (sinistra - img_sp_rif[0],
                   sopra - img_sp_rif[1]))
    img_ris.alpha_composite(img_pp.get_image(),
                            (sinistra - img_pp_rif[0],
                             sopra - img_pp_rif[1]))
    return Immagine(img_ris, (sinistra, sopra))


def immagine_vuota() -> Immagine:
    """
    Crea un'immagine vuota.
    Quando l'immagine vuota viene composta con un'altra immagine, si comporta
    da elemento neutro.
    Un'immagine vuota non può essere visualizzata.

    :returns: un'immagine vuota di larghezza e altezza 0 pixel.
    """
    return Immagine(ImageMod.new(_IMAGE_MODE, (0, 0)))


def scena_vuota(larghezza: int, altezza: int) -> Immagine:
    """
    Crea un'immagine trasparente delle dimensioni indicate.

    :param larghezza: larghezza dell'immagine in pixel
    :param altezza: altezza dell'immagine in pixel
    :returns: un'immagine trasparente delle dimensioni specificate
    """
    _valida_dimensione(larghezza)
    _valida_dimensione(altezza)
    return Immagine(ImageMod.new(_IMAGE_MODE, (larghezza, altezza),
                                 _TRANSPARENT_COLOR))


def testo(contenuto: str, punti: int, colore: str) -> Immagine:
    """
    Crea un'immagine con il testo indicato visualizzato usando il font Arial
    alla dimensione e con il colore specificati.
    Quando il font Arial non è disponibile, viene usato un font di base sempre
    disponibile.
    L'immagine risultante ha le dimensioni minime per contenere il testo da
    visualizzare in base alla dimensione richiesta.

    :param contenuto: testo da visualizzare
    :param punti: dimensione del testo (ad esempio, 12)
    :param colore: colore per il testo
    :returns: un'immagine con il testo
    """
    lista_font = ["arial.ttf", "Arial.ttf"]
    i = 0
    font = None
    while i < len(lista_font) and font is None:
        font = _ottieni_font_se_disponibile(lista_font[i], punti)
        i += 1
    if font is None:
        font = ImageFontMod.load_default()
    img = ImageMod.new(_IMAGE_MODE, font.getsize(contenuto))
    draw = ImageDraw.Draw(img)
    draw.text((0, 0), contenuto, fill=colore, font=font)
    return Immagine(img)


def cerchio(raggio: int, colore_riempimento: str) -> Immagine:
    """
    Crea un cerchio avente il raggio indicato, riempito con un colore.

    :param raggio: raggio del cerchio in pixel
    :param colore_riempimento: stringa che indica il colore con cui riempire il
                               cerchio
    :returns: un'immagine contenente il cerchio
    """
    _valida_dimensione(raggio)
    lato = raggio * 2
    img = ImageMod.new(_IMAGE_MODE, (lato, lato), _TRANSPARENT_COLOR)
    draw = ImageDraw.Draw(img)
    draw.ellipse([(0, 0), img.size], fill=colore_riempimento)
    return Immagine(img)


def settore_circolare(raggio: int, angolo: int,
                      colore_riempimento: str) -> Immagine:
    """
    Crea un settore circolare appartenente a un cerchio del raggio indicato,
    riempito con un colore.
    Un settore circolare è una porzione di cerchio racchiusa tra due raggi e un
    arco.
    Considerando il cerchio come un orologio, il primo raggio punta nella
    direzione delle 3. L'angolo determina la posizione del secondo raggio,
    calcolata a partire dal primo raggio procedendo in senso orario.
    Quando l'angolo è 360 gradi, il settore circolare diventa a tutti gli
    effetti un cerchio.

    :param raggio: raggio del cerchio che racchiude il settore circolare
    :param angolo: angolo al centro del settore circolare
    :param colore_riempimento: stringa che indica il colore con cui riempire il
                               settore circolare
    :returns: un'immagine contenente il settore circolare
    """
    _valida_dimensione(raggio)
    lato = raggio * 2
    img = ImageMod.new(_IMAGE_MODE, (lato, lato), _TRANSPARENT_COLOR)
    draw = ImageDraw.Draw(img)
    draw.pieslice([(0, 0), img.size], 0, angolo, fill=colore_riempimento)
    return Immagine(img).ritaglia_bounding_box()


def triangolo(lato: int, colore_riempimento: str) -> Immagine:
    """
    Crea un triangolo equilatero con la punta verso l'alto avente il lato
    indicato, riempito con un colore.

    :param lato: lato del triangolo equilatero in pixel
    :param colore_riempimento: stringa che indica il colore con cui riempire il
                               triangolo
    :returns: un'immagine contenente il triangolo equilatero
    """
    _valida_dimensione(lato)
    altezza = round(lato * sqrt(3) / 2)
    img = ImageMod.new(_IMAGE_MODE, (lato, altezza), _TRANSPARENT_COLOR)
    draw = ImageDraw.Draw(img)
    p_sottosx = (0, altezza)
    p_alto = (round(lato / 2), 0)
    p_sottodx = (lato, altezza)
    draw.polygon([p_sottosx, p_alto, p_sottodx], fill=colore_riempimento)
    return Immagine(img)


# ======================================== #
# Costanti
# ======================================== #


_IMAGE_MODE = "RGBA"  # RGB + canale Alpha
_TRANSPARENT_COLOR = (0, 0, 0, 0)  # Canale Alpha completamente trasparente

# ======================================== #
# Funzioni ausiliarie
# ======================================== #


def _ottieni_font_se_disponibile(nome: str, punti: int) -> Optional[ImageFont]:
    """
    Prova ad ottenere il font con il nome indicato alla dimensione richiesta.

    :param nome: nome del font, inclusa l'estensione, come "arial.ttf"
    :param punti: dimensione del font
    :returns: il font se è disponibile, altrimenti None
    """
    try:
        return ImageFontMod.truetype(nome, size=punti)
    except OSError:
        return None


def _valida_dimensione(valore: int):
    """
    Solleva un'eccezione quando il valore fornito non è valido per una
    dimensione in pixel, essendo negativo oppure uguale a zero.

    :param valore: il valore in pixel da controllare
    """
    if valore <= 0:
        raise ValueError("Dimensione non valida "
                         "(deve essere un numero positivo)")
