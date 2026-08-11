import re

NOUGAT_PATH = r"output_nougat_math\65_4_1_Mathematics.mmd"
GRAPH_IMAGE = "math_extracted_images/Q16_graph_combined.png"
OUTPUT_PATH = "math_final_combined.md"

with open(NOUGAT_PATH, "r", encoding="utf-8") as f:
    text = f.read()

# Q16 ke question text ke turant baad graph image insert karo
pattern = re.compile(r"(16\.\s*Th[ee].*?given below is\s*:)", re.IGNORECASE)

def insert_graph(match):
    return match.group(1) + f"\n\n![Q16 Graph]({GRAPH_IMAGE})\n\n"

merged = pattern.sub(insert_graph, text)

with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
    f.write(merged)

print(f"Saved: {OUTPUT_PATH}")
if GRAPH_IMAGE in merged:
    print("Graph successfully inserted near Q16.")
else:
    print("Warning: Q16 pattern match nahi hua -- manually check karna padega.")