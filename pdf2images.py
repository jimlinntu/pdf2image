import argparse
import pdf2image
from pathlib import Path

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("pdffile", type=str)
    parser.add_argument("output_dir", type=str)
    args = parser.parse_args()
    images = pdf2image.convert_from_path(args.pdffile)
    pdf_path = Path(args.pdffile)
    pdf_prefix = "".join(pdf_path.name.split(".")[:-1])
    out_dir = Path(args.output_dir)
    out_dir.mkdir(exist_ok=True)
    for page_idx, pil_image in enumerate(images):
        pil_image.save(out_dir / "{}_page_{}.png".format(pdf_prefix, page_idx))
    
if __name__ == "__main__":
    main()
