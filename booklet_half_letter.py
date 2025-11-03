"""
booklet_half_letter.py
============================

This script converts a range of pages from an existing PDF into
two new PDFs arranged for booklet-style printing.  Each physical sheet
in the resulting output contains two pages placed side by side,
so that when printed double-sided and folded, the pages appear in the
correct order as a booklet.

The script produces two output files:
    • output_front.pdf  – contains the front sides (outer page pairs)
    • output_back.pdf   – contains the back sides (inner page pairs)

Usage
-----
    python3 booklet_half_letter_fixed.py input.pdf start_page end_page

Author
------
    Aashish Poudel
    Date: 2025-11-03
"""

from pypdf import PdfReader, PdfWriter, PageObject, Transformation

def create_booklet_pdfs(input_pdf, start_page, end_page):
    reader = PdfReader(input_pdf)
    pages = list(range(start_page - 1, end_page))

    # Pad to multiple of 4
    while len(pages) % 4 != 0:
        pages.append(None)

    n = len(pages)
    front_pairs, back_pairs = [], []
    for i in range(0, n // 2, 2):
        left1, right1 = pages[-(i + 1)], pages[i]
        left2, right2 = pages[-(i + 2)], pages[i + 1]
        front_pairs.append((left1, right1))
        back_pairs.append((right2, left2))

    w = reader.pages[0].mediabox.width
    h = reader.pages[0].mediabox.height

    def merge_pages(left_index, right_index):
        """Place two pages side by side on a blank canvas."""
        new_page = PageObject.create_blank_page(width=w * 2, height=h)

        # copy left page content
        if left_index is not None:
            left = reader.pages[left_index]
            new_page.merge_page(left)

        # copy right page content with translation
        if right_index is not None:
            right = reader.pages[right_index]
            t = Transformation().translate(tx=w, ty=0)
            new_page.merge_transformed_page(right, t)

        return new_page

    def write_booklet(pairs, out_name):
        writer = PdfWriter()
        for left, right in pairs:
            writer.add_page(merge_pages(left, right))
        with open(out_name, "wb") as f:
            writer.write(f)

    write_booklet(front_pairs, "output_front.pdf")
    write_booklet(back_pairs, "output_back.pdf")
    print("✅  Created booklet PDFs:\n - output_front.pdf\n - output_back.pdf")

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 4:
        print("Usage: python booklet_half_letter_fixed.py input.pdf start_page end_page")
        sys.exit(1)
    create_booklet_pdfs(sys.argv[1], int(sys.argv[2]), int(sys.argv[3]))
