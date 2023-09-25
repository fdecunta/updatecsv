PREFIX = /usr/local
MANPREFIX = /share/man


install: updatecsv.py
	cp updatecsv.py $(PREFIX)/bin/updatecsv
	chmod +x $(PREFIX)/bin/updatecsv
	chmod 755 $(PREFIX)/bin/updatecsv
	mkdir -p $(PREFIX)$(MANPREFIX)/man1
	cp updatecsv.1 $(PREFIX)$(MANPREFIX)/man1/
	chmod 644 $(PREFIX)$(MANPREFIX)/man1/updatecsv.1

uninstall:
	rm -f $(PREFIX)/bin/updatecsv
	rm -f $(PREFIX)$(MANPREFIX)/man1/updatecsv.1

.PHONY: install uninstall
