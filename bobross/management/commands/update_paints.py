import os
import shutil
import regex as re
from django.conf import settings
from django.core.management.base import BaseCommand

from bobross.models import Paints


class Command(BaseCommand):
    # args = '<foo bar ...>'
    help = 'Use this to update paint links for amzn to https'

    paints_dict = {
        'Phthalo Blue': ['https://amzn.to/2tV2Iee',
                         """<a target="_blank" href="https://www.amazon.com/gp/product/B0009IL2N2/ref=as_li_tl?ie=UTF8&camp=1789&creative=9325&creativeASIN=B0009IL2N2&linkCode=as2&tag=happylittletr-20&linkId=9c88b153936c5921f78e84f064e19d6f">Winton Oil Paint 37ml Tube: Phthalo Blue</a><img src="//ir-na.amazon-adsystem.com/e/ir?t=happylittletr-20&l=am2&o=1&a=B0009IL2N2" width="1" height="1" border="0" alt="" style="border:none !important; margin:0px !important;" />"""],
        'Van Dyke Brown': ['https://amzn.to/2sYpBNW',
                           """<a target="_blank" href="https://www.amazon.com/gp/product/B004O7BQF8/ref=as_li_tl?ie=UTF8&camp=1789&creative=9325&creativeASIN=B004O7BQF8&linkCode=as2&tag=happylittletr-20&linkId=e2cc7b132f02774b8aa23bdcc55f2745">Winton Oil Paint 37ml/Tube-Vandyke Brown</a><img src="//ir-na.amazon-adsystem.com/e/ir?t=happylittletr-20&l=am2&o=1&a=B004O7BQF8" width="1" height="1" border="0" alt="" style="border:none !important; margin:0px !important;" />"""],
        'Alizarin Crimson': ['https://amzn.to/2tlQbDK',
                             """<a target="_blank" href="https://www.amazon.com/gp/product/B004O79MIQ/ref=as_li_tl?ie=UTF8&camp=1789&creative=9325&creativeASIN=B004O79MIQ&linkCode=as2&tag=happylittletr-20&linkId=8580e892cd9ad9100cea24434c338a0a">Winton Oil Paint 37ml/Tube-Permanent Alizarin Crimson</a><img src="//ir-na.amazon-adsystem.com/e/ir?t=happylittletr-20&l=am2&o=1&a=B004O79MIQ" width="1" height="1" border="0" alt="" style="border:none !important; margin:0px !important;" />"""],
        'Midnight Black': ['https://amzn.to/2ufBL4q',
                           """<a target="_blank" href="https://www.amazon.com/gp/product/B0027AEEB2/ref=as_li_tl?ie=UTF8&camp=1789&creative=9325&creativeASIN=B0027AEEB2&linkCode=as2&tag=happylittletr-20&linkId=987f5f4313abbfdd58a22edb3f2662b2">Bob Ross MR6004 37-Ml Artist Oil Color, Midnight Black</a><img src="//ir-na.amazon-adsystem.com/e/ir?t=happylittletr-20&l=am2&o=1&a=B0027AEEB2" width="1" height="1" border="0" alt="" style="border:none !important; margin:0px !important;" />"""],
        'Bright Red': ['https://amzn.to/2tlCEvQ',
                       """<a target="_blank" href="https://www.amazon.com/gp/product/B001E1TGHW/ref=as_li_tl?ie=UTF8&camp=1789&creative=9325&creativeASIN=B001E1TGHW&linkCode=as2&tag=happylittletr-20&linkId=3581088b6e63dbfa3a3a74332d38f3ad">Winsor &amp; Newton Artists Oil Color Paint Tube, 37ml, Bright Red</a><img src="//ir-na.amazon-adsystem.com/e/ir?t=happylittletr-20&l=am2&o=1&a=B001E1TGHW" width="1" height="1" border="0" alt="" style="border:none !important; margin:0px !important;" />"""],
        'Permanent Red': ['https://amzn.to/2tlCEvQ',
                       """<a target="_blank" href="https://www.amazon.com/gp/product/B001E1TGHW/ref=as_li_tl?ie=UTF8&camp=1789&creative=9325&creativeASIN=B001E1TGHW&linkCode=as2&tag=happylittletr-20&linkId=3581088b6e63dbfa3a3a74332d38f3ad">Winsor &amp; Newton Artists Oil Color Paint Tube, 37ml, Bright Red</a><img src="//ir-na.amazon-adsystem.com/e/ir?t=happylittletr-20&l=am2&o=1&a=B001E1TGHW" width="1" height="1" border="0" alt="" style="border:none !important; margin:0px !important;" />"""],
        'Phthalo Green': ['https://amzn.to/2sYGFn8',
                          """<a target="_blank" href="https://www.amazon.com/gp/product/B001JPIQ2O/ref=as_li_tl?ie=UTF8&camp=1789&creative=9325&creativeASIN=B001JPIQ2O&linkCode=as2&tag=happylittletr-20&linkId=201795ad28afca3898f835fb3540b703">M. Graham Artist Oil Paint Phthalo Green 1.25oz/37ml Tube</a><img src="//ir-na.amazon-adsystem.com/e/ir?t=happylittletr-20&l=am2&o=1&a=B001JPIQ2O" width="1" height="1" border="0" alt="" style="border:none !important; margin:0px !important;" />"""],
        'Cadmium Yellow': ['https://amzn.to/2tVdWPX',
                           """<a target="_blank" href="https://www.amazon.com/gp/product/B0009IL2JG/ref=as_li_tl?ie=UTF8&camp=1789&creative=9325&creativeASIN=B0009IL2JG&linkCode=as2&tag=happylittletr-20&linkId=1d4e4ce111220c9076059a038543f8d8">Winsor &amp; Newton Winton 37-Milliliter Oil Paint, Cadmium Yellow Light</a><img src="//ir-na.amazon-adsystem.com/e/ir?t=happylittletr-20&l=am2&o=1&a=B0009IL2JG" width="1" height="1" border="0" alt="" style="border:none !important; margin:0px !important;" />"""],
        'Dark Sienna': ['https://amzn.to/2rZwQ76',
                        """<a target="_blank" href="https://www.amazon.com/gp/product/B0027A3G4S/ref=as_li_tl?ie=UTF8&camp=1789&creative=9325&creativeASIN=B0027A3G4S&linkCode=as2&tag=happylittletr-20&linkId=f2c5fde46159db0b7d8eda05c22413f8">Bob Ross MR6001 37-Ml Artist Oil Color, Dark Sienna</a><img src="//ir-na.amazon-adsystem.com/e/ir?t=happylittletr-20&l=am2&o=1&a=B0027A3G4S" width="1" height="1" border="0" alt="" style="border:none !important; margin:0px !important;" />"""],
        'Mountain Mixture': ['https://amzn.to/2rZ93nK',
                             """<a target="_blank" href="https://www.amazon.com/gp/product/B0027IUSF0/ref=as_li_tl?ie=UTF8&camp=1789&creative=9325&creativeASIN=B0027IUSF0&linkCode=as2&tag=happylittletr-20&linkId=748d93b215527ece07eb14813d0cfbaa">Bob Ross MR6020 37-Ml Artist Oil Color, Mountain Mixture</a><img src="//ir-na.amazon-adsystem.com/e/ir?t=happylittletr-20&l=am2&o=1&a=B0027IUSF0" width="1" height="1" border="0" alt="" style="border:none !important; margin:0px !important;" />"""],
        'Prussian Blue': ['https://amzn.to/2tlzUyB',
                          """<a target="_blank" href="https://www.amazon.com/gp/product/B004O79Q3C/ref=as_li_tl?ie=UTF8&camp=1789&creative=9325&creativeASIN=B004O79Q3C&linkCode=as2&tag=happylittletr-20&linkId=837f1c395a2c078caf3812a37b9d42fe">Winton Oil Paint 37ml/Tube-Prussian Blue</a><img src="//ir-na.amazon-adsystem.com/e/ir?t=happylittletr-20&l=am2&o=1&a=B004O79Q3C" width="1" height="1" border="0" alt="" style="border:none !important; margin:0px !important;" />"""],
        'Prusian Blue': ['https://amzn.to/2tlzUyB',
                          """<a target="_blank" href="https://www.amazon.com/gp/product/B004O79Q3C/ref=as_li_tl?ie=UTF8&camp=1789&creative=9325&creativeASIN=B004O79Q3C&linkCode=as2&tag=happylittletr-20&linkId=837f1c395a2c078caf3812a37b9d42fe">Winton Oil Paint 37ml/Tube-Prussian Blue</a><img src="//ir-na.amazon-adsystem.com/e/ir?t=happylittletr-20&l=am2&o=1&a=B004O79Q3C" width="1" height="1" border="0" alt="" style="border:none !important; margin:0px !important;" />"""],

        'Indian Yellow': ['https://amzn.to/2tilqPm',
                          """<a target="_blank" href="https://www.amazon.com/gp/product/B0027AEEGC/ref=as_li_tl?ie=UTF8&camp=1789&creative=9325&creativeASIN=B0027AEEGC&linkCode=as2&tag=happylittletr-20&linkId=d4b729bf567017814054f00b086252aa">Bob Ross MR6070 37-Ml Artist Oil Color, Indian Yellow</a><img src="//ir-na.amazon-adsystem.com/e/ir?t=happylittletr-20&l=am2&o=1&a=B0027AEEGC" width="1" height="1" border="0" alt="" style="border:none !important; margin:0px !important;" />"""],
        'Sap Green': ['https://amzn.to/2tVmjuW',
                      """<a target="_blank" href="https://www.amazon.com/gp/product/B0052XYDIU/ref=as_li_tl?ie=UTF8&camp=1789&creative=9325&creativeASIN=B0052XYDIU&linkCode=as2&tag=happylittletr-20&linkId=5f8fc03d6ecde9201853414e9b6a4ff0">Winsor &amp; Newton Winton Oil Colour Tube, 37ml, Sap Green</a><img src="//ir-na.amazon-adsystem.com/e/ir?t=happylittletr-20&l=am2&o=1&a=B0052XYDIU" width="1" height="1" border="0" alt="" style="border:none !important; margin:0px !important;" />"""],
        'Titanium White': ['https://amzn.to/2sYIQH2',
                           """<a target="_blank" href="https://www.amazon.com/gp/product/B0044JPSDW/ref=as_li_tl?ie=UTF8&camp=1789&creative=9325&creativeASIN=B0044JPSDW&linkCode=as2&tag=happylittletr-20&linkId=85cd12fe1d08ab8097d42b3bbff66971">Winsor &amp; Newton Winton 200-Milliliter Oil Paint, Titanium White</a><img src="//ir-na.amazon-adsystem.com/e/ir?t=happylittletr-20&l=am2&o=1&a=B0044JPSDW" width="1" height="1" border="0" alt="" style="border:none !important; margin:0px !important;" />"""],
        'Magic White': ['https://amzn.to/2sk2uLL',
                        """<a target="_blank" href="https://www.amazon.com/gp/product/B0027A3F6W/ref=as_li_tl?ie=UTF8&camp=1789&creative=9325&creativeASIN=B0027A3F6W&linkCode=as2&tag=happylittletr-20&linkId=9cac9076701d57d506089efe2d8dbf0f">Martin/ F. Weber Bob Ross 236-Ml Oil Paint, Liquid White</a><img src="//ir-na.amazon-adsystem.com/e/ir?t=happylittletr-20&l=am2&o=1&a=B0027A3F6W" width="1" height="1" border="0" alt="" style="border:none !important; margin:0px !important;" />"""],
        'Yellow Ochre': ['https://amzn.to/2sk2H1v',
                         """<a target="_blank" href="https://www.amazon.com/gp/product/B004IXDHNM/ref=as_li_tl?ie=UTF8&camp=1789&creative=9325&creativeASIN=B004IXDHNM&linkCode=as2&tag=happylittletr-20&linkId=aaa0950e553ef4aaba6b3db266b8a7ea">Winsor &amp; Newton Winton Oil Colour Tube, 37ml, Yellow Ochre</a><img src="//ir-na.amazon-adsystem.com/e/ir?t=happylittletr-20&l=am2&o=1&a=B004IXDHNM" width="1" height="1" border="0" alt="" style="border:none !important; margin:0px !important;" />"""],
        'Thalo Blue': ['https://amzn.to/2tV2Iee',
                       """<a target="_blank" href="https://www.amazon.com/gp/product/B0009IL2N2/ref=as_li_tl?ie=UTF8&camp=1789&creative=9325&creativeASIN=B0009IL2N2&linkCode=as2&tag=happylittletr-20&linkId=9c88b153936c5921f78e84f064e19d6f">Winton Oil Paint 37ml Tube: Phthalo Blue</a><img src="//ir-na.amazon-adsystem.com/e/ir?t=happylittletr-20&l=am2&o=1&a=B0009IL2N2" width="1" height="1" border="0" alt="" style="border:none !important; margin:0px !important;" />"""],
        'Pthalo Blue': ['https://amzn.to/2tV2Iee',
                       """<a target="_blank" href="https://www.amazon.com/gp/product/B0009IL2N2/ref=as_li_tl?ie=UTF8&camp=1789&creative=9325&creativeASIN=B0009IL2N2&linkCode=as2&tag=happylittletr-20&linkId=9c88b153936c5921f78e84f064e19d6f">Winton Oil Paint 37ml Tube: Phthalo Blue</a><img src="//ir-na.amazon-adsystem.com/e/ir?t=happylittletr-20&l=am2&o=1&a=B0009IL2N2" width="1" height="1" border="0" alt="" style="border:none !important; margin:0px !important;" />"""],
        'Thalo Green': ['https://amzn.to/2sYGFn8',
                        """<a target="_blank" href="https://www.amazon.com/gp/product/B001JPIQ2O/ref=as_li_tl?ie=UTF8&camp=1789&creative=9325&creativeASIN=B001JPIQ2O&linkCode=as2&tag=happylittletr-20&linkId=201795ad28afca3898f835fb3540b703">M. Graham Artist Oil Paint Phthalo Green 1.25oz/37ml Tube</a><img src="//ir-na.amazon-adsystem.com/e/ir?t=happylittletr-20&l=am2&o=1&a=B001JPIQ2O" width="1" height="1" border="0" alt="" style="border:none !important; margin:0px !important;" />"""],
        'Pthalo Green': ['https://amzn.to/2sYGFn8',
                        """<a target="_blank" href="https://www.amazon.com/gp/product/B001JPIQ2O/ref=as_li_tl?ie=UTF8&camp=1789&creative=9325&creativeASIN=B001JPIQ2O&linkCode=as2&tag=happylittletr-20&linkId=201795ad28afca3898f835fb3540b703">M. Graham Artist Oil Paint Phthalo Green 1.25oz/37ml Tube</a><img src="//ir-na.amazon-adsystem.com/e/ir?t=happylittletr-20&l=am2&o=1&a=B001JPIQ2O" width="1" height="1" border="0" alt="" style="border:none !important; margin:0px !important;" />"""],
        'Cad Yellow': ['https://amzn.to/2tVdWPX',
                       """<a target="_blank" href="https://www.amazon.com/gp/product/B0009IL2JG/ref=as_li_tl?ie=UTF8&camp=1789&creative=9325&creativeASIN=B0009IL2JG&linkCode=as2&tag=happylittletr-20&linkId=1d4e4ce111220c9076059a038543f8d8">Winsor &amp; Newton Winton 37-Milliliter Oil Paint, Cadmium Yellow Light</a><img src="//ir-na.amazon-adsystem.com/e/ir?t=happylittletr-20&l=am2&o=1&a=B0009IL2JG" width="1" height="1" border="0" alt="" style="border:none !important; margin:0px !important;" />"""],
        'Russian Blue': ['https://amzn.to/2tlzUyB',
                         """<a target="_blank" href="https://www.amazon.com/gp/product/B004O79Q3C/ref=as_li_tl?ie=UTF8&camp=1789&creative=9325&creativeASIN=B004O79Q3C&linkCode=as2&tag=happylittletr-20&linkId=837f1c395a2c078caf3812a37b9d42fe">Winton Oil Paint 37ml/Tube-Prussian Blue</a><img src="//ir-na.amazon-adsystem.com/e/ir?t=happylittletr-20&l=am2&o=1&a=B004O79Q3C" width="1" height="1" border="0" alt="" style="border:none !important; margin:0px !important;" />"""],
        'Crimson': ['https://amzn.to/2tlQbDK',
                    """<a target="_blank" href="https://www.amazon.com/gp/product/B004O79MIQ/ref=as_li_tl?ie=UTF8&camp=1789&creative=9325&creativeASIN=B004O79MIQ&linkCode=as2&tag=happylittletr-20&linkId=8580e892cd9ad9100cea24434c338a0a">Winton Oil Paint 37ml/Tube-Permanent Alizarin Crimson</a><img src="//ir-na.amazon-adsystem.com/e/ir?t=happylittletr-20&l=am2&o=1&a=B004O79MIQ" width="1" height="1" border="0" alt="" style="border:none !important; margin:0px !important;" />"""],
        'Liquid White': ["https://amzn.to/2sWnnNB", """<a target="_blank" href="https://www.amazon.com/gp/product/B0027A3F6W/ref=as_li_tl?ie=UTF8&camp=1789&creative=9325&creativeASIN=B0027A3F6W&linkCode=as2&tag=happylittletr-20&linkId=1f9cb54f6f19faeb7613d0f5bf3e814d">Martin/ F. Weber Bob Ross 236-Ml Oil Paint, Liquid White</a><img src="//ir-na.amazon-adsystem.com/e/ir?t=happylittletr-20&l=am2&o=1&a=B0027A3F6W" width="1" height="1" border="0" alt="" style="border:none !important; margin:0px !important;" />"""],
        'Liquid Black': ["https://amzn.to/2u1xpBW", """<a target="_blank" href="https://www.amazon.com/gp/product/B00264189A/ref=as_li_tl?ie=UTF8&camp=1789&creative=9325&creativeASIN=B00264189A&linkCode=as2&tag=happylittletr-20&linkId=ed0c2f16e1e01b710dc9e63e75edd692">Martin/ F. Weber Bob Ross 236-Ml Oil Paint, Black</a><img src="//ir-na.amazon-adsystem.com/e/ir?t=happylittletr-20&l=am2&o=1&a=B00264189A" width="1" height="1" border="0" alt="" style="border:none !important; margin:0px !important;" />"""],
        'Black Gesso': ["https://amzn.to/2u1HBdN", """<a target="_blank" href="https://www.amazon.com/gp/product/B004MAQ8TG/ref=as_li_tl?ie=UTF8&camp=1789&creative=9325&creativeASIN=B004MAQ8TG&linkCode=as2&tag=happylittletr-20&linkId=4014f7dad6172c0bf8571ed03ba8aa78">Art Alternatives Black Acrylic Gesso - 16oz Jar</a><img src="//ir-na.amazon-adsystem.com/e/ir?t=happylittletr-20&l=am2&o=1&a=B004MAQ8TG" width="1" height="1" border="0" alt="" style="border:none !important; margin:0px !important;" />"""],
        'Liquid Clear': ["https://amzn.to/2u1B0A4", """<a target="_blank" href="https://www.amazon.com/gp/product/B0027A7BGM/ref=as_li_tl?ie=UTF8&camp=1789&creative=9325&creativeASIN=B0027A7BGM&linkCode=as2&tag=happylittletr-20&linkId=6d4b3f92a3f73c4e0e04866933201e3a">Martin/ F. Weber Bob Ross 236-Ml Oil Paint, Clear</a><img src="//ir-na.amazon-adsystem.com/e/ir?t=happylittletr-20&l=am2&o=1&a=B0027A7BGM" width="1" height="1" border="0" alt="" style="border:none !important; margin:0px !important;" />"""]
    }

    paints_dict_upper = {key.upper(): value for key, value in paints_dict.items()}

    def update_paints(self):
        p = Paints.object.all()
        for p1 in p:
            s = p1.amazon_link
            s1 = list(s[:4])
            s2 = list(s[4:])
            p1.amazon_link = ''.join(s1 + ['s'] + s2)
            p1.save()



def handle(self, *args, **options):
    self.update_paints()
    # FIX create manytomany

