"""Mapa de localização: a América do Sul e um zoom da região estudada.

Rode da raiz do repositório:

    uv run python docs/cinco_variaveis/figuras/mapa_regiao.py
"""

from pathlib import Path

import cartopy.crs as ccrs
import cartopy.feature as cfeature
import matplotlib.pyplot as plt
from matplotlib.patches import ConnectionPatch, Rectangle

AQUI = Path(__file__).resolve().parent
OESTE, LESTE, SUL, NORTE = -67, -43, -40, -14  # mesmo recorte do IC do Cláudio
VERMELHO = "#c0392b"
TERRA, MAR = "#f1eee6", "#dce9f2"
PC = ccrs.PlateCarree()

CIDADES = {
    "São Paulo": (-46.63, -23.55, "right"),
    "Curitiba": (-49.27, -25.43, "right"),
    "Porto Alegre": (-51.23, -30.03, "left"),
    "Buenos Aires": (-58.38, -34.60, "right"),
    "Montevidéu": (-56.16, -34.90, "left"),
    "Assunção": (-57.58, -25.26, "right"),
}
PAISES = {
    "BRASIL": (-50.5, -17.5),
    "PARAGUAI": (-59.8, -22.6),
    "BOLÍVIA": (-64.0, -16.0),
    "ARGENTINA": (-63.0, -31.0),
    "URUGUAI": (-55.9, -32.6),
}


def base(ax, escala):
    ax.add_feature(cfeature.OCEAN.with_scale(escala), facecolor=MAR, edgecolor="none")
    ax.add_feature(cfeature.LAND.with_scale(escala), facecolor=TERRA, edgecolor="none")
    ax.add_feature(cfeature.COASTLINE.with_scale(escala), linewidth=0.5, edgecolor="#555555")
    ax.add_feature(cfeature.BORDERS.with_scale(escala), linewidth=0.5, edgecolor="#777777")


fig = plt.figure(figsize=(7.0, 3.9))
ax1 = fig.add_axes([0.01, 0.03, 0.34, 0.92], projection=PC)
ax2 = fig.add_axes([0.42, 0.03, 0.56, 0.92], projection=PC)

# (a) a América do Sul inteira, com a região marcada
ax1.set_extent([-82, -34, -56, 13], crs=PC)
base(ax1, "110m")
ax1.add_patch(Rectangle((OESTE, SUL), LESTE - OESTE, NORTE - SUL, transform=PC,
                        facecolor="none", edgecolor=VERMELHO, linewidth=1.6))
ax1.text(-76, -28, "Oceano\nPacífico", transform=PC, fontsize=7, color="#4a6f8a",
         style="italic", ha="center")
ax1.text(-42, -49, "Oceano\nAtlântico", transform=PC, fontsize=7, color="#4a6f8a",
         style="italic", ha="center")
ax1.set_title("América do Sul", fontsize=9)

# (b) o zoom da região estudada
ax2.set_extent([OESTE, LESTE, SUL, NORTE], crs=PC)
base(ax2, "50m")
ax2.add_feature(cfeature.STATES.with_scale("50m"), linewidth=0.3, edgecolor="#a9a59b")
ax2.add_feature(cfeature.BORDERS.with_scale("50m"), linewidth=0.8, edgecolor="#555555")
for nome, (lon, lat) in PAISES.items():
    ax2.text(lon, lat, nome, transform=PC, fontsize=7.5, color="#444444",
             ha="center", va="center", fontweight="bold")
ax2.text(-46.5, -34.5, "Oceano\nAtlântico", transform=PC, fontsize=8, color="#4a6f8a",
         style="italic", ha="center")
for nome, (lon, lat, lado) in CIDADES.items():
    ax2.plot(lon, lat, "o", ms=3, color="#222222", transform=PC)
    dx = 0.5 if lado == "left" else -0.5
    ax2.text(lon + dx, lat, nome, transform=PC, fontsize=6.5, color="#222222",
             ha=lado, va="center")
grade = ax2.gridlines(draw_labels=True, linewidth=0.3, color="#bbbbbb", linestyle=":",
                      xlocs=range(-65, -42, 5), ylocs=range(-40, -13, 5))
grade.top_labels = grade.right_labels = False
grade.xlabel_style = grade.ylabel_style = {"size": 6.5, "color": "#555555"}
for borda in ax2.spines.values():
    borda.set_edgecolor(VERMELHO)
    borda.set_linewidth(1.4)
ax2.set_title("Região estudada", fontsize=9)

# linhas que ligam a caixa ao zoom
for canto_mapa, canto_zoom in [((LESTE, NORTE), (0, 1)), ((LESTE, SUL), (0, 0))]:
    fig.add_artist(ConnectionPatch(xyA=canto_mapa, coordsA=ax1.transData, xyB=canto_zoom,
                                   coordsB=ax2.transAxes, color=VERMELHO, linewidth=0.8,
                                   linestyle="--"))

fig.savefig(AQUI / "mapa_regiao.png", dpi=300, bbox_inches="tight")
print("ok", AQUI / "mapa_regiao.png")
