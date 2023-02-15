.PHONY:readme
readme:
	@awk -i inplace -v q="\`\`\`" 'BEGIN {p=1} /^<!-- help start -->/{print;print "";print q;print "$$ hag -h";system("hag -h");print q;print "";p=0} /^<!-- help end -->/{p=1} p' README.md
	@awk -i inplace -v q="python -c 'import hag; [print(\"- \" + p) for p in hag.parsers.__all__]'" 'BEGIN {p=1} /^<!-- parsers start -->/{print;print "";system(q);print "";p=0} /^<!-- parsers end -->/{p=1} p' README.md
