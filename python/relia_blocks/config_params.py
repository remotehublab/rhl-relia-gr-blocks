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

average_table = { 1.0:1.0,
    0.2:2.0,
    0.1:4.0,
    0.05:8.0,
}

def average_n2n(avginput):
    return average_table[avginput]

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

#This function fix the size of the vector to the length in GRC
def adapt_array(mydatain,mylen):
    temp=np.array(mydatain)
    temp2=temp[:,0:mylen]
    return  np.ndarray.tolist(temp2)


def relia_fft(datain,fftsize,nconnections):
    x,y=np.shape(datain)
    #print (x,y)
    if y>fftsize:
        temp=np.array(datain)
        temp2=temp[:,0:fftsize]
        ffttemp=10 * np.log10(np.abs(np.square(np.fft.fftshift(np.fft.fft(temp2[:,0:fftsize])))/fftsize))
        return  np.ndarray.tolist(ffttemp)
    else:
        return  np.ndarray.tolist(np.zeros((nconnections,fftsize)))

def relia_autocorr(datain,L,useDB):
    #print(datain)
    x,y=np.shape(datain)
    if y<1024:
        return np.ndarray.tolist(np.zeros((1,L)))
    else:
        myfft=np.square(abs(np.fft.fft(datain)))
        mycorr=np.real(np.fft.ifft(myfft))
        temp=np.array(mycorr)
        temp2=temp[:,0:L]
        if useDB:
            temp2=10*np.log10(temp2)
            temp2[np.isnan(temp2)] = 0
        else:
            temp2=temp2/np.max(temp2)
        #print (temp2)
        return np.ndarray.tolist(temp2)

