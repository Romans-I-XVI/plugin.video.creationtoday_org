'''
    t0mm0 test XBMC Addon
    Copyright (C) 2011 t0mm0

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''
import urllib
import urllib2
import xbmcplugin
import xbmcgui
import xbmcaddon
import os
import re
import string
import sys
from addon import Addon
from net import Net
import urlresolver


addon = Addon('plugin.video.creationtoday_org', sys.argv)
net = Net()

#logo = os.path.join(addon.get_path(), 'art','logo.jpg')

base_url = 'http://www.creationtoday.org'

play = addon.queries.get('play', None)


def MAIN():
	addDir('Creation Today', base_url + '/category/type/video/podcasts/',1,'')
	addDir('Creation Minute', 'https://www.youtube.com/playlist?list=PLvFrrGonrTSOO8_ZtChPQrBxx4MSla9Qb',2,'')


def Creation_Today(url):
	link = getUrl(url)
	match=re.compile('<span class="title"><a href="(.+?)"').findall(link)
	title=re.compile('<span class="title"><a href=".+?" rel="bookmark" title=".+?">(.+?)</a></span>').findall(link)
	thumb=re.compile('<img src="(.+?)" width="150" height="94" alt="" />').findall(link)
	mylist=zip((match),(title),(thumb))
	for url,title,thumb in mylist:
		title=title.replace("&#8211;","")
		addDir(title, url, 10, thumb)
		#url = GETSOURCE(url)
		#try:
		#	url = url[0]
		#	addon.add_item({'url': 'http://www.vimeo.com/' + url},
		#	{'title': title})
		#except:
		#	pass
#		addon.add_video_item({'url': 'http://www.vimeo.com/' + url},
#		{'title': 'youtube url'})
		
#	match=re.compile('<iframe src="http://player.vimeo.com/video/(.+?)title').findall(link)
	
#	for match in match:
#		match = match[:-1]
#		xbmc.log(match)
#		addon.add_video_item({'url': 'http://www.vimeo.com/' + match},
#		{'title': 'youtube url'})

	
def Creation_Minute(url):
	link = getUrl(url)	
	match=re.compile('watch?v=(.+?)').findall(link)
	title=re.compile('<a class=".+?" href="/watch?v=.+?">(.+?)</a>').findall(link)
	mylist=zip((match),(title))
	xbmc.log(str(match))
	for match,title in mylist:
		xbmc.log('http://www.youtube.com/watch?v='+match)
		addon.add_video_item({'url': 'http://www.youtube.com/watch?v='+match},
		{'title': title})




#    addon.add_video_item({'url': 'http://www.vimeo.com/30081785'},
#                         {'title': 'vimeo url'})
#    addon.add_video_item({'url': 'http://www.youtube.com/watch?v=Rnb28mYeSMI'},
#                         {'title': 'youtube url'})

if play:
	url = addon.queries.get('url', '')
	host = addon.queries.get('host', '')
	media_id = addon.queries.get('media_id', '')
	#stream_url = urlresolver.resolve(play)
	stream_url = urlresolver.HostedMediaFile(url=url, host=host, media_id=media_id).resolve()
	addon.resolve_url(stream_url)

def getUrl(url):
	req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
	return link

def GETSOURCE(url):
	link = getUrl(url)
	match=re.compile('<iframe src="http://player.vimeo.com/video/(.+?)title').findall(link)
	match=match[0]
	addon.add_item({'url': 'http://www.vimeo.com/' + match},
	{'title': 'test'})

def get_params():
        param=[]
        paramstring=sys.argv[2]
        if len(paramstring)>=2:
                params=sys.argv[2]
                cleanedparams=params.replace('?','')
                if (params[len(params)-1]=='/'):
                        params=params[0:len(params)-2]
                pairsofparams=cleanedparams.split('&')
                param={}
                for i in range(len(pairsofparams)):
                        splitparams={}
                        splitparams=pairsofparams[i].split('=')
                        if (len(splitparams))==2:
                                param[splitparams[0]]=splitparams[1]
                                
        return param
##################################################################################################################################
	

def addLink(name,url,iconimage):
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz)
        return ok

##################################################################################################################################

def addDir(name,url,mode,iconimage):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
        xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        return ok

##################################################################################################################################
        
              
params=get_params()
url=None
name=None
mode=None

try:
        url=urllib.unquote_plus(params["url"])
except:
        pass
try:
        name=urllib.unquote_plus(params["name"])
except:
        pass
try:
        mode=int(params["mode"])
except:
        pass

print "Mode: "+str(mode)
print "URL: "+str(url)
print "Name: "+str(name)

if mode==None or url==None or len(url)<1:
        print ""
        MAIN()
       
elif mode==1:
        print ""+url
        Creation_Today(url)
        
elif mode==2:
        print ""+url
        Creation_Minute(url)

elif mode==3:
        print ""+url
        CATEGORIES(url)

elif mode==4:
        print ""+url
        FAITHISSUES(url)

elif mode==5:
        print ""+url
        PROGRAMS(url)

elif mode==6:
        print ""+url
        RECENT(url)

elif mode==7:
        print ""+url
        LIVE(url)

elif mode==8:
        print ""+url
        SEARCH(url)

elif mode==9:
        print ""+url
        AIRDATE(url)

elif mode==10:
        print ""+url
        GETSOURCE(url)
elif mode==11:
        print ""+url
        PREVIOUS()

xbmcplugin.endOfDirectory(int(sys.argv[1]))




