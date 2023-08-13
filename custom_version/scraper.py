import os
import requests
import glob

URL = "https://hikaku-sitatter.com/en/"
PARENT_DIR = os.path.dirname(__file__)
OUT_PATH = os.path.join(PARENT_DIR, "out.svg")
SVG_SPRITES_FOLDER = os.path.join(PARENT_DIR, "svg_sprites")


def main():

    final_content = """<svg width="1000" height="1000">
    <defs>"""

    for filename in os.listdir(SVG_SPRITES_FOLDER):
        file = os.path.join(SVG_SPRITES_FOLDER, filename)
        with open(file, "r") as f:
            content = f.read()


        final_content += f"""
        <g id="{filename}"> {content} </g>"""

    final_content += """
    </defs>
</svg>        
"""
    with open(OUT_PATH, "w+") as f:
        f.write(final_content)


if __name__ == "__main__":
    main()