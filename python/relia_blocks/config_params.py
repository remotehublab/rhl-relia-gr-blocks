import numpy as np

color_table = {    
	'black':'#000000' ,
    'white': '#ffffff',
    'red'  : '#ff0000',
    'dark red':'#800000',
    'green':'#00ff00',
    'dark green':'#008000',
    'blue':'#0000ff',
    'dark blue':'#000080',
    'yellow':'#ffff00',
    'cyan':'#00ffff' ,
    'magenta':'#ff00ff',
	'"black"':'#000000' ,
    '"white"': '#ffffff',
    '"red"'  : '#ff0000',
    '"dark red"':'#800000',
    '"green"':'#00ff00',
    '"dark green"':'#008000',
    '"blue"':'#0000ff',
    '"dark blue"':'#000080',
    '"yellow"':'#ffff00',
    '"cyan"':'#00ffff' ,
    '"magenta"':'#ff00ff'
    }
    
style_table = { '1':['1', '0'] ,
 	'2':['3', '1'] ,
 	'3':['1', '3'] ,
 	'4':['3', '1', '1', '3'] ,
 	'5':['3', '1', '1', '3', '1', '3'],
 	'0':['1', '0'],
 	
     }

marker_table = {    '-1':'none' ,
    '0': 'circle',
    '1' : 'square',
    '2':'diamond',
    '3':'triangle',
    '4':'star',
    '5':'polygon',
    }



def color_name2hex(coloraname):
	l=len(coloraname)
	color_output=[]
	for i in range(l):
		color_output.append(color_table[coloraname[i]])
	return color_output

def style_number2dotdash(stylename):
	l=len(stylename)
	style_output=[]
	for i in range(l):
		style_output.append(style_table[stylename[i]])
	return style_output

def marker_number2shape(markername):
	l=len(markername)
	marker_output=[]
	for i in range(l):
		marker_output.append(marker_table[markername[i]])
	return marker_output
		
def relia_fft(datain):
	return  10 * np.log10(abs(np.fft.fftshift(np.fft.fft(datain)))**2)
