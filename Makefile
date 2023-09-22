PREFIX = /usr/local
MANPREFIX = /share/man
# Modificar segun ejecutable de python
PYTHONV = python

install: planillator.py
	sed "s/PYTHONV/$(PYTHONV)/g" < planillator.py > $(PREFIX)/bin/planillator
	chmod +x $(PREFIX)/bin/planillator
	chmod 755 $(PREFIX)/bin/planillator
	mkdir -p $(PREFIX)$(MANPREFIX)/man1
	# cp planillator.1 $(PREFIX)$(MANPREFIX)/man1/
	# chmod 644 $(PREFIX)$(MANPREFIX)/man1/planillator.1

uninstall:
	rm -f $(PREFIX)/bin/planillator
	# rm -f $(PREFIX)$(MANPREFIX)/man1/planillator.1

.PHONY: install uninstall
