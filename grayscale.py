from pathlib import Path

import fitz  # PyMuPDF
from tqdm import tqdm


def convert_pdf_to_grayscale(input_pdf, output_pdf, dpi=200):
    """
    Convert a PDF file to grayscale using PyMuPDF (no Ghostscript).
    Renders pages at high DPI to avoid blurry text (still rasterized).
    input_pdf and output_pdf must be non-None.

    Args:
        input_pdf (str | Path): path to input PDF
        output_pdf (str | Path): path to output PDF
        dpi (int): render resolution; 300 is typical print quality, 600 is very
    sharp
    """
    if input_pdf is None or output_pdf is None:
        raise ValueError("input_pdf and output_pdf cannot be None")

    in_path = Path(input_pdf)
    out_path = Path(output_pdf)

    if not in_path.exists():
        raise FileNotFoundError(f"Input PDF not found: {in_path}")

    # Scale factor: PDF user space = 72 DPI
    zoom = dpi / 72.0
    matrix = fitz.Matrix(zoom, zoom)

    src = fitz.open(in_path)
    dst = fitz.open()

    for i in tqdm(
        range(len(src)), desc="Converting to grayscale", unit="page"
    ):
        page = src[i]
        # Render page at high DPI directly to grayscale
        pix = page.get_pixmap(
            matrix=matrix, colorspace=fitz.csGRAY, alpha=False
        )

        # Create a page with the same physical size; the high-res image
        # increases effective DPI
        rect = page.rect
        new_page = dst.new_page(width=rect.width, height=rect.height)

        # Insert the rendered image; PyMuPDF will embed losslessly (flate) from
        # pixmap
        new_page.insert_image(rect, pixmap=pix)

    # Save: garbage=4 for cleanup and deflate=True to keep size reasonable
    # without JPEG artifacts
    dst.save(out_path, garbage=4, deflate=True)
    dst.close()
    src.close()

    return str(out_path)