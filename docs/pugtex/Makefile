NAME := Optimizing a Trebuchet

export TOP = $(CURDIR)
export UI = $(TOP)/ui
export DROPBOX = $(HOME)/Dropbox/Public/trebuchet/
export DROPBOX_SLIDES = $(HOME)/Dropbox/Public/trebuchet/trebuchet_Slides
INCL = 
IMAGES = $(TOP)/assets
export STYLE = 
export RST2HTML := rst2html
export RST2S5 := rst2s5
export RST2S5FLAGS = --current-slide --theme-url ui/small-white-small-code --math-output=MathJax
export RST2HTMLFLAGS = 

export SLIDES_DIR = $(TOP)/slides
export HANDOUTS_DIR = $(TOP)/handouts

SUBDIRS = 

TALK_RST = $(wildcard *.rst)
TALK_HTML = $(subst rst,html,$(TALK_RST))
HANDOUT_HTML = $(subst rst,handout.html,$(TALK_RST))
TALK_HTML_DEPS = $(TALK_RST) $(wildcard *.rst) $(STYLE)


#$(TALK_HTML): $(TALK_HTML_DEPS)
%.html: %.rst
	$(RST2S5) $(RST2S5FLAGS) $< $@

%.handout.html: %.rst
	$(RST2HTML) $(RST2HTMLFLAGS) $< $@

$(SLIDES_DIR): $(TALK_HTML)
	cd $(TOP) 
	mkdir -p $(SLIDES_DIR)
	for f in $^; do cp $$f $(SLIDES_DIR); done
	for f in $^; do cp $$f $(DROPBOX_SLIDES); done 
	cp -R  ui $(SLIDES_DIR)
	cp -R  $(IMAGES) $(SLIDES_DIR)
	cp -R  ui $(DROPBOX_SLIDES)
	cp -R  assets $(DROPBOX_SLIDES) 

$(HANDOUTS_DIR): $(HANDOUT_HTML)
	cd $(TOP)
	mkdir -p $(HANDOUTS_DIR)
	mkdir -p $(DROPBOX)
	for f in $^; do cp $$f $(HANDOUTS_DIR); done
	for f in $^; do cp $$f $(DROPBOX); done 

$(SUBDIRS): force_look
	$(MAKE) -C $@ $(MAKECMDGOALS)

dist: $(SLIDES_DIR) $(HANDOUTS_DIR) $(SUBDIRS)

clean:
	rm -rf $(SLIDES_DIR)
	rm -rf $(HANDOUTS_DIR)
	find -name '*.rst' -exec touch {} ';'
	find -name '*.html' -exec rm {} ';'

force_look:
	true

.PHONY: dist clean force_look

