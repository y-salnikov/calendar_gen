#!/usr/bin/python3

import datetime,sys

from odf.opendocument import load
from odf.table import TableRow,TableCell
from odf.text import P
from odf import text, teletype


mn=["Нулябрь","Январь","Февраль","Март","Апрель","Май","Июнь","Июль","Август","Сентябрь","Октябрь","Ноябрь","Декабрь"]





def m_grid(month=None):
	now=datetime.date.today()
	if month is None:
		month=now.month
	f_day=datetime.date(now.year,month,1).weekday()
	if month==12: n=31
	else: n=(datetime.date(now.year,month+1,1)-datetime.date(now.year,month,1)).days
	grid=[]
	i=0
	for r in range(6):
		l=[]
		for c in range(7):
			if (i>=f_day and (i-f_day)<n):
				l.append("%2d"%(1+i-f_day))
			else: l.append('')
			i+=1
		grid.append(l)
	return grid

def replace_tmpl(tmpl,grid,month_year):
	t=tmpl.strip()
	if t=="$month_year$": return month_year
	if len(t)==5 and t[0]=='$' and t[1]=='g' and t[4]=='$':
		x=int(t[3])-1
		y=int(t[2])-1
		if y>=len(grid): return " "
		if x>=len(grid[y]): return " "
		return grid[y][x]
	return None


def main():
	if len(sys.argv)==1: m=None
	else: m=int(sys.argv[1])
	grid=m_grid(m)
	now=datetime.date.today()
	if m is None:
		m=now.month
	f_day=datetime.date(now.year,m,1)
	cal=load("template_ru.ods")
	texts = cal.getElementsByType(text.P)
	s=len(texts)
	month_year="%s %d" %(mn[m],f_day.year)
	for i in range(s):
		old_text = teletype.extractText(texts[i])
		new_text =replace_tmpl(old_text,grid,month_year)
		if new_text!=None:
			new_S = text.P()
			new_S.setAttribute("stylename",texts[i].getAttribute("stylename"))
			new_S.addText(new_text)
			texts[i].parentNode.insertBefore(new_S,texts[i])
			texts[i].parentNode.removeChild(texts[i])
	cal.save("календарь на %s.ods" %(month_year))
main()






