PREFIX = /usr/local

src = $(wildcard *.c)
obj = $(src:.c=.o)

CC=gcc
CFLAGS = -I/usr/include/python2.7 -lpython2.7

pol: $(obj)
	$(CC) -o $@ $^ $(CFLAGS)

.PHONY: clean
clean:
	rm -f $(obj) pol

.PHONY: install
install: pol
	mkdir -p $(DESTDIR)$(PREFIX)/bin
	cp $< $(DESTDIR)$(PREFIX)/bin/pol

.PHONY: pol
uninstall:
	rm -f $(DESTDIR)$(PREFIX)/bin/pol
