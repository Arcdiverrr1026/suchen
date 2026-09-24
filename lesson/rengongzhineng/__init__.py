import matplotlib.font_manager as fm

fonts = fm.findSystemFonts()
print(len(fonts))

for f in fonts[:30]:
    print(f)