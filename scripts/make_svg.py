import argparse
import os
import copy
import re
import xml.etree.ElementTree as ET
from svgpathtools import parse_path

# The gradient colors based on your uploaded image
GRADIENT_SVG = """
<defs xmlns="http://www.w3.org/2000/svg">
  <linearGradient id="vaporwaveGrad" x1="0%" y1="0%" x2="100%" y2="0%">
    <stop offset="0%" stop-color="#f65e79" />
    <stop offset="50%" stop-color="#8a3ab9" />
    <stop offset="100%" stop-color="#4978f4" />
  </linearGradient>
</defs>
"""

# The solid background color matching the base in your image
BG_COLOR = "#361c7d"


def apply_color_to_element(element, new_color):
    """Safely forces the fill and stroke of an element to a new color."""
    if element.get("fill") not in [None, "none"]:
        element.set("fill", new_color)
    elif element.get("fill") is None and "path" in element.tag:
        element.set("fill", new_color)

    if element.get("stroke") not in [None, "none"]:
        element.set("stroke", new_color)

    style = element.get("style")
    if style:
        style = re.sub(r"fill\s*:\s*[^;]+", f"fill: {new_color}", style)
        style = re.sub(r"stroke\s*:\s*[^;]+", f"stroke: {new_color}", style)
        element.set("style", style)


def process_svgs(input_file):
    ET.register_namespace("", "http://www.w3.org/2000/svg")
    base_name, ext = os.path.splitext(input_file)

    try:
        original_tree = ET.parse(input_file)

        # ==========================================
        # PART 1: Generate the All-White Original
        # ==========================================
        white_tree = copy.deepcopy(original_tree)
        for elem in white_tree.iter():
            if any(
                tag in elem.tag
                for tag in ["path", "rect", "circle", "polygon", "polyline", "ellipse"]
            ):
                apply_color_to_element(elem, "white")

        white_output = f"{base_name}_background{ext}"
        white_tree.write(white_output, xml_declaration=True, encoding="utf-8")
        print(f"[✓] Saved white original: {white_output}")

        # ==========================================
        # PART 2: Generate the Layered Gradient SVG
        # ==========================================
        layered_tree = copy.deepcopy(original_tree)
        root = layered_tree.getroot()
        ns_path = "{http://www.w3.org/2000/svg}path"

        # Inject the gradient definition
        defs_elem = ET.fromstring(GRADIENT_SVG)
        root.insert(0, defs_elem)

        for parent in root.iter():
            for child in list(parent):
                if child.tag == ns_path or child.tag == "path":
                    d_attr = child.get("d")
                    if not d_attr:
                        continue

                    # Apply the vaporwave gradient to the original path
                    apply_color_to_element(child, "url(#vaporwaveGrad)")

                    # Calculate geometry for the background
                    full_path = parse_path(d_attr)
                    subpaths = full_path.continuous_subpaths()
                    kept_subpaths = []

                    for i, sp_a in enumerate(subpaths):
                        bbox_a = sp_a.bbox()
                        is_hole = False

                        for j, sp_b in enumerate(subpaths):
                            if i == j:
                                continue
                            bbox_b = sp_b.bbox()

                            if (
                                bbox_a[0] >= bbox_b[0]
                                and bbox_a[1] <= bbox_b[1]
                                and bbox_a[2] >= bbox_b[2]
                                and bbox_a[3] <= bbox_b[3]
                            ):

                                if bbox_a == bbox_b and i < j:
                                    continue
                                is_hole = True
                                break

                        if not is_hole:
                            kept_subpaths.append(sp_a)

                    # Create the solid background layer underneath
                    if kept_subpaths:
                        new_d = " ".join([sp.d() for sp in kept_subpaths])

                        bg_path = ET.Element(child.tag)
                        bg_path.set("d", new_d)
                        bg_path.set("fill", BG_COLOR)
                        bg_path.set("fill-rule", "nonzero")

                        if child.get("transform"):
                            bg_path.set("transform", child.get("transform"))

                        insert_index = list(parent).index(child)
                        parent.insert(insert_index, bg_path)

        layered_output = f"{base_name}_foreground{ext}"
        layered_tree.write(layered_output, xml_declaration=True, encoding="utf-8")
        print(f"[✓] Saved layered gradient: {layered_output}")

    except Exception as e:
        print(f"Error processing SVG: {e}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Create a white SVG and a hardcoded layered gradient SVG."
    )
    parser.add_argument("input", help="Path to the original SVG file")

    args = parser.parse_args()

    if not os.path.isfile(args.input):
        print(f"Error: The file '{args.input}' does not exist.")
    else:
        process_svgs(args.input)
