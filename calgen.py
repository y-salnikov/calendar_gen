#!/usr/bin/python2
# -*- coding: UTF-8 -*-

import sys,subprocess
from odf.opendocument import load
from odf.table import TableRow,TableCell
from odf.text import P
from odf import text, teletype

grid=[]
month_year=u""

def replace_tmpl(tmpl):
    global grid
    global month_year
    t=tmpl.strip()
    if t=="$month_year$": return month_year.decode("utf-8")
    if len(t)==5 and t[0]=='$' and t[1]=='g' and t[4]=='$':
	x=int(t[3])-1
	y=int(t[2])-1
	if y>=len(grid): return u" "
	if x>=len(grid[y]): return u" "
	return grid[y][x].encode("utf-8")
    return None
    
def main():
    global grid
    global month_year
    if len(sys.argv)==1:	cmd_line="ncal -h"
    else: cmd_line="ncal -h -m %s" %(sys.argv[1])
    cal_prc=subprocess.Popen(cmd_line.split(' '),stdout=subprocess.PIPE)
    cal_str_lst_tr=cal_prc.communicate()[0].split('\n')
    cal_str_lst=[cal_str_lst_tr[0]]
    for c in xrange(7):
	line=u""
	for l in xrange(7):
	    st=(cal_str_lst_tr[l+1].decode("utf-8")+u"   ")[c*3:(c*3+3)]
	    line=line+st
	cal_str_lst.append(line)
    month_year=cal_str_lst[0].strip()
    header=cal_str_lst[1].split(' ')
    header=[i for i in header if len(i)>0]
    for n in cal_str_lst:
	ned=[]
	if (len(n)>20):
	    for d in xrange(7):
		day=''+n[3*d]+n[(3*d)+1]
		ned.append(day)
	    grid.append(ned)
    grid=grid[2:]
    cal=load("template_ru.ods")
    texts = cal.getElementsByType(text.P)
    s=len(texts)
    for i in range(s):
	old_text = teletype.extractText(texts[i]).encode("utf-8")
	new_text =replace_tmpl(old_text)
	if new_text!=None:
	    new_S = text.P()
	    new_S.setAttribute("stylename",texts[i].getAttribute("stylename"))
	    new_S.addText(new_text)
	    texts[i].parentNode.insertBefore(new_S,texts[i])
	    texts[i].parentNode.removeChild(texts[i])
    cal.save("календарь на %s.ods" %(month_year))
main()
