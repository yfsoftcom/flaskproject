# -*- coding: utf-8 -*-
import unittest, re
from libs.kit import *

STR = '''logged_user = false;
	var static_id_cdn = 7;
	var html5player = new HTML5Player('html5video', '28605129');
	if (html5player) {
	    html5player.setVideoTitle('[POV] Japanese Blowjob #tower_ad39 - From JAVz.se');
	    html5player.setSponsors(false);
	    html5player.setVideoUrlLow('https://video-hw.xvideos-cdn.com/videos/3gp/0/d/a/xvideos.com_0da2d543359e254faadacddbb5d43e58.mp4?e=1539143702&ri=1024&rs=85&h=11d5cedc1c504ce7f86f2bca47ead768');
	    html5player.setThumbUrl('https://img-egc.xvideos-cdn.com/videos/thumbslll/0d/a2/d5/0da2d543359e254faadacddbb5d43e58/0da2d543359e254faadacddbb5d43e58.9.jpg');
	    html5player.setThumbUrl169('https://img-egc.xvideos-cdn.com/videos/thumbs169lll/0d/a2/d5/0da2d543359e254faadacddbb5d43e58/0da2d543359e254faadacddbb5d43e58.10.jpg');
	    html5player.setRelated(video_related);
	    html5player.setThumbSlide('https://img-egc.xvideos-cdn.com/videos/thumbs169/0d/a2/d5/0da2d543359e254faadacddbb5d43e58/mozaique.jpg');
	    html5player.setIdCDN('2');
	    html5player.setIdCdnHLS('7');
	    html5player.setFakePlayer(false);
	    html5player.setDesktopiew(true);
      html5player.setSeekBarColor('#tower_adde2600');
	    html5player.setUploaderName('mokkodotri');
	    html5player.setVideoURL('/video28605129/_pov_japanese_blowjob_39_-_from_javz.se');
	    html5player.setIsEmbed(true);
	    html5player.setStaticDomain('static-egc.xvideos-cdn.com');
	    html5player.setHttps();
	    html5player.setCanUseHttps();
	    document.getElementById('html5video').style.minHeight = '';
	    html5player.initPlayer();
   }
'''

class TestParse(unittest.TestCase):

    """Test TestParse"""

    def test_parser(self):
      regex_video_mp4 = re.compile(r'setVideoUrlLow\(\'[\S^\)]+\'\)')
      regex_http = re.compile(r'(ht|f)tp(s?)\:\/\/[0-9a-zA-Z]([-.\w]*[0-9a-zA-Z])*(:(0-9)*)*(\/?)([a-zA-Z0-9\-\.\?\,\/\\\+&amp;%\$#_=]*)?')

      r = str_search(STR, regex_video_mp4)
      if r:
        src = str_search(r, regex_http).strip()
        print(src)
        self.assertTrue(True)
      else:
        self.assertTrue(False)