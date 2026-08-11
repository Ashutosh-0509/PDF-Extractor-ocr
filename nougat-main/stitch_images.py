from PIL import Image

img1 = Image.open("math_extracted_images/page2_img1.png")
img2 = Image.open("math_extracted_images/page2_img2.png")
img3 = Image.open("math_extracted_images/page2_img3.png")

# Sabki width same honi chahiye (agar nahi hai, resize karenge)
width = max(img1.width, img2.width, img3.width)
total_height = img1.height + img2.height + img3.height

combined = Image.new("RGB", (width, total_height), "white")
combined.paste(img1, (0, 0))
combined.paste(img2, (0, img1.height))
combined.paste(img3, (0, img1.height + img2.height))

combined.save("math_extracted_images/Q16_graph_combined.png")
print("Saved: math_extracted_images/Q16_graph_combined.png")