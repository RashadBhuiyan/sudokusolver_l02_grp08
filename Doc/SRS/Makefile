# Authors:
#      Kai Zhu, Rashad A. Bhuiyan, Stanley Chan
# Date:
#      2022-02-14

## setting the MAIN filename to the appropriate path
#  ensures that the proper latex files are made

MAIN = SRS
EXTRA := $(shell echo "Assets/*")

## Important files
OBJECTS = $(shell echo *.tex)
BIB = $(shell echo *.bib)

OBJECTS_TEST = $(addsuffix .t, $(basename $(OBJECTS))) 
BIB_TEST = bib
TEST_SET = $(addprefix make/, $(OBJECTS_TEST) $(BIB_TEST))
TEMP2 := $(shell mkdir make 2>/dev/null)

.PHONY: all
all: $(MAIN).pdf

$(MAIN).pdf: $(TEST_SET) $(EXTRA)
	pdflatex $(MAIN)
	pdflatex $(MAIN)

make/%.t: %.tex
	touch $@

make/bib: $(BIB)
	latex $(MAIN)
	bibtex $(MAIN)
	touch $@

.PHONY: clean
clean:
	-rm -f *.aux
	-rm -f *.bbl
	-rm -f make/bib
	-rm -f *.blg
	-rm -f *.fdb_latexmk
	-rm -f *.dvi
	-rm -f *.fls
	-rm -f *.lof
	-rm -f *.log
	-rm -f *.lot
	-rm -f *.out
	-rm -f *.synctex.gz
	-rm -f *.toc
	-rm -f *.pdf
	