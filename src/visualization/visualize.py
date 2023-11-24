import os
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import seaborn as sns

from src.visualization.colors import dark_grey

def change_matplotlib_font():
    FONT_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "assets"))

    font_files = fm.findSystemFonts(fontpaths=[FONT_PATH])
    for font_file in font_files:
        fm.fontManager.addfont(font_file)

    font_name = fm.FontProperties(fname=font_files[0]).get_name()
    matplotlib.rc("font", family=font_name)
    print("font family: ", plt.rcParams["font.family"])


def seaborn_style(background_color):
    font_family = "Montserrat"
    text_color = dark_grey

    sns.set_style(
        {
            "axes.facecolor": background_color,
            "figure.facecolor": background_color,
            "font.family": font_family,
            "text.color": text_color,
        }
    )

