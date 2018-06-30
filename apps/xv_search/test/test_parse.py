# -*- coding: utf-8 -*-
import unittest, re
from libs.kit import *

STR = '''logged_user = false;
	var static_id_cdn = 2;
	var html5player = new HTML5Player('html5video', '12050059');
	if (html5player) {
	    html5player.setVideoTitle('JAPAN HD Special Japanese Blowjob');
	    html5player.setSponsors([{"link":"http:\/\/enter.japanhd.xxx\/track\/MjYyMS41LjEzMi4zNjUuMC4wLjAuMC4w","desc":"You like your Asian girls petite and dirty? You'll love our Japanese girls doing everything you have dreamed off in full uncensored HD videos!","records2257":"http:\/\/www.japanhd.xxx\/2257","name":"Japan Hd"}]);
	    html5player.setVideoUrlLow('https://video-hw.xvideos-cdn.com/videos/3gp/b/1/9/xvideos.com_b190e77d1dfe475671da7c80311c8cda-1.mp4?e=1530260161&ri=1024&rs=85&h=a4a3428c701f52fbe070a1ddaa1e0e32');
	    html5player.setVideoUrlHigh('https://video-hw.xvideos-cdn.com/videos/mp4/b/1/9/xvideos.com_b190e77d1dfe475671da7c80311c8cda-1.mp4?e=1530260161&ri=1024&rs=85&h=92d6db78290e0402a63448f94b67126b');
	    html5player.setVideoHLS('https://hls-hw.xvideos-cdn.com/videos/hls/b1/90/e7/b190e77d1dfe475671da7c80311c8cda-1/hls.m3u8?e=1530260161&l=0&h=bf294a1d7911052f9466d98862fc0393');
	    html5player.setThumbUrl('https://img-l3.xvideos-cdn.com/videos/thumbslll/b1/90/e7/b190e77d1dfe475671da7c80311c8cda/b190e77d1dfe475671da7c80311c8cda.19.jpg');
	    html5player.setThumbUrl169('https://img-l3.xvideos-cdn.com/videos/thumbs169lll/b1/90/e7/b190e77d1dfe475671da7c80311c8cda/b190e77d1dfe475671da7c80311c8cda.5.jpg');
	    html5player.setRelated(video_related);
	    html5player.setThumbSlide('https://img-l3.xvideos-cdn.com/videos/thumbs169/b1/90/e7/b190e77d1dfe475671da7c80311c8cda/mozaique.jpg');
	    html5player.setThumbSlideBig('https://img-l3.xvideos-cdn.com/videos/thumbs169/b1/90/e7/b190e77d1dfe475671da7c80311c8cda/mozaiquefull.jpg');
	    html5player.setThumbSlideMinute('https://img-l3.xvideos-cdn.com/videos/thumbs169/b1/90/e7/b190e77d1dfe475671da7c80311c8cda/mozaiquemin_');
	    html5player.setIdCDN('2');
	    html5player.setIdCdnHLS('2');
	    html5player.setFakePlayer(false);
	    html5player.setDesktopiew(true);
      html5player.setSeekBarColor('#de2600');
	    html5player.setUploaderName('japan-hd');
	    html5player.setVideoURL('/video12050059/japan_hd_special_japanese_blowjob');
	    html5player.setStaticDomain('static-hw.xvideos.works');
	    html5player.setHttps();
	    html5player.setCanUseHttps();
	    document.getElementById('html5video').style.minHeight = '';
	    html5player.initPlayer();
'''

class TestParse(unittest.TestCase):

    """Test TestParse"""

    def test_parser(self):
        regex = re.compile(r'setVideoUrlHigh\(\'[\S^\)]+\'\)')
        m = regex.search(STR)
        if m is True:
		  	self.assertEqual(m.group(0), "setVideoUrlHigh('https://video-hw.xvideos-cdn.com/videos/mp4/b/1/9/xvideos.com_b190e77d1dfe475671da7c80311c8cda-1.mp4?e=1530260161&ri=1024&rs=85&h=92d6db78290e0402a63448f94b67126b')")
		    download_file('https://video-hw.xvideos-cdn.com/videos/mp4/b/1/9/xvideos.com_b190e77d1dfe475671da7c80311c8cda-1.mp4?e=1530262489&ri=1024&rs=85&h=f2cbd2fb46c54a6b6b462e8d26643fcc', './demo.mp4')
        else:
            self.assertTrue(False)