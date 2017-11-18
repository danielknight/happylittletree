import os
import shutil
import regex as re
from django.conf import settings
from django.core.management.base import BaseCommand

from bobross.models import Episode, Paints


class Command(BaseCommand):
    # args = '<foo bar ...>'
    help = 'Use this to populate the db'

    paints_dict = {
        'Phthalo Blue': ['http://amzn.to/2tV2Iee',
                         """<a target="_blank" href="https://www.amazon.com/gp/product/B0009IL2N2/ref=as_li_tl?ie=UTF8&camp=1789&creative=9325&creativeASIN=B0009IL2N2&linkCode=as2&tag=happylittletr-20&linkId=9c88b153936c5921f78e84f064e19d6f">Winton Oil Paint 37ml Tube: Phthalo Blue</a><img src="//ir-na.amazon-adsystem.com/e/ir?t=happylittletr-20&l=am2&o=1&a=B0009IL2N2" width="1" height="1" border="0" alt="" style="border:none !important; margin:0px !important;" />"""],
        'Van Dyke Brown': ['http://amzn.to/2sYpBNW',
                           """<a target="_blank" href="https://www.amazon.com/gp/product/B004O7BQF8/ref=as_li_tl?ie=UTF8&camp=1789&creative=9325&creativeASIN=B004O7BQF8&linkCode=as2&tag=happylittletr-20&linkId=e2cc7b132f02774b8aa23bdcc55f2745">Winton Oil Paint 37ml/Tube-Vandyke Brown</a><img src="//ir-na.amazon-adsystem.com/e/ir?t=happylittletr-20&l=am2&o=1&a=B004O7BQF8" width="1" height="1" border="0" alt="" style="border:none !important; margin:0px !important;" />"""],
        'Alizarin Crimson': ['http://amzn.to/2tlQbDK',
                             """<a target="_blank" href="https://www.amazon.com/gp/product/B004O79MIQ/ref=as_li_tl?ie=UTF8&camp=1789&creative=9325&creativeASIN=B004O79MIQ&linkCode=as2&tag=happylittletr-20&linkId=8580e892cd9ad9100cea24434c338a0a">Winton Oil Paint 37ml/Tube-Permanent Alizarin Crimson</a><img src="//ir-na.amazon-adsystem.com/e/ir?t=happylittletr-20&l=am2&o=1&a=B004O79MIQ" width="1" height="1" border="0" alt="" style="border:none !important; margin:0px !important;" />"""],
        'Midnight Black': ['http://amzn.to/2ufBL4q',
                           """<a target="_blank" href="https://www.amazon.com/gp/product/B0027AEEB2/ref=as_li_tl?ie=UTF8&camp=1789&creative=9325&creativeASIN=B0027AEEB2&linkCode=as2&tag=happylittletr-20&linkId=987f5f4313abbfdd58a22edb3f2662b2">Bob Ross MR6004 37-Ml Artist Oil Color, Midnight Black</a><img src="//ir-na.amazon-adsystem.com/e/ir?t=happylittletr-20&l=am2&o=1&a=B0027AEEB2" width="1" height="1" border="0" alt="" style="border:none !important; margin:0px !important;" />"""],
        'Bright Red': ['http://amzn.to/2tlCEvQ',
                       """<a target="_blank" href="https://www.amazon.com/gp/product/B001E1TGHW/ref=as_li_tl?ie=UTF8&camp=1789&creative=9325&creativeASIN=B001E1TGHW&linkCode=as2&tag=happylittletr-20&linkId=3581088b6e63dbfa3a3a74332d38f3ad">Winsor &amp; Newton Artists Oil Color Paint Tube, 37ml, Bright Red</a><img src="//ir-na.amazon-adsystem.com/e/ir?t=happylittletr-20&l=am2&o=1&a=B001E1TGHW" width="1" height="1" border="0" alt="" style="border:none !important; margin:0px !important;" />"""],
        'Permanent Red': ['http://amzn.to/2tlCEvQ',
                       """<a target="_blank" href="https://www.amazon.com/gp/product/B001E1TGHW/ref=as_li_tl?ie=UTF8&camp=1789&creative=9325&creativeASIN=B001E1TGHW&linkCode=as2&tag=happylittletr-20&linkId=3581088b6e63dbfa3a3a74332d38f3ad">Winsor &amp; Newton Artists Oil Color Paint Tube, 37ml, Bright Red</a><img src="//ir-na.amazon-adsystem.com/e/ir?t=happylittletr-20&l=am2&o=1&a=B001E1TGHW" width="1" height="1" border="0" alt="" style="border:none !important; margin:0px !important;" />"""],
        'Phthalo Green': ['http://amzn.to/2sYGFn8',
                          """<a target="_blank" href="https://www.amazon.com/gp/product/B001JPIQ2O/ref=as_li_tl?ie=UTF8&camp=1789&creative=9325&creativeASIN=B001JPIQ2O&linkCode=as2&tag=happylittletr-20&linkId=201795ad28afca3898f835fb3540b703">M. Graham Artist Oil Paint Phthalo Green 1.25oz/37ml Tube</a><img src="//ir-na.amazon-adsystem.com/e/ir?t=happylittletr-20&l=am2&o=1&a=B001JPIQ2O" width="1" height="1" border="0" alt="" style="border:none !important; margin:0px !important;" />"""],
        'Cadmium Yellow': ['http://amzn.to/2tVdWPX',
                           """<a target="_blank" href="https://www.amazon.com/gp/product/B0009IL2JG/ref=as_li_tl?ie=UTF8&camp=1789&creative=9325&creativeASIN=B0009IL2JG&linkCode=as2&tag=happylittletr-20&linkId=1d4e4ce111220c9076059a038543f8d8">Winsor &amp; Newton Winton 37-Milliliter Oil Paint, Cadmium Yellow Light</a><img src="//ir-na.amazon-adsystem.com/e/ir?t=happylittletr-20&l=am2&o=1&a=B0009IL2JG" width="1" height="1" border="0" alt="" style="border:none !important; margin:0px !important;" />"""],
        'Dark Sienna': ['http://amzn.to/2rZwQ76',
                        """<a target="_blank" href="https://www.amazon.com/gp/product/B0027A3G4S/ref=as_li_tl?ie=UTF8&camp=1789&creative=9325&creativeASIN=B0027A3G4S&linkCode=as2&tag=happylittletr-20&linkId=f2c5fde46159db0b7d8eda05c22413f8">Bob Ross MR6001 37-Ml Artist Oil Color, Dark Sienna</a><img src="//ir-na.amazon-adsystem.com/e/ir?t=happylittletr-20&l=am2&o=1&a=B0027A3G4S" width="1" height="1" border="0" alt="" style="border:none !important; margin:0px !important;" />"""],
        'Mountain Mixture': ['http://amzn.to/2rZ93nK',
                             """<a target="_blank" href="https://www.amazon.com/gp/product/B0027IUSF0/ref=as_li_tl?ie=UTF8&camp=1789&creative=9325&creativeASIN=B0027IUSF0&linkCode=as2&tag=happylittletr-20&linkId=748d93b215527ece07eb14813d0cfbaa">Bob Ross MR6020 37-Ml Artist Oil Color, Mountain Mixture</a><img src="//ir-na.amazon-adsystem.com/e/ir?t=happylittletr-20&l=am2&o=1&a=B0027IUSF0" width="1" height="1" border="0" alt="" style="border:none !important; margin:0px !important;" />"""],
        'Prussian Blue': ['http://amzn.to/2tlzUyB',
                          """<a target="_blank" href="https://www.amazon.com/gp/product/B004O79Q3C/ref=as_li_tl?ie=UTF8&camp=1789&creative=9325&creativeASIN=B004O79Q3C&linkCode=as2&tag=happylittletr-20&linkId=837f1c395a2c078caf3812a37b9d42fe">Winton Oil Paint 37ml/Tube-Prussian Blue</a><img src="//ir-na.amazon-adsystem.com/e/ir?t=happylittletr-20&l=am2&o=1&a=B004O79Q3C" width="1" height="1" border="0" alt="" style="border:none !important; margin:0px !important;" />"""],
        'Prusian Blue': ['http://amzn.to/2tlzUyB',
                          """<a target="_blank" href="https://www.amazon.com/gp/product/B004O79Q3C/ref=as_li_tl?ie=UTF8&camp=1789&creative=9325&creativeASIN=B004O79Q3C&linkCode=as2&tag=happylittletr-20&linkId=837f1c395a2c078caf3812a37b9d42fe">Winton Oil Paint 37ml/Tube-Prussian Blue</a><img src="//ir-na.amazon-adsystem.com/e/ir?t=happylittletr-20&l=am2&o=1&a=B004O79Q3C" width="1" height="1" border="0" alt="" style="border:none !important; margin:0px !important;" />"""],

        'Indian Yellow': ['http://amzn.to/2tilqPm',
                          """<a target="_blank" href="https://www.amazon.com/gp/product/B0027AEEGC/ref=as_li_tl?ie=UTF8&camp=1789&creative=9325&creativeASIN=B0027AEEGC&linkCode=as2&tag=happylittletr-20&linkId=d4b729bf567017814054f00b086252aa">Bob Ross MR6070 37-Ml Artist Oil Color, Indian Yellow</a><img src="//ir-na.amazon-adsystem.com/e/ir?t=happylittletr-20&l=am2&o=1&a=B0027AEEGC" width="1" height="1" border="0" alt="" style="border:none !important; margin:0px !important;" />"""],
        'Sap Green': ['http://amzn.to/2tVmjuW',
                      """<a target="_blank" href="https://www.amazon.com/gp/product/B0052XYDIU/ref=as_li_tl?ie=UTF8&camp=1789&creative=9325&creativeASIN=B0052XYDIU&linkCode=as2&tag=happylittletr-20&linkId=5f8fc03d6ecde9201853414e9b6a4ff0">Winsor &amp; Newton Winton Oil Colour Tube, 37ml, Sap Green</a><img src="//ir-na.amazon-adsystem.com/e/ir?t=happylittletr-20&l=am2&o=1&a=B0052XYDIU" width="1" height="1" border="0" alt="" style="border:none !important; margin:0px !important;" />"""],
        'Titanium White': ['http://amzn.to/2sYIQH2',
                           """<a target="_blank" href="https://www.amazon.com/gp/product/B0044JPSDW/ref=as_li_tl?ie=UTF8&camp=1789&creative=9325&creativeASIN=B0044JPSDW&linkCode=as2&tag=happylittletr-20&linkId=85cd12fe1d08ab8097d42b3bbff66971">Winsor &amp; Newton Winton 200-Milliliter Oil Paint, Titanium White</a><img src="//ir-na.amazon-adsystem.com/e/ir?t=happylittletr-20&l=am2&o=1&a=B0044JPSDW" width="1" height="1" border="0" alt="" style="border:none !important; margin:0px !important;" />"""],
        'Magic White': ['http://amzn.to/2sk2uLL',
                        """<a target="_blank" href="https://www.amazon.com/gp/product/B0027A3F6W/ref=as_li_tl?ie=UTF8&camp=1789&creative=9325&creativeASIN=B0027A3F6W&linkCode=as2&tag=happylittletr-20&linkId=9cac9076701d57d506089efe2d8dbf0f">Martin/ F. Weber Bob Ross 236-Ml Oil Paint, Liquid White</a><img src="//ir-na.amazon-adsystem.com/e/ir?t=happylittletr-20&l=am2&o=1&a=B0027A3F6W" width="1" height="1" border="0" alt="" style="border:none !important; margin:0px !important;" />"""],
        'Yellow Ochre': ['http://amzn.to/2sk2H1v',
                         """<a target="_blank" href="https://www.amazon.com/gp/product/B004IXDHNM/ref=as_li_tl?ie=UTF8&camp=1789&creative=9325&creativeASIN=B004IXDHNM&linkCode=as2&tag=happylittletr-20&linkId=aaa0950e553ef4aaba6b3db266b8a7ea">Winsor &amp; Newton Winton Oil Colour Tube, 37ml, Yellow Ochre</a><img src="//ir-na.amazon-adsystem.com/e/ir?t=happylittletr-20&l=am2&o=1&a=B004IXDHNM" width="1" height="1" border="0" alt="" style="border:none !important; margin:0px !important;" />"""],
        'Thalo Blue': ['http://amzn.to/2tV2Iee',
                       """<a target="_blank" href="https://www.amazon.com/gp/product/B0009IL2N2/ref=as_li_tl?ie=UTF8&camp=1789&creative=9325&creativeASIN=B0009IL2N2&linkCode=as2&tag=happylittletr-20&linkId=9c88b153936c5921f78e84f064e19d6f">Winton Oil Paint 37ml Tube: Phthalo Blue</a><img src="//ir-na.amazon-adsystem.com/e/ir?t=happylittletr-20&l=am2&o=1&a=B0009IL2N2" width="1" height="1" border="0" alt="" style="border:none !important; margin:0px !important;" />"""],
        'Pthalo Blue': ['http://amzn.to/2tV2Iee',
                       """<a target="_blank" href="https://www.amazon.com/gp/product/B0009IL2N2/ref=as_li_tl?ie=UTF8&camp=1789&creative=9325&creativeASIN=B0009IL2N2&linkCode=as2&tag=happylittletr-20&linkId=9c88b153936c5921f78e84f064e19d6f">Winton Oil Paint 37ml Tube: Phthalo Blue</a><img src="//ir-na.amazon-adsystem.com/e/ir?t=happylittletr-20&l=am2&o=1&a=B0009IL2N2" width="1" height="1" border="0" alt="" style="border:none !important; margin:0px !important;" />"""],
        'Thalo Green': ['http://amzn.to/2sYGFn8',
                        """<a target="_blank" href="https://www.amazon.com/gp/product/B001JPIQ2O/ref=as_li_tl?ie=UTF8&camp=1789&creative=9325&creativeASIN=B001JPIQ2O&linkCode=as2&tag=happylittletr-20&linkId=201795ad28afca3898f835fb3540b703">M. Graham Artist Oil Paint Phthalo Green 1.25oz/37ml Tube</a><img src="//ir-na.amazon-adsystem.com/e/ir?t=happylittletr-20&l=am2&o=1&a=B001JPIQ2O" width="1" height="1" border="0" alt="" style="border:none !important; margin:0px !important;" />"""],
        'Pthalo Green': ['http://amzn.to/2sYGFn8',
                        """<a target="_blank" href="https://www.amazon.com/gp/product/B001JPIQ2O/ref=as_li_tl?ie=UTF8&camp=1789&creative=9325&creativeASIN=B001JPIQ2O&linkCode=as2&tag=happylittletr-20&linkId=201795ad28afca3898f835fb3540b703">M. Graham Artist Oil Paint Phthalo Green 1.25oz/37ml Tube</a><img src="//ir-na.amazon-adsystem.com/e/ir?t=happylittletr-20&l=am2&o=1&a=B001JPIQ2O" width="1" height="1" border="0" alt="" style="border:none !important; margin:0px !important;" />"""],
        'Cad Yellow': ['http://amzn.to/2tVdWPX',
                       """<a target="_blank" href="https://www.amazon.com/gp/product/B0009IL2JG/ref=as_li_tl?ie=UTF8&camp=1789&creative=9325&creativeASIN=B0009IL2JG&linkCode=as2&tag=happylittletr-20&linkId=1d4e4ce111220c9076059a038543f8d8">Winsor &amp; Newton Winton 37-Milliliter Oil Paint, Cadmium Yellow Light</a><img src="//ir-na.amazon-adsystem.com/e/ir?t=happylittletr-20&l=am2&o=1&a=B0009IL2JG" width="1" height="1" border="0" alt="" style="border:none !important; margin:0px !important;" />"""],
        'Russian Blue': ['http://amzn.to/2tlzUyB',
                         """<a target="_blank" href="https://www.amazon.com/gp/product/B004O79Q3C/ref=as_li_tl?ie=UTF8&camp=1789&creative=9325&creativeASIN=B004O79Q3C&linkCode=as2&tag=happylittletr-20&linkId=837f1c395a2c078caf3812a37b9d42fe">Winton Oil Paint 37ml/Tube-Prussian Blue</a><img src="//ir-na.amazon-adsystem.com/e/ir?t=happylittletr-20&l=am2&o=1&a=B004O79Q3C" width="1" height="1" border="0" alt="" style="border:none !important; margin:0px !important;" />"""],
        'Crimson': ['http://amzn.to/2tlQbDK',
                    """<a target="_blank" href="https://www.amazon.com/gp/product/B004O79MIQ/ref=as_li_tl?ie=UTF8&camp=1789&creative=9325&creativeASIN=B004O79MIQ&linkCode=as2&tag=happylittletr-20&linkId=8580e892cd9ad9100cea24434c338a0a">Winton Oil Paint 37ml/Tube-Permanent Alizarin Crimson</a><img src="//ir-na.amazon-adsystem.com/e/ir?t=happylittletr-20&l=am2&o=1&a=B004O79MIQ" width="1" height="1" border="0" alt="" style="border:none !important; margin:0px !important;" />"""],
        'Liquid White': ["http://amzn.to/2sWnnNB", """<a target="_blank" href="https://www.amazon.com/gp/product/B0027A3F6W/ref=as_li_tl?ie=UTF8&camp=1789&creative=9325&creativeASIN=B0027A3F6W&linkCode=as2&tag=happylittletr-20&linkId=1f9cb54f6f19faeb7613d0f5bf3e814d">Martin/ F. Weber Bob Ross 236-Ml Oil Paint, Liquid White</a><img src="//ir-na.amazon-adsystem.com/e/ir?t=happylittletr-20&l=am2&o=1&a=B0027A3F6W" width="1" height="1" border="0" alt="" style="border:none !important; margin:0px !important;" />"""],
        'Liquid Black': ["http://amzn.to/2u1xpBW", """<a target="_blank" href="https://www.amazon.com/gp/product/B00264189A/ref=as_li_tl?ie=UTF8&camp=1789&creative=9325&creativeASIN=B00264189A&linkCode=as2&tag=happylittletr-20&linkId=ed0c2f16e1e01b710dc9e63e75edd692">Martin/ F. Weber Bob Ross 236-Ml Oil Paint, Black</a><img src="//ir-na.amazon-adsystem.com/e/ir?t=happylittletr-20&l=am2&o=1&a=B00264189A" width="1" height="1" border="0" alt="" style="border:none !important; margin:0px !important;" />"""],
        'Black Gesso': ["http://amzn.to/2u1HBdN", """<a target="_blank" href="https://www.amazon.com/gp/product/B004MAQ8TG/ref=as_li_tl?ie=UTF8&camp=1789&creative=9325&creativeASIN=B004MAQ8TG&linkCode=as2&tag=happylittletr-20&linkId=4014f7dad6172c0bf8571ed03ba8aa78">Art Alternatives Black Acrylic Gesso - 16oz Jar</a><img src="//ir-na.amazon-adsystem.com/e/ir?t=happylittletr-20&l=am2&o=1&a=B004MAQ8TG" width="1" height="1" border="0" alt="" style="border:none !important; margin:0px !important;" />"""],
        'Liquid Clear': ["http://amzn.to/2u1B0A4", """<a target="_blank" href="https://www.amazon.com/gp/product/B0027A7BGM/ref=as_li_tl?ie=UTF8&camp=1789&creative=9325&creativeASIN=B0027A7BGM&linkCode=as2&tag=happylittletr-20&linkId=6d4b3f92a3f73c4e0e04866933201e3a">Martin/ F. Weber Bob Ross 236-Ml Oil Paint, Clear</a><img src="//ir-na.amazon-adsystem.com/e/ir?t=happylittletr-20&l=am2&o=1&a=B0027A7BGM" width="1" height="1" border="0" alt="" style="border:none !important; margin:0px !important;" />"""]
    }

    paints_dict_upper = {key.upper(): value for key, value in paints_dict.items()}

    def create_paints(self):
        for key, val in self.paints_dict.items():
            p, created = Paints.objects.get_or_create(color=key.upper(), amazon_link=val[0], amazon_html=val[1])
            if created:
                print("Created ", key)
            else:
                print(key, " already in models")
        return 0

    def get_yt_thumb(self, video_id):
        mq_thumb = "https://img.youtube.com/vi/" +  video_id + "/mqdefault.jpg"
        return mq_thumb

    def get_yt_link(self, vid_id):
        return "https://youtube.com/embed/" + vid_id

    def read_data_file(self, episode_path ):
        data_file_path = os.path.join(episode_path, 'data.txt')
        with open(data_file_path, 'r') as f:
            season_num = f.readline()[:-1]
            epi_num = f.readline()[:-1]
            vid_id = f.readline()[:-1]
        return season_num, epi_num, vid_id

    def get_title_season_episode(self, episode_dir):
        m = re.match(r"Bob Ross - (?P<title>[^\(]*)\(Season (?P<season>[0-9]+) Episode (?P<episode>[0-9]+)\)", episode_dir)
        return m.group('title')[:-1], m.group('season'), m.group('episode')

    def get_transcript(self, episode_dir, episode_name):
        transcript_path = os.path.join(episode_dir, episode_name+'.txt')
        with open(transcript_path, 'r') as f:
            text = ' '.join(f.readlines())
        return text

    def get_transcript_file(self, episode_dir, episode_name):
        transcript_path = os.path.join('bobross', 'media', 'transcripts', episode_name+'.txt')
        return transcript_path

    def get_cloud(self, episode_dir, episode_name, cloud_dir='bobross/media/wordclouds/'):
        cloud = os.path.join('bobross', 'media','wordclouds', episode_name + ".png")
        return cloud

    def get_paints(self, episode_dir):
        paints_path = os.path.join(episode_dir, "paint.txt")
        paint_info = {}
        with open(paints_path, 'r') as f:
            paints = f.readlines()
            paints = [p[:-1] for p in paints]
        for paint in paints:
            if paint in self.paints_dict_upper.keys():
                short_link = self.paints_dict_upper[paint][0]
                html_link = self.paints_dict_upper[paint][1]
                p = Paints.objects.get_or_create(
                    color=paint,
                    amazon_link=short_link,
                    amazon_html=html_link
                )
                paint_info[paint] = [short_link, html_link]
            else:
                print("Paint not found: ", paint)
        return paint_info

    def get_painting(self, epi_path, season, num):
        painting = os.path.join('bobross', 'media',
                                'finished_paintings', "painting" + season + "-" + num + ".jpg")
        return painting

    def _create_episode(self):
        #walk through data folder for each episode
        data_path = os.path.join(settings.PROJECT_PATH, 'bobross', 'data')
        for root, dirs, files in os.walk(data_path):
            #once inside of an epi directory, set episode fields
            for dirname in dirs:
                if dirname.startswith('Bob Ross -'): # we are at an episode directory
                    epi_path = os.path.join(root, dirname)
                    season_num, episode, vid_id = self.read_data_file(epi_path)
                    title, season, episode_num = self.get_title_season_episode(dirname)
                    print(dirname)
                    epi = Episode(title=title)
                    epi.episode_number = episode_num # get from filename
                    epi.season = season  # get from filename
                    epi.yt_link = self.get_yt_link(vid_id) #get from vid id
                    epi.wordcloud = self.get_cloud(epi_path, dirname)#get from directory
                    epi.transcript = self.get_transcript(epi_path, dirname)#get from directory
                    epi.transcript_file = self.get_transcript_file(epi_path, dirname)#serve as static file
                    epi.thumbnail = self.get_yt_thumb(vid_id) #get from yt id
                    epi.painting = self.get_painting(epi_path, season, episode_num)
                    epi.save()
                    for paint, links in self.get_paints(epi_path).items():
                        p, created = Paints.objects.get_or_create(color=paint, amazon_link=links[0], amazon_html=links[1])
                        if created:
                            p.save()
                        epi.paints.add(p)

    def handle(self, *args, **options):
        self.create_paints()
        #FIX create manytomany
        self._create_episode()

