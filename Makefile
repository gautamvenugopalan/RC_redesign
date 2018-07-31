#!/usr/bin/make -f
.PHONY: all
all: main

main: %: %.tex
	latexmk -pdf $@

.PHONY: clean
clean:
	latexmk -c

