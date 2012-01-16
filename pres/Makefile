markdown_srcs := $(wildcard *.md)
markdown_web   = $(markdown_srcs:.md=.html)
markdown_pres  = $(markdown_srcs:.md=_pres.html)

all : $(markdown_web) $(markdown_pres)

%.html : %.md
	markdown_py -x def_list -x codehilite -n $< -f $@
%_pres.html : %.md
	landslide -l no -x def_list $< -c -r -d $@

web: overview.html
	open overview.html
pres: overview_pres.html
	open overview_pres.html

clean: 
	rm *.html