all: bib pdf

generate_gbib_source:
	python3 scripts/bib_generator.py bibliography/ output/bibliography.gbib

bib: generate_gbib_source
	python3 scripts/gbib.py output/bibliography.gbib output/bibliography.tex

pdf:
	latexmk --output-directory=output/ -xelatex main.tex

clean:
	rm -rf output/

