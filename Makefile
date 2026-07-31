PYTHON := python3
PYINSTALLER := pyinstaller

APP := CounterLauncher
ENTRY := minecraft_dl.py
ICON := channels4_profile_256.png

APPDIR := AppDir
DIST := dist
BUILD := build

.PHONY: all clean appdir appimage

all: appimage

clean:
	rm -rf $(BUILD) $(DIST) $(APPDIR) *.spec *.AppImage

build:
	$(PYINSTALLER) --onefile --name $(APP) $(ENTRY)

appdir: build
	mkdir -p $(APPDIR)/usr/bin
	cp $(DIST)/$(APP) $(APPDIR)/usr/bin/$(APP)
	cp $(ICON) $(APPDIR)/$(APP).png

	printf '#!/bin/sh\nHERE="$$(dirname "$$(readlink -f "$$0")")"\nexec "$$HERE/usr/bin/$(APP)" "$$@"\n' > $(APPDIR)/AppRun
	chmod +x $(APPDIR)/AppRun

	printf '[Desktop Entry]\n\
Type=Application\n\
Name=$(APP)\n\
Comment=Minecraft Launcher\n\
Exec=$(APP)\n\
Icon=$(APP)\n\
Terminal=true\n\
Categories=Game;\n' > $(APPDIR)/$(APP).desktop

appimage: appdir
	./appimagetool $(APPDIR)
