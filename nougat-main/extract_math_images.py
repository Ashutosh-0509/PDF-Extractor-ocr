import fitz
import os

pdf_path = r"C:\Users\Ashutosh Amale\Downloads\65_4_1_Mathematics.pdf"
output_dir = "math_extracted_images"
os.makedirs(output_dir, exist_ok=True)

doc = fitz.open(pdf_path)
count = 0

for page_num in range(len(doc)):
    page = doc[page_num]
    images = page.get_images(full=True)
    for img_index, img in enumerate(images):
        xref = img[0]
        base_image = doc.extract_image(xref)
        image_bytes = base_image["image"]
        ext = base_image["ext"]
        filename = f"{output_dir}/page{page_num+1}_img{img_index+1}.{ext}"
        with open(filename, "wb") as f:
            f.write(image_bytes)
        count += 1
        print(f"Saved: {filename}")

print(f"\nTotal images extracted: {count}")
doc.close()