from pathlib import Path
from html import escape as e
import json, os
ROOT=Path(__file__).parent
PHOTOS=json.loads((ROOT/"assets/photo-sources.json").read_text(encoding='utf8'))
YT='https://www.youtube.com/@GogaMeskhiOfficial'; FB='https://www.facebook.com/gogameskhi86'; SP='https://open.spotify.com/track/38Nr0ZsrmhwKEgu7J1WgQF'
FORTUNA='https://fortuna.ge/'; TBI='https://tbiliselebi.ge/ka/news/show-business/'

# ---------------------------------------------------------------------------
# SEO configuration. See SEO-REPORT.md for how each value was verified.
# ---------------------------------------------------------------------------
SITE = 'https://gogameskhi.com'          # production origin; must match the CNAME file
PERSON_ID = SITE + '/#person'            # one identifier for the artist on every page
WEBSITE_ID = SITE + '/#website'
# Profiles confirmed to belong to the artist. Instagram and Amazon Music stay out
# until they are confirmed (see RESEARCH-SOURCES.md).
YT_CHANNEL = 'https://www.youtube.com/channel/UCNU6GugDOPRzOXqNmVPieRA'
SPOTIFY_ARTIST = 'https://open.spotify.com/artist/1CK6M44gPDtqCTHxJq44NI'
SAME_AS = [YT, YT_CHANNEL, FB, SPOTIFY_ARTIST]
# Typographic share card. It contains no photograph, so no photo licence is needed.
SHARE = dict(url=SITE + '/assets/goga-meskhi-share-card.png', w=1200, h=630, mime='image/png')
# Upload time, duration and largest available thumbnail, read from each video's
# YouTube page on 2026-11-22. All eight are on the official channel above.
VIDEO = {
    'TZKdkyT1gds': dict(uploaded='2026-11-19T11:29:08-08:00', duration='PT3M22S', thumb=('maxresdefault', 1280, 720)),
    'IPtHxz2tNIQ': dict(uploaded='2025-01-23T10:36:58-08:00', duration='PT3M49S', thumb=('sddefault', 640, 480)),
    'TzgvbnIbC88': dict(uploaded='2025-01-27T06:45:06-08:00', duration='PT3M19S', thumb=('maxresdefault', 1280, 720)),
    'ime1fuc-Fh4': dict(uploaded='2026-02-03T21:45:03-08:00', duration='PT3M59S', thumb=('maxresdefault', 1280, 720)),
    '62JjHrVYlcQ': dict(uploaded='2025-02-02T05:00:06-08:00', duration='PT3M53S', thumb=('sddefault', 640, 480)),
    'CByIEf4zfBo': dict(uploaded='2025-02-09T05:43:43-08:00', duration='PT4M17S', thumb=('sddefault', 640, 480)),
    'TlpW6A1lR84': dict(uploaded='2025-03-08T22:00:06-08:00', duration='PT3M37S', thumb=('maxresdefault', 1280, 720)),
    'DN3_Drt9_Co': dict(uploaded='2025-03-21T00:45:06-07:00', duration='PT3M25S', thumb=('maxresdefault', 1280, 720)),
}
# Second performer on the duets, as credited on the track pages.
FEAT = {'davbrundebi': ('Keti Chanturidze', 'ქეთი ჭანტურიძე'),
        'momenatre-da-movedi': ('Nanuka Karukhnishvili', 'ნანუკა ქარუხნიშვილი')}
# Page <title> and meta description: (title en, title ka, description en, description ka).
# Keyword ownership is documented in SEO-KEYWORDS.md to limit cannibalization between pages.
PAGE_META = {
    'index': ('Goga Meskhi — Georgian singer, actor and recording artist',
              'გოგა მესხი — ქართველი მომღერალი და მსახიობი | ოფიციალური ვებგვერდი',
              'Official website of Georgian recording artist Goga Meskhi (გოგა მესხი) — singer and actor: explore songs, music, videos, biography and concerts.',
              'გოგა მესხი მომღერალი და გოგა მესხი მსახიობი — ოფიციალური ვებგვერდი: სიმღერები, მუსიკა, ვიდეოკლიპები, ბიოგრაფია და კონცერტები.'),
    'music': ('Goga Meskhi songs and music — catalogue | Georgian recordings',
              'გოგა მესხი სიმღერები და მუსიკა — კატალოგი | ქართული ჩანაწერები',
              'Explore Goga Meskhi songs: original recordings, duets and reinterpretations of Georgian music, each with credits and a link to listen.',
              'გოგა მესხი სიმღერები და მუსიკა — ქართული ჩანაწერები, დუეტები და ინტერპრეტაციები, კრედიტებითა და მოსასმენი ბმულებით.'),
    'videos': ('Goga Meskhi music videos — performances and clips',
               'გოგა მესხი — ვიდეოკლიპები და შესრულებები',
               'Watch Goga Meskhi music videos and performance recordings, including Chamotova Isev, Melikishvili Avenue, Chemo Aprilo and more.',
               'უყურე გოგა მესხის ვიდეოკლიპებსა და შესრულების ჩანაწერებს — „ჩამოთოვა ისევ“, „მელიქიშვილის გამზირი“, „დაღამებულხარ, ჩემო აპრილო“ და სხვა.'),
    'listen': ('Listen to Goga Meskhi — YouTube, Spotify and streaming',
               'გოგა მესხი მუსიკა — მოსასმენი არხები და სტრიმინგი',
               'Where to listen to Goga Meskhi music online: YouTube, Facebook, Spotify and Amazon Music, plus Radio Fortuna premieres and interviews.',
               'სად მოისმინო გოგა მესხის მუსიკა: YouTube, Facebook, Spotify და Amazon Music, ასევე რადიო „ფორტუნას“ პრემიერები და ინტერვიუები.'),
    'live': ('Goga Meskhi concerts — live performances and booking',
             'გოგა მესხი კონცერტი — ცოცხალი შესრულება და მოწვევა',
             'Goga Meskhi concert appearances with the Tbilisi Symphony Orchestra and at Black Sea Arena, plus how to send a booking inquiry.',
             'გოგა მესხის კონცერტები და ცოცხალი გამოსვლები თბილისის სიმფონიურ ორკესტრთან და „ბლექ სი არენაზე“; ინფორმაცია მოწვევისთვის.'),
    'about': ('Goga Meskhi biography — Georgian singer and actor',
              'გოგა მესხის ბიოგრაფია — მომღერალი და მსახიობი',
              'Goga Meskhi biography — Georgian singer and actor: from the vocal group Vivo and The Voice of Georgia to orchestral concerts and new recordings.',
              'გოგა მესხის ბიოგრაფია — ქართველი მომღერალი და მსახიობი: ჯგუფ „ვივოდან“, „ახალი ხმიდან“ სიმფონიურ კონცერტებამდე და ახალ ჩანაწერებამდე.'),
    'stories': ('Song stories — Goga Meskhi and Georgian music',
                'სიმღერების ისტორიები — გოგა მესხი და ქართული მუსიკა',
                'The stories behind Goga Meskhi songs: people, places and memories connected to Melikishvili Avenue, Chamotova Isev and Chemo Aprilo.',
                'გოგა მესხის სიმღერების ისტორიები — ადამიანები, ადგილები და მოგონებები „მელიქიშვილის გამზირზე“, „ჩამოთოვა ისევს“ და „დაღამებულხარ, ჩემო აპრილოზე“.'),
    'press': ('Goga Meskhi in the press — interviews and media',
              'გოგა მესხი მედიაში — ინტერვიუები და პუბლიკაციები',
              'Interviews, appearances and music premieres featuring Georgian singer Goga Meskhi — Fortuna, Tbiliselebi, Ambebi.ge and 1TV.',
              'გოგა მესხი მედიაში: ქართველი მომღერალი გოგა მესხი — რჩეული ინტერვიუები და მუსიკალური პრემიერები.'),
    'contact': ('Contact Goga Meskhi — concerts and booking',
                'გოგა მესხი — კონტაქტი, კონცერტი და მოწვევა',
                'Contact Goga Meskhi about concerts, festivals, collaborations and media requests. Draft your message here and send it via Facebook.',
                'დაუკავშირდი გოგა მესხს კონცერტის მოწვევის, ფესტივალის, თანამშრომლობისა და მედიის მოთხოვნისთვის — შეტყობინება Facebook-ზე.'),
    'privacy': ('Privacy | Goga Meskhi',
                'კონფიდენციალურობა | გოგა მესხი',
                'How the Goga Meskhi website handles information: the inquiry form stays in your browser, there is no analytics tracking, and videos play through YouTube.',
                'როგორ მუშავდება ინფორმაცია გოგა მესხის ვებგვერდზე: ფორმის ტექსტი მხოლოდ ბრაუზერში რჩება, ანალიტიკური თვალთვალი არ არის, ვიდეოები YouTube-ით იკვრება.'),
    '404': ('Page not found | Goga Meskhi', 'გვერდი ვერ მოიძებნა | გოგა მესხი',
            'This page does not exist. Go to the Goga Meskhi homepage.', 'გვერდი ვერ მოიძებნა. გადადი გოგა მესხის მთავარ გვერდზე.'),
}
# Primary/secondary keywords per page stem (used by seo_keyword_audit.py). Track pages use TRACK_KEYWORDS below.
PAGE_KEYWORDS = {
    'index': dict(primary_en=['Goga Meskhi'], secondary_en=['Georgian singer', 'Georgian recording artist', 'Goga Meskhi actor'],
                primary_ka=['გოგა მესხი'], secondary_ka=['ქართველი მომღერალი', 'გოგა მესხი მომღერალი', 'გოგა მესხი მსახიობი']),
    'music': dict(primary_en=['Goga Meskhi songs', 'Goga Meskhi music'], secondary_en=['Georgian music', 'Goga Meskhi'],
                primary_ka=['გოგა მესხი სიმღერები', 'გოგა მესხი მუსიკა'], secondary_ka=['ქართული მუსიკა', 'გოგა მესხი']),
    'videos': dict(primary_en=['Goga Meskhi music videos'], secondary_en=['Goga Meskhi', 'Georgian music'],
                primary_ka=['გოგა მესხი'], secondary_ka=['ვიდეოკლიპები', 'ქართული მუსიკა']),
    'listen': dict(primary_en=['Listen to Goga Meskhi'], secondary_en=['Goga Meskhi music', 'Goga Meskhi songs', 'Georgian music'],
                primary_ka=['გოგა მესხი მუსიკა'], secondary_ka=['გოგა მესხი', 'ქართული მუსიკა']),
    'live': dict(primary_en=['Goga Meskhi concert'], secondary_en=['Goga Meskhi', 'Georgian singer', 'Georgian music'],
               primary_ka=['გოგა მესხი კონცერტი'], secondary_ka=['გოგა მესხი', 'ქართველი მომღერალი']),
    'about': dict(primary_en=['Goga Meskhi biography'], secondary_en=['Goga Meskhi singer', 'Goga Meskhi actor', 'Georgian singer'],
                primary_ka=['გოგა მესხის ბიოგრაფია'], secondary_ka=['გოგა მესხი მომღერალი', 'გოგა მესხი მსახიობი', 'ქართველი მომღერალი']),
    'stories': dict(primary_en=['Song stories'], secondary_en=['Goga Meskhi', 'Georgian music', 'Goga Meskhi songs'],
                   primary_ka=['სიმღერების ისტორიები'], secondary_ka=['გოგა მესხი', 'ქართული მუსიკა']),
    'press': dict(primary_en=['Goga Meskhi'], secondary_en=['Georgian singer', 'Goga Meskhi music', 'Georgian music'],
                 primary_ka=['გოგა მესხი'], secondary_ka=['ქართველი მომღერალი', 'ქართული მუსიკა']),
    'contact': dict(primary_en=['Contact Goga Meskhi'], secondary_en=['Goga Meskhi concert', 'Goga Meskhi', 'Georgian singer'],
                   primary_ka=['გოგა მესხი'], secondary_ka=['კონტაქტი', 'გოგა მესხი კონცერტი']),
    'privacy': dict(primary_en=['Goga Meskhi'], secondary_en=[], primary_ka=['გოგა მესხი'], secondary_ka=[]),
}
# Schema.org type for each top-level page; everything else is a plain WebPage.
PAGE_TYPE = {'about': 'ProfilePage', 'contact': 'ContactPage', 'music': 'CollectionPage', 'videos': 'CollectionPage',
             'stories': 'CollectionPage', 'press': 'CollectionPage', 'listen': 'CollectionPage'}
UTILITY = {'privacy'}                    # crawlable, but left out of sitemap.xml
SITEMAP = []                             # filled by Site.frame: (canonical URL, {lang: URL})
press=[('Fortuna','2026-02-04','A new video in memory of Mamuka Onashvili','მამუკა ონაშვილის ხსოვნისადმი მიძღვნილი კლიპი',FORTUNA+'video-cremlnarevi-da-sevdiani-emociebi-gvqonda-mamuka-gamicockhle-da-didi-ram-gaakete-chemtviso-mikharia-rom-es-shevdzeli-goga-meskhis-midzghvna-mamuka-onashvils-da/'),('Fortuna','2025-09','Chamiara: a new song premiere','„ჩამიარა“ — სიმღერის პრემიერა',FORTUNA+'dzalian-sheviyvare-es-simghera-aseti-damokidebuleba-arcert-simgheraze-ar-mqonia-misamgheri-mesizmreboda-da-es-raghac-skhvas-nishnavs-goga-meskhi-premierit-ar-dai/'),('Fortuna','2022-09','Melikishvili Avenue and the stories behind the songs','მელიქიშვილის გამზირი და სიმღერების ისტორიები',FORTUNA+'goga-meskhi-meliqishvilis-gamziri-chems-simgherebshi-calke-dgas-radgan-chems-zura-doijashvils-edzghvneba-kargi-gamokhmaureba-hqonda-magram-iyo-iseti-raghacebi-ramac-guli-matki-2/'),('Tbiliselebi','2024','The story behind Chamotova Isev','„ჩამოთოვა ისევ“ — სიმღერის ისტორია',TBI+'rogor-igrdzno-30-tslis-tsin-dakarguli-mamis-siakhlove-goga-meskhma-da-ra-sastsaulit-gadaurcha-is-orjer-sikvdils'),('Fortuna','2025','A conversation about music and The Voice','საუბარი მუსიკასა და „ახალ ხმაზე“',FORTUNA+'goga-meskhi-meored-rom-davojakhdi-mashin-gaigo-khalkhma-rom-pirvel-meughles-davshordi/')]
tracks=[dict(slug='ar-makhsovs',en='I Don’t Remember',ka='არ მახსოვს',year='YouTube',cat='recording',img='ar-makhsovs',id='TZKdkyT1gds',desc=("Goga Meskhi performs I Don’t Remember (არ მახსოვს / Ar Makhsovs) — listen to the official recording on YouTube.",'გოგა მესხის შესრულება — „არ მახსოვს“ (I Don’t Remember). ოფიციალური ჩანაწერი YouTube-ზე.'),credits=[],source=1,source_url='https://www.youtube.com/watch?v=TZKdkyT1gds'),dict(slug='chamotova-isev',en='Chamotova Isev',ka='ჩამოთოვა ისევ',year='2022 / 2025',cat='interpretation',img='snow',id='IPtHxz2tNIQ',desc=('A reinterpretation of a Georgian composition by Mamuka Charkviani, with poetry by Jansugh Charkviani and a new visual treatment. The official video was published in January 2025.','მამუკა ჩარკვიანის კომპოზიციის ახალი ინტერპრეტაცია ჯანსუღ ჩარკვიანის ლექსზე. ოფიციალური ვიდეო 2025 წლის იანვარში გამოქვეყნდა.'),credits=[('Composer','კომპოზიტორი','Mamuka Charkviani','მამუკა ჩარკვიანი'),('Lyrics','ლექსი','Jansugh Charkviani','ჯანსუღ ჩარკვიანი'),('Arrangement','არანჟირება','Zaza Marjanishvili','ზაზა მარჯანიშვილი')],source=3),dict(slug='melikishvili-avenue',en='Melikishvili Avenue',ka='მელიქიშვილის გამზირი',year='2025 video',cat='interpretation',img='avenue',id='TzgvbnIbC88',desc=('A tribute to Goga’s friend, Georgian singer Zura Doijashvili. The recording connects a familiar Tbilisi street with the memories and music of the city.','გოგას მეგობრის, ქართველი მომღერლის ზურა დოიჯაშვილის ხსოვნისადმი მიძღვნილი სიმღერა. ჩანაწერი თბილისის ნაცნობ ქუჩას ქალაქის მოგონებებსა და მუსიკასთან აკავშირებს.'),credits=[('Dedication','მიძღვნა','Zura Doijashvili','ზურა დოიჯაშვილი')],spotify=SP,source=2),dict(slug='chemo-aprilo',en='Chemo Aprilo',ka='დაღამებულხარ, ჩემო აპრილო',year='2026 video',cat='interpretation',img='april',id='ime1fuc-Fh4',desc=('A new visual interpretation of a song by Soso Ebralidze, dedicated to the memory of Mamuka Onashvili. The tribute video was presented in 2026.','სოსო ებრალიძის სიმღერის ახალი ვიზუალური ინტერპრეტაცია, რომელიც მამუკა ონაშვილის ხსოვნას ეძღვნება. ვიდეოკლიპი 2026 წელს წარადგინეს.'),credits=[('Composer','კომპოზიტორი','Soso Ebralidze','სოსო ებრალიძე'),('Lyrics','ლექსი','Vakhtang Gogolashvili','ვახტანგ გოგოლაშვილი'),('Version','ვერსია','Mamuka Onashvili','მამუკა ონაშვილი')],source=0)]
nav=[('index','Home','მთავარი'),('music','Music','მუსიკა'),('videos','Videos','ვიდეოები'),('live','Live','კონცერტები'),('about','About','ბიოგრაფია'),('stories','Stories','ისტორიები'),('press','Press','მედია'),('contact','Contact','კონტაქტი')]
stories=[('melikishvili-avenue','A song for Tbilisi','სიმღერა თბილისისთვის','The story of Melikishvili Avenue.','მელიქიშვილის გამზირის ისტორია.','story-city',tracks[2]),('ar-makhsovs','I Don’t Remember','არ მახსოვს','The story behind Goga Meskhi’s recording I Don’t Remember (არ მახსოვს).','გოგა მესხის ჩანაწერი „არ მახსოვს“ (I Don’t Remember) და მისი კონტექსტი.','ar-makhsovs',tracks[0]),('chamotova-isev','A familiar song, a new vision','ნაცნობი სიმღერა, ახალი ხედვა','A new interpretation of Chamotova Isev.','„ჩამოთოვა ისევ“ — ახალი ინტერპრეტაცია.','snow',tracks[1]),('chemo-aprilo','Remembering Mamuka','მამუკას ხსოვნისთვის','A musical tribute to Mamuka Onashvili.','მამუკა ონაშვილის ხსოვნისადმი მიძღვნილი სიმღერა.','april',tracks[3])]

IG='https://www.instagram.com/gogameskhi/'
AM='https://music.amazon.com/tracks/B0GMYTCKPL'
RADIO='https://fortuna.ge/ardaidardo-tag/goga-meskhi/'
BSA='https://bsa.ge/ge/events/kakhidze'
ORCH='https://1tv.ge/news/bleq-si-arena-dghes-jansugh-da-vakhtang-kakhidzeebis-simgherebis-saghamos-umaspindzlebs/'
BELLA='https://yolo.ge/en/poster/charity-concert-bella-and-her-friends434564565'
AMB='https://www.ambebi.ge/article/89582-goga-meskhi-qmaia-darsmelidzem-ar-vici-thavis-gundshi-ratom-amiyvanaq/'
SARK='https://sarkenews.ge/2021/06/goga-meskhis-deda-chemi-meughle-gaqra-chemthvis-samqharo-chamoiqtsa-sabtchotha-estradis-varskvlavis-tskhovrebis-gza/'
DUET='https://fortuna.ge/jerjerobit-duetze-var-gadartuli-ar-aris-aucilebeli-solo-kariera-gavagrdzelo-goga-meskhi/'
OLD='https://www.ambebi.ge/article/43647-goga-mesxma-sevdiani-simgera-qopil-sheqvarebuls-miuzgvna/'
press.extend([
 ('Radio Fortuna','2023-10-19','A duet with Nanuka Karukhnishvili','დუეტი ნანუკა ქარუხნიშვილთან',DUET),
 ('Ambebi.ge','2011-11-02','The making of Nu Damemdurebi','„ნუ დამემდურები“ — კლიპის ისტორია',OLD),
 ('Ambebi.ge','2013','The Voice: Maia Darsmelidze’s team','„ახალი ხმა“ — მაია დარსმელიძის გუნდი',AMB),
 ('Black Sea Arena','2019-08-17','Jansugh and Vakhtang Kakhidze concert','ჯანსუღ და ვახტანგ კახიძეების შემოქმედებითი საღამო',BSA),
 ('1TV','2019-08-17','Symphonic and jazz-folk repertoire at Black Sea Arena','სიმფონიური და ჯაზ-ფოლკ პროგრამა „ბლექ სი არენაზე“',ORCH),
 ('Radio Fortuna','2017','Tbilisi Symphony Orchestra concert','თბილისის სიმფონიური ორკესტრის კონცერტი',FORTUNA+'tbilisis-simfoniuri-orkestris-koncerti-gaimarta/'),
 ('Sarke','2021-06','A musical family and the beginnings of Vivo','მუსიკალური ოჯახი და ჯგუფი „ვივო“',SARK),
 ('Radio Fortuna','2024','A new version of Chamotova featuring its composer','„ჩამოთოვა“ — ახალი ვერსია ავტორის მონაწილეობით',FORTUNA+'video-goga-meskhma-mamuka-charkvianis-simghera-chamotova-akhali-versiit-sheasrula-da-klipi-gadaigho/'),
 ('YOLO','2026-04-04','Bella and Her Friends — charity concert listing','„ბელა და მეგობრები“ — საქველმოქმედო კონცერტის აფიშა',BELLA),
 ('Radio Fortuna','2016-01-25','Datuna Mgeladze recalls the band Vivo','დათუნა მგელაძე ჯგუფ „ვივოს“ იხსენებს',FORTUNA+'dzalian-gamimarthla-radgan-shesarchevze-300-000-mde-adamiani-iyo-math-shoris-bevri-qarthveli/')])
tracks[1]['credits'] += [('Recording studio','ჩამწერი სტუდია','Zura Makhniashvili','ზურა მახნიაშვილი'),('Video directors','კლიპის რეჟისორები','Zura Vasadze, Sergo Egoiani, Giorgi Ivanishvili','ზურა ვასაძე, სერგო ეგოიანი, გიორგი ივანიშვილი')]
tracks[2]['credits'] += [('Arrangement / studio','არანჟირება / სტუდია','Zura Makhniashvili','ზურა მახნიაშვილი'),('Version','ვერსია','Zaza Tsurtsumia','ზაზა წურწუმია'),('Illustrations','ილუსტრაციები','Nona Giunashvili','ნონა გიუნაშვილი')]
tracks.extend([
 dict(slug='imgere-rame',en='Imgere Rame',ka='იმღერე რამე',year='2025 video',cat='interpretation',img='imgere',id='62JjHrVYlcQ',desc=('A performance of Gogi Tsabadze’s classic, dedicated to the memory of Gio Khutsishvili. It was performed on radio in 2022; the official video followed in February 2025.','გოგი ცაბაძის სიმღერის შესრულება გიო ხუციშვილის ხსოვნისადმი. 2022 წელს შესრულდა რადიოეთერში; ოფიციალური ვიდეო 2025 წლის თებერვალში გამოქვეყნდა.'),credits=[('Music','მუსიკა','Gogi Tsabadze','გოგი ცაბაძე'),('Lyrics','ტექსტი','Petre Gruzinsky','პეტრე გრუზინსკი'),('Arrangement','არანჟირება','Zura Makhniashvili','ზურა მახნიაშვილი'),('Director','რეჟისორი','Beka Shakashvili','ბექა შაკაშვილი')],source=2),
 dict(slug='nu-damemdurebi',en='Nu Damemdurebi',ka='ნუ დამემდურები',year='2011 / 2025',cat='original',img='nu',id='CByIEf4zfBo',desc=('An early song in Goga’s solo career. The music video directed by Dachi Darchia was reported in 2011 and uploaded to his channel in February 2025.','გოგას სოლო კარიერის ადრეული სიმღერა. დაჩი დარჩიას გადაღებული კლიპის შესახებ 2011 წელს დაიწერა; ვიდეო არხზე 2025 წლის თებერვალში გამოქვეყნდა.'),credits=[('Music','მუსიკა','Zura Menteshashvili','ზურა მენთეშაშვილი'),('Lyrics (official video credit)','ტექსტი (ვიდეოს მიხედვით)','Vasil Beselia','ვასილ ბესელია'),('Arrangement','არანჟირება','Paata Patsuria','პაატა ფაცურია'),('Director','რეჟისორი','Dachi Darchia','დაჩი დარჩია')],source=6),
 dict(slug='momenatre-da-movedi',en='Momenatre da Movedi',ka='მომენატრე და მოვედი',year='2023',cat='duet',img='duet',id=None,external=DUET,desc=('A duet with Nanuka Karukhnishvili, premiered on Radio Ar Daidardo on 13 October 2023. The two singers developed a joint project with their own band.','დუეტი ნანუკა ქარუხნიშვილთან, რომლის პრემიერაც რადიო „არ დაიდარდოში“ 2023 წლის 13 ოქტომბერს გაიმართა. მომღერლებმა ერთობლივი პროექტი საკუთარ ბენდთან ერთად წამოიწყეს.'),credits=[('Vocals','ვოკალი','Goga Meskhi & Nanuka Karukhnishvili','გოგა მესხი და ნანუკა ქარუხნიშვილი'),('Lyrics','ტექსტი','Irina Sanikidze','ირინა სანიკიძე'),('Studio','სტუდია','Zura Makhniashvili','ზურა მახნიაშვილი')],source=5)])
PHOTOS.update({'imgere':'https://i.ytimg.com/vi/62JjHrVYlcQ/hqdefault.jpg','nu':'https://i.ytimg.com/vi/CByIEf4zfBo/hqdefault.jpg'})
channels=[('YouTube','01','Official artist channel','ოფიციალური არტისტის არხი',YT),('Facebook','02','Artist’s social page','არტისტის სოციალური გვერდი',FB),('Instagram','03','Handle cited in 2022 media; current status unconfirmed','2022 წლის მედიაში მითითებული ანგარიში; მიმდინარე სტატუსი დაუდასტურებელია',IG),('Spotify','04','Melikishvili Avenue · track','მელიქიშვილის გამზირი · სიმღერა',SP),('Amazon Music','05','Album listing via Passed Me By; availability may vary','ალბომის ჩანაწერი Passed Me By-ის გვერდზე; ხელმისაწვდომობა შესაძლოა განსხვავდებოდეს',AM),('Radio Fortuna','06','Radio premieres, audio and interviews','რადიოპრემიერები, აუდიო და ინტერვიუები',RADIO)]
album=[('I Don’t Remember','03:31'),('Melikishvili Avenue','03:15'),('My Heart Kept Waiting','03:48'),('Don’t Be Hard On Me','04:18'),('Passed Me By','04:24'),('Back To You','03:36'),('Snow Falls Again','04:21'),('When Tomorrow Comes','03:32')]
nav.insert(3,('listen','Listen & follow','არხები'))
KETI='https://fortuna.ge/duetad-ukve-didi-khania-chamovyalibdit-goga-meskhi-da-qeti-chanturidze-premierit-ar-daidardoshi-2/'
press.append(('Radio Fortuna','2021-12-01','Davbrundebi — collaboration with Keti Chanturidze','„დავბრუნდები“ — თანამშრომლობა ქეთი ჭანტურიძესთან',KETI))
tracks.extend([dict(slug='davbrundebi',en='Davbrundebi',ka='დავბრუნდები',year='2021 / 2025',cat='duet',img='davbrundebi',id='TlpW6A1lR84',desc=('A collaboration with Keti Chanturidze, first presented on Radio Ar Daidardo in November 2021. Their official YouTube upload followed on 8 March 2025.','დუეტი ქეთი ჭანტურიძესთან, რომლის პრემიერაც რადიო „არ დაიდარდოში“ 2021 წლის ნოემბერში შედგა. ოფიციალური YouTube ვიდეო 2025 წლის 8 მარტს გამოქვეყნდა.'),credits=[('Vocals','ვოკალი','Goga Meskhi & Keti Chanturidze','გოგა მესხი და ქეთი ჭანტურიძე'),('Music and lyrics','მუსიკა და ტექსტი','Zura Managadze','ზურა მანაგაძე'),('Arrangement','არანჟირება','Zura Makhniashvili','ზურა მახნიაშვილი'),('Guitar','გიტარა','Dato Londaridze','დათო ლონდარიძე'),('Concept','იდეა','Leri Robakidze','ლერი რობაქიძე')],source=len(press)-1),dict(slug='khval-daitskos',en='Khval Daitskos',ka='ხვალ დაიწყოს',year='2025 audio',cat='original',img='khval',id='DN3_Drt9_Co',desc=('An official audio recording published on 21 March 2025. Maiko Katchkatchishvili’s music and Nana Tsintsadze’s lyrics are joined by saxophone from Zura Makhniashvili.','ოფიციალური აუდიოჩანაწერი, რომელიც 2025 წლის 21 მარტს გამოქვეყნდა. მაიკო კაჭკაჭიშვილის მუსიკასა და ნანა ცინცაძის ტექსტს ზურა მახნიაშვილის საქსოფონი აერთიანებს.'),credits=[('Music','მუსიკა','Maiko Katchkatchishvili','მაიკო კაჭკაჭიშვილი'),('Lyrics','ტექსტი','Nana Tsintsadze','ნანა ცინცაძე'),('Arrangement','არანჟირება','Paata Patsuria','პაატა ფაცურია'),('Saxophone','საქსოფონი','Zura Makhniashvili','ზურა მახნიაშვილი')],source=4)])
tracks[-1]['source_url']='https://www.youtube.com/watch?v=DN3_Drt9_Co'
tracks[2]['credits'] += [('Music','მუსიკა','Zura Managadze','ზურა მანაგაძე'),('Lyrics','ტექსტი','Murman Lebanidze, Nana Tsintsadze','მურმან ლებანიძე, ნანა ცინცაძე'),('Trumpet','საყვირი','Giorgi Tskhvariashvili','გიორგი ცხვარიაშვილი'),('Director','რეჟისორი','Beka Gachechiladze','ბექა გაჩეჩილაძე'),('Editing','მონტაჟი','Beka Shakashvili','ბექა შაკაშვილი'),('Producer','პროდიუსერი','Misha Gachechiladze','მიშა გაჩეჩილაძე')]
PHOTOS.update({'davbrundebi':'https://i.ytimg.com/vi/TlpW6A1lR84/hqdefault.jpg','khval':'https://i.ytimg.com/vi/DN3_Drt9_Co/hqdefault.jpg'})
# Per-track keyword ownership: song title is primary; artist name is secondary (songs hub keeps “Goga Meskhi songs”).
TRACK_KEYWORDS = {tr['slug']: dict(primary_en=[tr['en']], primary_ka=[tr['ka']],
                                    secondary_en=[tr['ka'], tr['en'], 'Goga Meskhi'],
                                    secondary_ka=[tr['en'], 'გოგა მესხი']) for tr in tracks}
STORY_KEYWORDS = {}
for s in stories:
    tr = s[6]
    STORY_KEYWORDS[s[0]] = dict(primary_en=[s[1], tr['en']], primary_ka=[s[2], tr['ka']],
                                secondary_en=['Goga Meskhi', tr['ka']], secondary_ka=['გოგა მესხი', tr['en']])

# ---------------------------------------------------------------------------
# SEO helpers: canonical URLs, <head> metadata, structured data, sitemap
# ---------------------------------------------------------------------------
# Which recording each thumbnail belongs to, so alt text can name the song.
THUMB_TRACK = {tr['img']: tr for tr in tracks if tr.get('id')}
THUMB_TRACK.update({'story-city': tracks[2], 'video': tracks[1]})
COMPOSER = {'Composer', 'Music', 'Music and lyrics'}
LYRICIST = {'Lyrics', 'Lyrics (official video credit)', 'Music and lyrics'}


def absurl(stem='index', lang='en'):
    """Canonical absolute URL of a page. The English homepage is the site root."""
    if stem == 'index':
        return SITE + '/' if lang == 'en' else f'{SITE}/{lang}/'
    return f'{SITE}/{lang}/{stem}.html'


def is_video(tr):
    """Same rule as the Videos page: YouTube uploads, minus the audio-only release."""
    return bool(tr.get('id')) and tr['slug'] != 'khval-daitskos'


def thumb(ytid):
    name, w, h = VIDEO[ytid]['thumb']
    return dict(url=f'https://i.ytimg.com/vi/{ytid}/{name}.jpg', w=w, h=h, mime='image/jpeg')


def credit_people(tr, labels, ka):
    """People credited under the given labels on the track page, as schema.org Persons."""
    names = []
    for credit in tr['credits']:
        if credit[0] in labels:
            names += [n.strip() for n in credit[3 if ka else 2].split(',')]
    return [{'@type': 'Person', 'name': n} for n in names]


def recording_node(tr, site, compact=False):
    """MusicRecording for a track. The @id is the same in both languages."""
    ka = site.ka
    node = {'@type': 'MusicRecording', '@id': f'{SITE}/#recording-{tr["slug"]}', 'name': tr[site.lang],
            'alternateName': tr['en' if ka else 'ka'], 'url': absurl('music/' + tr['slug'], site.lang),
            'byArtist': {'@id': PERSON_ID}}
    if tr['slug'] in FEAT:
        node['byArtist'] = [{'@id': PERSON_ID}, {'@type': 'Person', 'name': FEAT[tr['slug']][ka]}]
    if compact:
        return node
    node['description'] = tr['desc'][ka]
    composers, lyricists = credit_people(tr, COMPOSER, ka), credit_people(tr, LYRICIST, ka)
    if composers or lyricists:
        work = {'@type': 'MusicComposition', 'name': tr[site.lang]}
        if composers:
            work['composer'] = composers
        if lyricists:
            work['lyricist'] = lyricists
        node['recordingOf'] = work
    same = [tr['spotify']] if tr.get('spotify') else []
    if tr.get('id'):
        node['image'] = thumb(tr['id'])['url']
        if is_video(tr):
            node['video'] = {'@id': f'{SITE}/#video-{tr["id"]}'}
        else:
            same.append('https://www.youtube.com/watch?v=' + tr['id'])
    if same:
        node['sameAs'] = same
    return node


def video_node(tr, site):
    """VideoObject for the YouTube video that the track page plays."""
    v = VIDEO[tr['id']]
    return {'@type': 'VideoObject', '@id': f'{SITE}/#video-{tr["id"]}',
            'name': f'{tr[site.lang]} — {site.t("Goga Meskhi", "გოგა მესხი")}', 'description': tr['desc'][site.ka],
            'thumbnailUrl': [thumb(tr['id'])['url'], f'https://i.ytimg.com/vi/{tr["id"]}/hqdefault.jpg'],
            'uploadDate': v['uploaded'], 'duration': v['duration'],
            'embedUrl': 'https://www.youtube.com/embed/' + tr['id']}


def item_list(site, entries):
    """ItemList of (name, absolute URL) pairs for a listing page."""
    return {'@type': 'ItemList', '@id': site.canonical + '#list',
            'itemListElement': [{'@type': 'ListItem', 'position': i, 'name': name, 'url': url}
                                for i, (name, url) in enumerate(entries, 1)]}


def build_graph(site, full, desc, crumbs, nodes, main, about, image):
    t, canon = site.t, site.canonical
    page_type = PAGE_TYPE.get(site.stem, 'WebPage')
    website = {'@type': 'WebSite', '@id': WEBSITE_ID, 'url': SITE + '/', 'name': 'Goga Meskhi',
               'alternateName': 'გოგა მესხი', 'inLanguage': ['en', 'ka'], 'publisher': {'@id': PERSON_ID}}
    person = {'@type': 'Person', '@id': PERSON_ID, 'name': t('Goga Meskhi', 'გოგა მესხი'),
              'alternateName': t('გოგა მესხი', 'Goga Meskhi'), 'givenName': t('Goga', 'გოგა'),
              'familyName': t('Meskhi', 'მესხი'),
              'description': t('Georgian singer and actor', 'ქართველი მომღერალი და მსახიობი'),
              'jobTitle': [t('Singer', 'მომღერალი'), t('Actor', 'მსახიობი')], 'url': SITE + '/',
              'mainEntityOfPage': absurl('about', site.lang), 'sameAs': SAME_AS}
    page = {'@type': page_type, '@id': canon + '#webpage', 'url': canon, 'name': full, 'description': desc,
            'inLanguage': site.lang, 'isPartOf': {'@id': WEBSITE_ID}}
    if site.stem not in UTILITY:
        page['about'] = [{'@id': i} for i in [PERSON_ID, *about]] if about else {'@id': PERSON_ID}
    if page_type == 'ProfilePage':
        main = PERSON_ID
    if main:
        page['mainEntity'] = {'@id': main}
    if image['url'] != SHARE['url']:
        page['primaryImageOfPage'] = {'@type': 'ImageObject', 'url': image['url'], 'width': image['w'], 'height': image['h']}
    graph = [website, person, page]
    if crumbs:
        page['breadcrumb'] = {'@id': canon + '#breadcrumb'}
        graph.append({'@type': 'BreadcrumbList', '@id': canon + '#breadcrumb',
                      'itemListElement': [{'@type': 'ListItem', 'position': i, 'name': name, 'item': url}
                                          for i, (name, url) in enumerate(crumbs, 1)]})
    return {'@context': 'https://schema.org', '@graph': graph + list(nodes)}


def build_head(site, full, desc, og_type, image, graph, og, extra, index):
    t, p, canon = site.t, site.prefix, site.canonical
    head = ['<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">'
            '<meta name="referrer" content="strict-origin-when-cross-origin">'
            f'<title>{e(full)}</title><meta name="description" content="{e(desc)}">']
    if not index:
        head.append('<meta name="robots" content="noindex, follow">')
    else:
        head.append('<meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1, max-video-preview:-1">')
        head.append(f'<link rel="canonical" href="{canon}">')
        if not site.duplicate:
            head += [f'<link rel="alternate" hreflang="{l}" href="{absurl(site.stem, l)}">' for l in ('ka', 'en')]
            head.append(f'<link rel="alternate" hreflang="x-default" href="{absurl(site.stem, "en")}">')
        props = [('og:site_name', t('Goga Meskhi', 'გოგა მესხი')), ('og:type', og_type), ('og:title', full),
                 ('og:description', desc), ('og:url', canon), ('og:locale', t('en_US', 'ka_GE')),
                 ('og:locale:alternate', t('ka_GE', 'en_US')), ('og:image', image['url']),
                 ('og:image:type', image['mime']), ('og:image:width', image['w']), ('og:image:height', image['h']),
                 ('og:image:alt', image['alt']), *og]
        head += [f'<meta property="{k}" content="{e(str(v))}">' for k, v in props]
        cards = [('twitter:card', 'summary_large_image'), ('twitter:title', full), ('twitter:description', desc),
                 ('twitter:image', image['url']), ('twitter:image:alt', image['alt'])]
        head += [f'<meta name="{k}" content="{e(str(v))}">' for k, v in cards]
    head.append('<meta name="theme-color" content="#111113">'
                f'<link rel="icon" href="{p}favicon.ico" sizes="32x32">'
                f'<link rel="icon" href="{p}assets/favicon.svg" type="image/svg+xml">'
                f'<link rel="apple-touch-icon" href="{p}assets/apple-touch-icon.png">'
                + extra +
                '<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
                '<link href="https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@700;800;900&family=Inter:wght@400;500;600;700;800&family=Noto+Sans+Georgian:wght@400;600;700;800;900&display=swap" rel="stylesheet">'
                f'<link rel="stylesheet" href="{p}assets/style.css">')
    if graph:
        head.append('<script type="application/ld+json">' + json.dumps(graph, ensure_ascii=False).replace('</', '<\\/') + '</script>')
    head.append(f'<script defer src="{p}assets/main.js"></script>')
    return ''.join(head)


def write_sitemap():
    """sitemap.xml: every canonical, indexable page with its language alternates."""
    rows = []
    for canon, alts, stem in sorted(SITEMAP, key=lambda x: (x[2] != 'index', x[2].count('/'), x[2], x[0])):
        if stem in UTILITY:
            continue
        links = ''.join(f'<xhtml:link rel="alternate" hreflang="{l}" href="{alts[l]}"/>' for l in ('ka', 'en'))
        links += f'<xhtml:link rel="alternate" hreflang="x-default" href="{alts["en"]}"/>'
        rows.append(f'  <url><loc>{canon}</loc>{links}</url>')
    xml = ('<?xml version="1.0" encoding="UTF-8"?>\n'
           '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">\n'
           + '\n'.join(rows) + '\n</urlset>\n')
    (ROOT / 'sitemap.xml').write_text(xml, encoding='utf8', newline='\n')


def write_robots():
    """robots.txt: pages are open; repository housekeeping files are not worth crawling."""
    lines = ['User-agent: *', 'Allow: /', 'Disallow: /build.py', 'Disallow: /make_preview.py', 'Disallow: /seo_check.py',
             'Disallow: /seo_keyword_audit.py', 'Disallow: /*.md$', '', f'Sitemap: {SITE}/sitemap.xml', '']
    (ROOT / 'robots.txt').write_text('\n'.join(lines), encoding='utf8', newline='\n')


class Site:
 def __init__(self,lang,path):
  self.lang=lang;self.ka=lang=='ka';self.path=Path(path);self.page=self.path.as_posix();self.prefix=os.path.relpath(ROOT, (ROOT/self.path).parent).replace(os.sep,'/')+'/';self.prefix='' if self.prefix=='./' else self.prefix;self.alt='en' if self.ka else 'ka'
  # GitHub Pages serves 404.html for any missing URL, so its links must be root-relative.
  if self.page=='404.html':self.prefix='/'
  self.stem={'index.html':'index','404.html':'404'}.get(self.page) or self.page.split('/',1)[1][:-5]
  # en/index.html repeats the root homepage; its canonical points at the root.
  self.duplicate=self.page=='en/index.html';self.canonical=absurl(self.stem,lang)
  # Attribute for elements whose whole text is a Georgian-script title on an English page.
  self.klang='' if self.ka else ' lang="ka"'
 def t(self,en,ka):return ka if self.ka else en
 def url(self,path='index',lang=None):
  # Homepages are linked as directories (the root and ka/) so internal links match the canonical URLs.
  lang=lang or self.lang
  if path=='index':return (self.prefix or './') if lang=='en' else self.prefix+'ka/'
  return self.prefix+lang+'/'+path+'.html'
 def thumbalt(self,tr):
  # Alt text names the song the thumbnail belongs to, instead of a generic "Music video thumbnail".
  return self.t(f'YouTube thumbnail for “{tr["en"]}” by Goga Meskhi',f'გოგა მესხი — „{tr["ka"]}“, YouTube-ის მინიატურა')
 def img(self,name,alt='',cls='',loading='eager',priority=False):
  labels={'portrait':('Portrait of Goga Meskhi. Photo: Tbiliselebi','გოგა მესხის პორტრეტი. ფოტო: თბილისელები'),'home-artist':('Goga Meskhi','გოგა მესხი'),'story-studio':('Radio Fortuna studio photograph','რადიო ფორტუნას სტუდიის ფოტო')}
  tr=THUMB_TRACK.get(name)
  if not alt:alt=self.thumbalt(tr) if tr else self.t(*labels.get(name,('Music video thumbnail','ვიდეოს მინიატურა')))
  # width/height let the browser reserve space before the image loads; priority marks the main image of a page.
  src=PHOTOS[name]
  if not src.startswith(('http://', 'https://')):
    src=f'{self.prefix}{src}'
  dims=' width="480" height="360"' if src.endswith('/hqdefault.jpg') else '';pri=' fetchpriority="high"' if priority else ''
  return f'<img src="{src}" data-fallback="{self.prefix}assets/image-fallback.svg" alt="{e(alt)}" class="{cls}" loading="{loading}" decoding="async"{dims}{pri}>'
 def ext(self,url,text,cls='textlink'):return f'<a class="{cls}" href="{e(url)}" target="_blank" rel="noopener noreferrer">{text} <span aria-hidden="true">↗</span></a>'
 def link(self,path,text,cls='textlink',aria=None):
  # aria: fuller accessible name for links whose visible text repeats in a list ("Song details", "Read story").
  label=f' aria-label="{e(aria)}"' if aria else ''
  return f'<a class="{cls}" href="{self.url(path)}"{label}>{text} <span aria-hidden="true">↗</span></a>'
 def watch(self,tr,cls='btn',label=None,named=False):
  if not tr.get('id'):return self.ext(tr['external'],self.t('Listen on radio','მოუსმინე რადიოში'),cls)
  # named=True is for lists, where several identical "Play" links need the song title to tell them apart.
  label=label or self.t("Listen now","მოუსმინე");aria=f' aria-label="{e(label+": "+tr[self.lang])}"' if named else ''
  return f'<a href="https://www.youtube.com/watch?v={tr["id"]}" class="{cls}" target="_blank" rel="noopener" data-video="{tr["id"]}" data-title="{e(tr[self.lang])}"{aria}><span aria-hidden="true">▶</span> {label}</a>'
 def other(self,text):
  # Georgian-script titles on English pages are marked up so screen readers and search engines read them as Georgian.
  return text if self.ka else f'<span lang="ka">{text}</span>'
 def cover(self,tr,loading='eager',priority=False):
  if not tr.get('id'):return f'<div class="cover duet-art"><span>GM × NK</span><small>{self.t("Radio duet / 2023","რადიო დუეტი / 2023")}</small></div>'
  return f'<div class="cover">{self.img(tr["img"],loading=loading,priority=priority)}<span class="cover-label">{self.t("Video thumbnail","ვიდეოს მინიატურა")}</span></div>'
 def track(self,tr,loading='eager'):return f'<article class="track" data-category="{tr["cat"]}"><a href="{self.url("music/"+tr["slug"])}" aria-label="{e(tr[self.lang])}">{self.cover(tr,loading)}</a><div class="track-copy"><h3><a href="{self.url("music/"+tr["slug"])}">{tr[self.lang]}</a></h3><p{self.klang}>{tr["en" if self.ka else "ka"]}</p>{self.watch(tr,"listen",named=True)}</div></article>'
 def eyebrow(self,text):return '<div class="eyebrow">'+text+'</div>'
 def sectionhead(self,label,title,more=''):return f'<div class="section-head"><div>{self.eyebrow(label)}<h2>{title}</h2></div>{more}</div>'
 def pagehero(self,label,title,desc):return f'<section class="pagehero"><div class="wrap">{self.eyebrow(label)}<h1>{title}</h1><p>{desc}</p></div></section>'
 def pressrows(self,n=None):return '<div class="presslist">'+''.join(f'<a class="pressrow" href="{e(p[4])}" target="_blank" rel="noopener noreferrer"><small>{p[0]}<br><time datetime="{p[1]}">{p[1]}</time></small><strong>{p[3 if self.ka else 2]}</strong><span aria-hidden="true">↗</span></a>' for p in press[:n])+'</div>'
 def storycard(self,s,loading='lazy'):return f'<article class="story"><a class="preview" href="{self.url("stories/"+s[0])}">{self.img(s[5],loading=loading)}</a><div>{self.eyebrow(self.t("Behind the song","სიმღერის ისტორია"))}<h3><a href="{self.url("stories/"+s[0])}">{s[2 if self.ka else 1]}</a></h3><p>{s[4 if self.ka else 3]}</p>{self.link("stories/"+s[0],self.t("Read story","წაიკითხე"),aria=self.t("Read story","წაიკითხე")+": "+s[2 if self.ka else 1])}</div></article>'
 def connect(self):return f'<section class="connect compact"><div class="wrap"><h2>{self.t("Let’s stay<br>in tune.","დარჩი<br>ჩვენთან რიტმში.")}</h2><div><p>{self.t("Follow Goga for new music, videos and performance announcements.","გამოიწერე გოგას არხები — ახალი სიმღერები, ვიდეოები და კონცერტების სიახლეები.")}</p><div class="actions">{self.ext(YT,self.t("Subscribe on YouTube","YouTube-ის გამოწერა"),"btn")}{self.ext(FB,self.t("Follow on Facebook","Facebook-ზე გამოწერა"),"btn ghost")}</div></div></div></section>'
 def frame(self,active,title,body,desc=None,full=None,og_type='website',image=None,nodes=(),main=None,about=(),crumbs=None,og=(),extra='',index=True):
  # title: short name used in breadcrumbs. full/desc: <title> and meta description (default: PAGE_META).
  # image: social card image. nodes/main/about: extra structured data. og: extra Open Graph properties.
  # extra: resource hints for <head>. index=False marks a utility page such as 404.
  stem=self.stem;name=self.t('Goga Meskhi','გოგა მესხი');meta=PAGE_META.get(stem,());full=full or self.t(*meta[:2]);desc=desc or self.t(*meta[2:]);label=lambda x:self.t(x[1],x[2]);navhtml=''.join(f'<a href="{self.url(n[0])}"'+(' aria-current="page"' if n[0]==active else '')+f'>{label(n)}</a>' for n in nav)
  langs=' / '.join(f'<a href="{self.url("index" if stem=="404" else stem,l)}" lang="{l}" hreflang="{l}"'+(' aria-current="true"' if self.lang==l else '')+f' aria-label="{lname}">{l.upper()}</a>' for l,lname in [('ka','ქართული'),('en','English')]);footer=''.join(f'<a href="{self.url(n[0])}">{label(n)}</a>' for n in nav[1:])
  image=dict(image or SHARE);image.setdefault('alt',self.t('Goga Meskhi — Georgian singer, actor and recording artist','გოგა მესხი — ქართველი მომღერალი და მსახიობი'))
  if crumbs is None and stem!='index':crumbs=[(self.t('Home','მთავარი'),absurl('index',self.lang)),(title,self.canonical)]
  if 'i.ytimg.com' in body or stem in ('index','live'):extra='<link rel="preconnect" href="https://i.ytimg.com">'+extra
  head=build_head(self,full,desc,og_type,image,build_graph(self,full,desc,crumbs,nodes,main,about,image) if index else None,og,extra,index)
  if index and not self.duplicate:SITEMAP.append((self.canonical,{l:absurl(stem,l) for l in ('ka','en')},stem))
  html=f'''<!doctype html><html lang="{self.lang}"><head>{head}</head><body><a class="skip" href="#main">{self.t('Skip to content','შინაარსზე გადასვლა')}</a><header class="top"><div class="wrap nav"><a class="logo" href="{self.url()}">GOGA MESKHI<b>.</b></a><nav id="nav" class="navlinks" aria-label="{self.t('Main navigation','მთავარი მენიუ')}">{navhtml}</nav><div class="lang">{langs}</div><button class="menubtn" aria-controls="nav" aria-expanded="false" aria-label="{self.t('Menu','მენიუ')}">☰</button></div></header><main id="main">{body}</main><footer class="footer"><div class="wrap"><div class="footer-top"><div><a class="logo" href="{self.url()}">GOGA MESKHI<b>.</b></a><small>{self.t('Singer / Actor / Performer','მომღერალი / მსახიობი / შემსრულებელი')}</small></div><nav aria-label="{self.t('Footer navigation','დამატებითი მენიუ')}">{footer}</nav><div><div class="socials">{self.ext(YT,'YouTube','')}{self.ext(FB,'Facebook','')}{self.ext(SP,'Spotify','')}{self.link('listen',self.t('All platforms','ყველა არხი'),'')}</div><small>{self.t('Georgian voice. Universal emotion.','ქართული ხმა. ემოცია საზღვრებს მიღმა.')}</small></div></div><div class="footer-bottom"><span>© {name} · {self.t('Website preview','ვებგვერდის სამუშაო ვერსია')}</span><span>{self.t('Photo usage rights pending approval','ფოტოების უფლებები დასაზუსტებელია')}</span><a class="privacy-link" href="{self.url('privacy')}">{self.t('Privacy','კონფიდენციალურობა')}</a></div></div></footer><dialog class="video-dialog" id="video-dialog" aria-labelledby="dialog-title"><div class="dialog-head"><strong class="dialog-title" id="dialog-title">{name}</strong><button class="close-dialog" aria-label="{self.t('Close video','ვიდეოს დახურვა')}">×</button></div><div class="video-frame"></div><div class="dialog-foot">{self.t('Playback is provided by YouTube.','ვიდეოს დაკვრა YouTube-ის საშუალებით ხდება.')} <a class="watch-external" href="{YT}" target="_blank" rel="noopener">{self.t('Watch on YouTube','უყურე YouTube-ზე')} ↗</a></div></dialog></body></html>'''
  dest=ROOT/self.path;dest.parent.mkdir(parents=True,exist_ok=True);dest.write_text(html,encoding='utf8')
 def home(self):
  t=self.t;tr=tracks[0];hero=f'''<section class="hero"><div class="wrap hero-content">{self.eyebrow(t('Georgian singer and recording artist','ქართველი მომღერალი'))}<h1><span>{t('GOGA','გოგა')}</span> <span>{t('MESKHI','მესხი')}<b style="color:var(--red)">.</b></span></h1><p>{t('Georgian voice.<br>Universal emotion.','ქართული ხმა.<br>ემოცია საზღვრებს მიღმა.')}</p><div class="hero-actions">{self.link('music',t('Goga Meskhi songs','სიმღერები'),'btn')}{self.link('about',t('Biography','ბიოგრაფია'),'btn ghost')}</div></div><div class="wrap hero-foot"><span>TBILISI / GEORGIA</span><span class="asset-note">{t('Stage photo: Fortuna','სცენის ფოტო: Fortuna')}</span></div></section><div class="strip"><div class="wrap"><span>GOGA MESKHI / გოგა მესხი</span><span>{t('Music · Live · Stories','მუსიკა · კონცერტები · ისტორიები')}</span></div></div>'''
  music=self.featured_music()+self.platform_strip()

  video=f'''<section class="cinema bgvideo"><div class="wrap cinema-grid"><div>{self.eyebrow(t('02 / Visual experiences','02 / ვიდეოები'))}<h2>{t('Music<br>in motion.','მუსიკა<br>კადრში.')}</h2><p>{t('Official music videos, live performances and the visual stories behind the songs.','ოფიციალური ვიდეოკლიპები, ცოცხალი შესრულება და სიმღერების ვიზუალური ისტორიები.')}</p><div class="actions">{self.link('videos',t('Explore videos','ყველა ვიდეო'),'btn ghost')}</div></div>{self.watch(tracks[1],'playbig',t('<span class="sr-only">Play video</span>','<span class="sr-only">ვიდეოს ნახვა</span>'))}</div></section>'''
  about=f'''<section class="section"><div class="wrap split"><div class="portrait">{self.img('home-artist',loading='lazy')}</div><div>{self.eyebrow(t('03 / The artist','03 / არტისტი'))}<h2>{t('More than<br>a voice.','მეტი, ვიდრე<br>ხმა.')}</h2><p>{t('From the group Vivo in 2003 and The Voice in 2013 to symphonic concerts at Black Sea Arena and contemporary recordings — Goga’s artistry bridges music, theatre and film.','2003 წელს ჯგუფ „ვივოდან“ და 2013 წელს „ახალი ხმიდან“ — „ბლექ სი არენას“ სიმფონიურ კონცერტებსა და თანამედროვე ჩანაწერებამდე. გოგას შემოქმედება მუსიკას, თეატრსა და კინოს აერთიანებს.')}</p>{self.link('about',t('Goga Meskhi biography','ბიოგრაფია'))}</div></div></section>'''
  live=f'''<section class="cinema bglive live"><div class="wrap"><div>{self.eyebrow(t('04 / Live experiences','04 / კონცერტები'))}<h2>{t('Feel it live.','იგრძენი ცოცხლად.')}</h2><p>{t('Concerts, special projects and international collaborations.','კონცერტები, სპეციალური პროექტები და საერთაშორისო თანამშრომლობა.')}</p><div class="actions">{self.link('live',t('Live & booking','კონცერტები და მოწვევა'),'btn')}{self.link('contact',t('Bring Goga to your city','მოიწვიე გოგა შენს ქალაქში'),'btn ghost')}</div></div></div></section>'''
  story=f'''<section class="section"><div class="wrap">{self.sectionhead(t('05 / The journal','05 / ისტორიები'),t('Behind the music.','მუსიკის მიღმა.'),self.link('stories',t('All stories','ყველა ისტორია')))}<div class="stories">{''.join(self.storycard(x) for x in stories[:2])}</div></div></section>'''
  pr=f'''<section class="compact" style="background:#e8e5e0"><div class="wrap">{self.sectionhead(t('06 / In the media','06 / მედია'),t('In the press.','პრესაში.'),self.link('press',t('Press & media','მედია და პრესა')))}{self.pressrows(3)}</div></section>'''
  # The hero photo is a CSS background, which browsers discover late; preloading it speeds up the first paint.
  self.frame('index',t('Goga Meskhi','გოგა მესხი'),hero+music+video+about+live+story+pr+self.connect(),extra=f'<link rel="preload" as="image" href="{PHOTOS["hero"]}" fetchpriority="high">')
 def music(self):
  t=self.t;f=''.join(f'<button class="filter {"active" if k=="all" else ""}" data-filter="{k}" aria-pressed="{"true" if k=="all" else "false"}">{t(en,ka)}</button>' for k,en,ka in [('all','All','ყველა'),('original','Original repertoire','ორიგინალური სიმღერები'),('interpretation','Interpretations','ინტერპრეტაციები'),('duet','Duets','დუეტები'),('recording','Other recordings','სხვა ჩანაწერები')]);body=self.pagehero('01 / '+t('Discography','დისკოგრაფია'),t('Goga Meskhi songs and music.','გოგა მესხი სიმღერები და მუსიკა.'),t('A catalogue of Goga Meskhi music: original songs, duets and reinterpretations of Georgian music.','გოგა მესხის მუსიკის კატალოგი — ორიგინალური სიმღერები, დუეტები და ქართული მუსიკის ინტერპრეტაციები.'))+f'<section class="section"><div class="wrap"><h2 class="sr-only">{t("Selected recordings","რჩეული ჩანაწერები")}</h2><div class="filters">{f}</div><div class="catalog">{"".join(self.track(x,"eager" if i<3 else "lazy") for i,x in enumerate(tracks))}</div></div></section>'+self.album_block()+self.platform_strip()+self.connect();self.frame('music',t('Music','მუსიკა'),body,nodes=[item_list(self,[(x[self.lang],absurl('music/'+x['slug'],self.lang)) for x in tracks])],main=self.canonical+'#list')
 def trackpage(self,tr):
  t=self.t;cred=''.join(f'<div><dt>{x[1 if self.ka else 0]}</dt><dd>{x[3 if self.ka else 2]}</dd></div>' for x in tr['credits']);source=press[tr['source']];body=self.pagehero(t('Music / Selected recordings','მუსიკა / რჩეული ჩანაწერები'),tr[self.lang],self.other(tr['en' if self.ka else 'ka'])+' · '+tr['year'])+f'<section class="section"><div class="wrap"><a class="textlink backlink" href="{self.url("music")}">← {t("Goga Meskhi songs","გოგა მესხის სიმღერები")}</a><div class="details">{self.cover(tr,priority=True)}<div><h2>{t("About the song","სიმღერის შესახებ")}</h2><p>{tr["desc"][self.ka]}</p><div class="actions">{self.watch(tr)}{self.ext(tr["spotify"],"Spotify","btn ghost") if tr.get("spotify") else ""}</div><dl class="credits"><div><dt>{t("Performer","შემსრულებელი")}</dt><dd>{t("Goga Meskhi","გოგა მესხი")}</dd></div>{cred}</dl>{self.ext(tr.get("source_url",source[4]),t("Video source","ვიდეოს წყარო") if tr["slug"]=="ar-makhsovs" else t("Source & credits","წყარო და კრედიტები"))}</div></div></div></section>'+self.connect()
  # Structured data: the recording, plus the YouTube video where the page plays one.
  rec=recording_node(tr,self);nodes=[rec]+([video_node(tr,self)] if is_video(tr) else [])
  image=dict(thumb(tr['id']),alt=self.thumbalt(tr)) if tr.get('id') else None
  crumbs=[(t('Home','მთავარი'),absurl('index',self.lang)),(t('Music','მუსიკა'),absurl('music',self.lang)),(tr[self.lang],self.canonical)]
  other=tr['en' if self.ka else 'ka'];kind=t('song','სიმღერა')
  meta_desc=tr['desc'][self.ka]
  self.frame('music',tr[self.lang],body,meta_desc,full=f'{tr[self.lang]} ({other}) — {t("Goga Meskhi","გოგა მესხი")} | {kind}',og_type='music.song',image=image,nodes=nodes,main=rec['@id'],crumbs=crumbs,og=[('music:musician',absurl('about',self.lang))])
 def videos(self):
  t=self.t;cards='';
  vids=[x for x in tracks if is_video(x)]
  for i,tr in enumerate(vids):
   cards+=f'<article class="video-card"><div class="thumb">{self.img(tr["img"],loading="eager" if i<2 else "lazy")}<a class="thumbbutton" href="https://www.youtube.com/watch?v={tr["id"]}" target="_blank" rel="noopener" data-video="{tr["id"]}" data-title="{e(tr[self.lang])}" aria-label="{e(t("Play ","ვიდეო: ")+tr[self.lang])}"><span aria-hidden="true">▶</span></a></div><h3>{tr[self.lang]}</h3><p class="muted">{self.other(tr["en" if self.ka else "ka"])} · {t("Video","ვიდეო")}</p>{self.link("music/"+tr["slug"],t("Song details","სიმღერის შესახებ"),aria=t("Song details","სიმღერის შესახებ")+": "+tr[self.lang])}</article>'
  body=self.pagehero(t('02 / Visual experiences','02 / ვიდეოები'),t('Goga Meskhi music videos.','გოგა მესხის ვიდეოკლიპები.'),t('Selected music videos and live performance recordings by Goga Meskhi.','გოგა მესხის რჩეული ვიდეოკლიპები და ცოცხალი შესრულების ჩანაწერები.'))+f'<section class="section"><div class="wrap"><h2 class="sr-only">{t("Music videos","ვიდეოკლიპები")}</h2><div class="video-grid">{cards}</div><div class="actions">{self.ext(YT,t("Visit the official YouTube channel","ოფიციალური YouTube არხი"),"btn")}</div></div></section>';self.frame('videos',t('Videos','ვიდეოები'),body+self.platform_strip()+self.connect(),nodes=[item_list(self,[(x[self.lang],absurl('music/'+x['slug'],self.lang)) for x in vids])],main=self.canonical+'#list')
 def about(self):
  t=self.t;milestones=[('2013',t('Participated in The Voice of Georgia, joining Maia Darsmelidze’s team.','„ახალი ხმის“ მონაწილე, მაია დარსმელიძის გუნდის წევრი.')),('2022',t('Radio premiere of Chamotova Isev, alongside live performances and conversation about Melikishvili Avenue.','„ჩამოთოვა ისევ“ — რადიოპრემიერა, ცოცხალი შესრულება და საუბარი „მელიქიშვილის გამზირზე“.')),('2025',t('Chamotova Isev and Melikishvili Avenue videos published on the official YouTube channel; Chamiara premiered.','ოფიციალურ YouTube არხზე გამოქვეყნდა „ჩამოთოვა ისევ“ და „მელიქიშვილის გამზირი“; შედგა „ჩამიარას“ პრემიერა.')),('2026',t('Presented a new video of Chemo Aprilo, dedicated to Mamuka Onashvili.','წარადგინა „დაღამებულხარ, ჩემო აპრილო“ — ვიდეოკლიპი მამუკა ონაშვილის ხსოვნისადმი.'))];timeline=''.join(f'<div><b>{a}</b><p>{b}</p></div>' for a,b in milestones);body=self.pagehero(t('03 / The artist','03 / არტისტი'),t('More than a voice.','მეტი, ვიდრე ხმა.'),t('Meet Goga Meskhi.','გაიცანი გოგა მესხი.'))+f'<section class="section"><div class="wrap split"><div class="portrait">{self.img("portrait")}</div><div><h2>{t("The artist.","არტისტი.")}</h2><p>{t("Goga Meskhi is a Georgian vocalist with a longstanding performing career. His repertoire includes new songs written for him, collaborations and personal interpretations of familiar Georgian music.","გოგა მესხი ქართველი მომღერალია, რომელსაც სცენაზე მუშაობის მრავალწლიანი გამოცდილება აქვს. მის რეპერტუარშია სპეციალურად მისთვის დაწერილი სიმღერები, დუეტები და ნაცნობი ქართული მუსიკის საკუთარი ინტერპრეტაციები.")}</p><p>{t("His recordings and videos carry the stories of the people, places and artists that inspire them. Explore his music and the interviews behind the works.","მის ჩანაწერებსა და ვიდეოებში გაცოცხლებულია ადამიანები, ადგილები და ხელოვანები, რომლებიც მის შთაგონებას ქმნიან. გაეცანი მუსიკასა და სიმღერების ისტორიებს.")}</p>{self.link("music",t("Explore music","მუსიკის მოსმენა"))}</div></div></section><section class="compact" style="background:#e7e4df"><div class="wrap"><h2>{t("Selected milestones","რჩეული ეტაპები")}</h2><div class="timeline">{timeline}</div><div class="actions">{self.link("press",t("Interviews and sources","ინტერვიუები და წყაროები"))}</div></div></section>'+self.connect();self.frame('about',t('About','ბიოგრაფია'),body)
 def live(self):
  t=self.t;body=self.pagehero('04 / '+t('Live','კონცერტები'),t('Goga Meskhi concerts.','გოგა მესხის კონცერტები.'),t('Past concert appearances and how to invite Goga Meskhi for live performances.','გაეცანი ცოცხალ გამოსვლებს და გოგა მესხის მოწვევის შესახებ.'))+f'<section class="cinema bglive"><div class="wrap"><h2>{t("Music, together.","მუსიკა გვაერთიანებს.")}</h2><p>{t("Concerts, cultural events and special collaborations.","კონცერტები, კულტურული ღონისძიებები და შემოქმედებითი თანამშრომლობა.")}</p>{self.link("contact",t("Booking inquiry","მოწვევის შესახებ"),"btn")}</div></section><section class="section"><div class="wrap"><h2>{t("Upcoming dates","მომავალი კონცერტები")}</h2><div class="empty"><h3>{t("Stay connected.","დარჩი ჩვენთან.")}</h3><p>{t("No confirmed dates have been supplied for this website. Follow Goga’s social channels for announcements.","ვებგვერდისთვის ჯერ არ არის მოწოდებული დადასტურებული თარიღები. სიახლეებისთვის გამოიწერე გოგას სოციალური არხები.")}</p>{self.ext(FB,"Facebook","btn")}</div><div class="section-head" style="margin-top:55px"><div><h2>{t("Bring Goga to your city.","მოიწვიე გოგა შენს ქალაქში.")}</h2><p style="margin-top:20px">{t("Are you a concert organizer, cultural association or a fan interested in a performance? Prepare a message and contact Goga directly.","წარმოადგენ საკონცერტო ორგანიზაციას, კულტურულ გაერთიანებას ან გსურს გოგას კონცერტი შენს ქალაქში? მოამზადე შეტყობინება და პირდაპირ დაუკავშირდი.")}</p></div>{self.link("contact",t("Prepare an inquiry","მოამზადე შეტყობინება"),"btn")}</div></div></section>'+self.connect();self.frame('live',t('Live','კონცერტები'),body.replace(self.connect(),self.past_live()+self.connect()))
 def stories(self):
  t=self.t;body=self.pagehero(t('05 / The journal','05 / ისტორიები'),t('Behind the music.','მუსიკის მიღმა.'),t('The people, places and memories behind the songs.','ადამიანები, ადგილები და მოგონებები სიმღერების მიღმა.'))+f'<section class="section"><div class="wrap"><h2 class="sr-only">{t("Song stories","სიმღერების ისტორიები")}</h2><div class="stories">{"".join(self.storycard(x,"eager" if i<2 else "lazy") for i,x in enumerate(stories))}</div></div></section>'+self.connect();self.frame('stories',t('Stories','ისტორიები'),body,nodes=[item_list(self,[(x[2 if self.ka else 1],absurl('stories/'+x[0],self.lang)) for x in stories])],main=self.canonical+'#list')
 def storypage(self,s):
  t=self.t;tr=s[6];p=press[tr['source']];extra={'ar-makhsovs':('Explore the video and discover more of Goga’s repertoire in the music catalogue.','ნახე ვიდეო და აღმოაჩინე გოგას სხვა სიმღერები მუსიკის კატალოგში.'),'melikishvili-avenue':('In an interview with Radio Fortuna, Goga described the track as a special part of his repertoire because of its dedication to Doijashvili. The official video, presented as part of Georgian Stories, brings the listener into the cultural landscape of Tbilisi.','რადიო „ფორტუნას“ ინტერვიუში გოგამ აღნიშნა, რომ ეს სიმღერა მის რეპერტუარში განსაკუთრებულ ადგილს იკავებს, რადგან დოიჯაშვილს ეძღვნება. ოფიციალური ვიდეო მსმენელს თბილისის კულტურულ სივრცეში ამოგზაურებს.'),'chamotova-isev':('In an interview, Goga recalled hearing Mamuka Charkviani’s version and later asking permission to record his own interpretation. His video continues that creative conversation.','ინტერვიუში გოგამ გაიხსენა მამუკა ჩარკვიანის შესრულებით სიმღერის მოსმენა და მოგვიანებით საკუთარი ვერსიის ჩაწერის სურვილი. ვიდეო ამ შემოქმედებითი დიალოგის გაგრძელებაა.'),'chemo-aprilo':('The 2026 premiere was a tribute rather than simply another recording. The song connects the work of Ebralidze and Gogolashvili with the interpretation associated with Mamuka Onashvili.','2026 წლის პრემიერა ხსოვნისადმი მიძღვნა იყო. სიმღერა ებრალიძისა და გოგოლაშვილის შემოქმედებას მამუკა ონაშვილის შესრულების ტრადიციასთან აკავშირებს.')}[s[0]];body=self.pagehero(t('The journal / Behind the song','ისტორიები / სიმღერის შესახებ'),s[2 if self.ka else 1],s[4 if self.ka else 3])+f'<section class="section"><article class="wrap article">{self.img(s[5],priority=True)}<p>{tr["desc"][self.ka]}</p><p>{extra[self.ka]}</p><div class="actions">{self.watch(tr)}{self.link("music/"+tr["slug"],t("Song details","სიმღერის შესახებ"))}</div><p class="mini muted" style="margin-top:30px">{t("Video source:","ვიდეოს წყარო:") if tr.get("slug")=="ar-makhsovs" else t("Editorial summary based on the published interview:","გამოქვეყნებული ინტერვიუს მიხედვით მომზადებული ტექსტი:")} {self.ext(tr["source_url"],"YouTube") if tr.get("slug")=="ar-makhsovs" else self.ext(p[4],p[0])}</p>{self.link("stories",t("All stories","ყველა ისტორია"))}</article></section>'+self.connect()
  # Title pairs the story with its song; the description is the summary plus the first sentence of the story.
  name=t('Goga Meskhi','გოგა მესხი');st=s[2 if self.ka else 1];first=extra[self.ka].split('. ')[0];first=first if first.endswith('.') else first+'.'
  rec=recording_node(tr,self,compact=True);crumbs=[(t('Home','მთავარი'),absurl('index',self.lang)),(t('Stories','ისტორიები'),absurl('stories',self.lang)),(st,self.canonical)]
  self.frame('stories',st,body,s[4 if self.ka else 3]+' '+first,full=(f'{st} — {tr[self.lang]}' if st!=tr[self.lang] else f'{st} — {t("Behind the song","სიმღერის ისტორია")}')+f' | {name}',og_type='article',image=dict(thumb(tr['id']),alt=self.thumbalt(tr)),nodes=[rec],about=[rec['@id']],crumbs=crumbs)
 def presspage(self):
  t=self.t;body=self.pagehero(t('06 / Media','06 / მედია'),t('In the press.','პრესაში.'),t('Selected interviews, appearances and music premieres.','რჩეული ინტერვიუები, გამოსვლები და მუსიკალური პრემიერები.'))+f'<section class="section"><div class="wrap">{self.pressrows()}<div class="section-head" style="margin-top:60px"><div><h2>{t("Press information","მედიისთვის")}</h2><p style="margin-top:20px">{t("For media inquiries and requests for authorized photography or an electronic press kit, contact Goga directly.","მედიის წარმომადგენლებს ინტერვიუს, ავტორიზებული ფოტოების ან ელექტრონული პრესკიტის მოთხოვნა შეუძლიათ პირდაპირ გოგასთან.")}</p></div>{self.link("contact",t("Media inquiries","მედიის მოთხოვნები"),"btn")}</div></div></section>'+self.connect();self.frame('press',t('Press','მედია'),body)
 def contact(self):
  t=self.t;opts=[t('Concert / festival','კონცერტი / ფესტივალი'),t('Bring Goga to my city','მოიწვიე გოგა ჩემს ქალაქში'),t('Media / interview','მედია / ინტერვიუ'),t('Collaboration','თანამშრომლობა'),t('Other','სხვა')];name=t('Name','სახელი');city=t('City / country','ქალაქი / ქვეყანა');msg=t('Message','შეტყობინება');typ=t('Inquiry type','მოთხოვნის ტიპი');body=self.pagehero(t('Connect','კონტაქტი'),t('Let’s connect.','დაგვიკავშირდი.'),t('Concert booking, collaborations and media inquiries for Goga Meskhi.','გოგა მესხის კონცერტის მოწვევა, თანამშრომლობა და მედიის მოთხოვნები.'))+f'''<section class="section"><div class="wrap details"><div><h2>{t('Get in touch.','დაგვიკავშირდი.')}</h2><p>{t('Use Goga’s social page to contact him. For an event inquiry, include the proposed city, date, venue and your organization.','გოგასთან დასაკავშირებლად გამოიყენე მისი სოციალური გვერდი. კონცერტის შემთხვევაში მიუთითე ქალაქი, თარიღი, ადგილი და ორგანიზაცია.')}</p>{self.ext(FB,t('Open Facebook','Facebook-ზე გადასვლა'),'btn')}<p class="notice" style="margin-top:25px">{t('This website does not send or store your inquiry. The form prepares a message for you to copy and send yourself on Facebook.','ვებგვერდი არ აგზავნის და არ ინახავს შეტყობინებას. ფორმა ამზადებს ტექსტს, რომელსაც თავად დააკოპირებ და Facebook-ზე გაგზავნი.')}</p></div><div><form class="form" data-inquiry><label>{typ}<select name="{typ}">{''.join('<option>'+x+'</option>' for x in opts)}</select></label><label>{name}<input name="{name}" required autocomplete="name" maxlength="100"></label><label>{city}<input name="{city}" required maxlength="120"></label><label>{msg}<textarea name="{msg}" required maxlength="1500"></textarea></label><button class="btn" type="submit">{t('Prepare message','შეტყობინების მომზადება')} ↗</button></form><div class="form-output" hidden><label>{t('Your message draft','შეტყობინების ტექსტი')}<textarea class="message-draft" readonly></textarea></label><button class="btn" data-copy>{t('Copy message','ტექსტის კოპირება')}</button>{self.ext(FB,t('Open Facebook to send','გაგზავნე Facebook-ზე'),'btn ghost')}</div></div></div></section>''';self.frame('contact',t('Contact','კონტაქტი'),body)
 def privacy(self):
  t=self.t;body=self.pagehero(t('Information','ინფორმაცია'),t('Privacy.','კონფიდენციალურობა.'),t('How this preview handles information.','როგორ მუშავდება ინფორმაცია ამ სამუშაო ვერსიაში.'))+f'<section class="section"><article class="wrap article"><p>{t("The inquiry form creates a draft locally in your browser. This preview has no newsletter database, analytics tracking or server-side form submission.","მოთხოვნის ფორმა შეტყობინების ტექსტს მხოლოდ ბრაუზერში ქმნის. სამუშაო ვერსიას არ აქვს გამოწერის მონაცემთა ბაზა, ანალიტიკური თვალთვალი ან სერვერზე ფორმის გაგზავნის ფუნქცია.")}</p><p>{t("When you choose to play a video, the site connects to YouTube’s privacy-enhanced embed. External links open third-party services, which have their own privacy policies. Google Fonts may load fonts from Google servers.","ვიდეოს დაკვრისას ვებგვერდი უკავშირდება YouTube-ის კონფიდენციალურობის გაუმჯობესებულ რეჟიმს. გარე ბმულები მესამე მხარის სერვისებზე გადადის, რომლებსაც საკუთარი კონფიდენციალურობის პოლიტიკა აქვთ. შრიფტები შესაძლოა Google Fonts-ის სერვერებიდან ჩაიტვირთოს.")}</p></article></section>';self.frame('privacy',t('Privacy','კონფიდენციალურობა'),body)
 def notfound(self):
  # GitHub Pages serves this for any missing URL. It is bilingual because the visitor's language is unknown.
  body=self.pagehero('404','Page not found.','This page does not exist or has moved.')+'<section class="section"><div class="wrap"><p lang="ka">გვერდი ვერ მოიძებნა ან გადატანილია.</p><div class="actions"><a class="btn" href="/">Go to the homepage <span aria-hidden="true">↗</span></a><a class="btn ghost" href="/ka/" lang="ka" hreflang="ka">მთავარი გვერდი <span aria-hidden="true">↗</span></a><a class="btn ghost" href="/en/music.html">Music <span aria-hidden="true">↗</span></a></div></div></section>'
  self.frame('','Page not found',body,index=False)

 def featured_music(self):
  t=self.t; featured=tracks[3]; rows=''
  for i,tr in enumerate([tracks[7],tracks[0],tracks[2],tracks[1],tracks[6],tracks[8]],1):
   art=self.img(tr['img'],loading='lazy') if tr.get('id') else '<div class="mini-duet">GM<br>× NK</div>'
   kind=t(*{'recording':('Song','სიმღერა'),'original':('Song','სიმღერა'),'interpretation':('Music video','ვიდეოკლიპი'),'duet':('Duet','დუეტი')}[tr['cat']]); kind=t('With Keti Chanturidze','ქეთი ჭანტურიძესთან ერთად') if tr['slug']=='davbrundebi' else kind; href=self.url('music/'+tr['slug'])
   rows+=f'<article class="music-row"><span class="track-num">{i:02}</span><a class="mini-cover" href="{href}">{art}</a><div class="song-info"><h3><a href="{href}">{tr[self.lang]}</a></h3><p>{kind} · {tr["year"].replace("video",t("video","ვიდეო")).replace("audio",t("audio","აუდიო"))}</p></div>{self.watch(tr,"row-play",t("Play","მოსმენა"),named=True)}<a class="row-detail" href="{href}" aria-label="{e(t("Song details","სიმღერის შესახებ")+": "+tr[self.lang])}">↗</a></article>'
  return f'''<section class="featured-section" id="music"><div class="wrap">{self.sectionhead(t("01 / Listen & discover","01 / მოუსმინე და აღმოაჩინე"),t("Selected music.","რჩეული მუსიკა"),self.link("music",t("Full discography","ყველა სიმღერა")))}<div class="music-editorial"><article class="spotlight"><div class="spot-art">{self.img(featured['img'],loading='lazy')}<div class="spot-gradient"></div><span class="spot-badge">{t('2026 / Featured video','2026 / რჩეული კლიპი')}</span></div><div class="spot-copy"><p class="eyebrow">{t('A tribute to Mamuka Onashvili','მამუკა ონაშვილის ხსოვნას')}</p><h3>{featured[self.lang]}</h3><p>{featured['desc'][self.ka]}</p><div class="actions">{self.watch(featured,'btn',t('Watch video','უყურე კლიპს'))}{self.link('music/'+featured['slug'],t('Song story','სიმღერის ისტორია'))}</div></div></article><div class="playlist"><div class="playlist-head"><strong>{t('Explore the catalogue','აღმოაჩინე რეპერტუარი')}</strong><span>06 {t('selections','ჩანაწერი')}</span></div>{rows}</div></div></div></section>'''
 def platform_strip(self):
  t=self.t; return f'<section class="platform-strip"><div class="wrap"><div><span class="eyebrow">{t("Your music. Your platform.","მუსიკა შენს პლატფორმაზე")}</span><h3>{t("Listen & follow","მოუსმინე და გამოიწერე")}</h3></div><div class="platform-pills">{self.ext(YT,"YouTube","pill-link")}{self.ext(SP,"Spotify","pill-link")}{self.ext(AM,"Amazon Music","pill-link")}{self.ext(FB,"Facebook","pill-link")}{self.link("listen",t("All channels","ყველა არხი"),"pill-link accent")}</div></div></section>'
 def album_block(self):
  t=self.t; rows=''.join(f'<div><span>{i:02}</span><strong>{title}</strong><span>{duration}</span></div>' for i,(title,duration) in enumerate(album,1));return f'<section class="section album-section"><div class="wrap details"><div><p class="eyebrow">{t("Digital release / Amazon Music listing","ციფრული გამოცემა / Amazon Music")}</p><h2>Love, as it is.</h2><p>{t("An eight-track collection indexed by Amazon Music under Goga Meskhi. Titles are shown as listed by the platform. The release date, complete credits and availability are still to be confirmed.","Amazon Music-ზე გოგა მესხის სახელით ინდექსირებული რვასიმღერიანი კრებული. სათაურები მოცემულია პლატფორმის მიხედვით. გამოცემის თარიღი, სრული კრედიტები და ხელმისაწვდომობა დასაზუსტებელია.")}</p>{self.ext(AM,t("View on Amazon Music","გადასვლა Amazon Music-ზე"),"btn")}</div><div class="album-list">{rows}</div></div></section>'
 def listenpage(self):
  t=self.t; cards=''.join(f'<a class="channel-card" href="{e(c[4])}" target="_blank" rel="noopener noreferrer"><span class="eyebrow">{c[1]}</span><h3>{c[0]}</h3><p>{c[3 if self.ka else 2]}</p><span class="channel-arrow" aria-hidden="true">↗</span></a>' for c in channels);body=self.pagehero(t('Discover / Connect','აღმოაჩინე / გამოიწერე'),t('Listen to Goga Meskhi music.','გოგა მესხის მუსიკის მოსმენა.'),t('Official channels to stream Goga Meskhi songs: YouTube, Spotify, Facebook and radio archives.','გოგა მესხის სიმღერების ოფიციალური არხები — YouTube, Spotify, Facebook და რადიოარქივი.'))+f'<section class="section"><h2 class="sr-only">{t("Channels and platforms","არხები და პლატფორმები")}</h2><div class="wrap channel-grid">{cards}</div></section>'+f'<section class="compact"><div class="wrap"><h3>{t("Media archive","მედიაარქივი")}</h3><p>{t("Third-party coverage and indexed video copies, separate from artist-operated pages.","მესამე მხარის მედია და ვიდეოარქივები, არტისტის საკუთარი არხებისგან დამოუკიდებლად.")}</p><div class="actions">{self.ext("https://lot.ge/video/eb198e75cc05d/%E1%83%92%E1%83%9D%E1%83%92%E1%83%90-%E1%83%9B%E1%83%94%E1%83%A1%E1%83%AE%E1%83%98-%E1%83%9B%E1%83%94%E1%83%9A%E1%83%98%E1%83%A5%E1%83%98%E1%83%A8%E1%83%95%E1%83%98%E1%83%9A%E1%83%98%E1%83%A1-%E1%83%92%E1%83%90%E1%83%9B%E1%83%96%E1%83%98%E1%83%A0%E1%83%98-georgian-stories-official-video","Lot.ge · Melikishvili Avenue")}{self.ext("https://fortuna.ge/fortuna-tag/goga-meskhi/","Fortuna · Media archive")}{self.link("press",t("All press","ყველა მედია"))}</div></div></section>'+self.album_block()+self.connect();self.frame('listen' ,t('Listen & follow','არხები'),body)
 def past_live(self):
  t=self.t; events=[('2017',t('Tbilisi Symphony Orchestra','თბილისის სიმფონიური ორკესტრი'),t('Concert with Vakhtang Kakhidze and guest vocalists.','კონცერტი ვახტანგ კახიძესა და მოწვეულ ვოკალისტებთან ერთად.'),press[10][4]),('17.08.2019',t('Black Sea Arena','ბლექ სი არენა'),t('Jansugh and Vakhtang Kakhidze’s compositions with the Tbilisi Symphony Orchestra and ensemble Rustavi.','ჯანსუღ და ვახტანგ კახიძეების კომპოზიციები თბილისის სიმფონიურ ორკესტრსა და ანსამბლ „რუსთავთან“ ერთად.'),BSA),('04.04.2026',t('Bella and Her Friends','ბელა და მეგობრები'),t('Listed performer for a charity concert at the Tbilisi State Conservatoire.','თბილისის სახელმწიფო კონსერვატორიის საქველმოქმედო კონცერტის აფიშაზე მითითებული შემსრულებელი.'),BELLA)];rows=''.join(f'<div><b>{dt}</b><p><strong>{title}</strong><br>{d}<br>{self.ext(url,t("Event source","წყარო"))}</p></div>' for dt,title,d,url in events);return f'<section class="compact past-live"><div class="wrap"><h2>{t("Selected appearances","რჩეული გამოსვლები")}</h2><div class="timeline">{rows}</div></div></section>'
 def about(self):
  t=self.t; blocks=[(t('From theatre to music','თეატრიდან მუსიკამდე'),t('Raised in a musical family, Goga initially studied dentistry before switching to theatre. He trained as an actor and later made music his career. In 2003 he joined the vocal group Vivo, which performed live and released an album.','გოგა მუსიკალურ ოჯახში გაიზარდა. თავდაპირველად სტომატოლოგიას სწავლობდა, შემდეგ კი თეატრალურ სასწავლებელში გადავიდა. მსახიობის პროფესიის დაუფლების შემდეგ მუსიკა მის მთავარ საქმიანობად იქცა. 2003 წელს ჯგუფ „ვივოში“ დაიწყო სიმღერა; ჯგუფი ცოცხლად გამოდიოდა და ალბომიც გამოუშვა.'),press[4][4]),(t('Television and the stage','ტელევიზია და სცენა'),t('Star Academy introduced him to a broad television audience. In 2013 he joined Maia Darsmelidze’s team on The Voice of Georgia; later he appeared in GDS’s One to One.','„ვარსკვლავების აკადემიამ“ იგი ფართო სატელევიზიო აუდიტორიას გააცნო. 2013 წელს „ახალ ხმაში“ მაია დარსმელიძის გუნდში მოხვდა, მოგვიანებით კი GDS-ის პროექტში „ერთი ერთში“ მონაწილეობდა.'),AMB),(t('Orchestral collaborations','სიმფონიური პროექტები'),t('His work with Vakhtang Kakhidze includes performances alongside the Tbilisi Symphony Orchestra. In August 2019 he was part of the Black Sea Arena concert celebrating Jansugh and Vakhtang Kakhidze’s music, with ensemble Rustavi and fellow Georgian vocalists.','ვახტანგ კახიძესთან თანამშრომლობა თბილისის სიმფონიურ ორკესტრთან გამოსვლებსაც მოიცავს. 2019 წლის აგვისტოში „ბლექ სი არენაზე“ ჯანსუღ და ვახტანგ კახიძეების შემოქმედებით საღამოში მონაწილეობდა ანსამბლ „რუსთავთან“ და სხვა ქართველ ვოკალისტებთან ერთად.'),ORCH),(t('A contemporary repertoire','თანამედროვე რეპერტუარი'),t('From the 2011 video Nu Damemdurebi to recent recordings, Goga builds a repertoire of original songs and reinterpretations. His collaboration with Keti Chanturidze produced Davbrundebi in 2021; in 2023 he launched another duet project with Nanuka Karukhnishvili.','2011 წლის ვიდეოკლიპიდან „ნუ დამემდურები“ უახლეს ჩანაწერებამდე გოგა რეპერტუარს ავტორეული სიმღერებითა და ინტერპრეტაციებით ავითარებს. 2021 წელს ქეთი ჭანტურიძესთან ერთად ჩაწერა „დავბრუნდები“, 2023 წელს კი ნანუკა ქარუხნიშვილთან დუეტის პროექტი დაიწყო.'),DUET),(t('Music and cinema','მუსიკა და კინო'),t('His recent visual projects revisit Georgian classics while bringing together music, poetry and film. In a February 2026 radio interview, he also described his ambition to make a film.','ბოლო ვიდეოპროექტებში ქართული კლასიკური სიმღერები მუსიკის, პოეზიისა და კინოს საშუალებით ახლებურად ცოცხლდება. 2026 წლის თებერვლის რადიოინტერვიუში მან ფილმის გადაღების სურვილზეც ისაუბრა.'),press[0][4])]; cards=''.join(f'<article><h3>{a}</h3><p>{b}</p>{self.ext(u,t("Source","წყარო"))}</article>' for a,b,u in blocks)
  milestones=[('2003','Vivo / ვივო'),('2011',t('Nu Damemdurebi music video','„ნუ დამემდურები“ — კლიპი')),('2013',t('The Voice of Georgia','„ახალი ხმა“')),('2017',t('Symphony orchestra concert','სიმფონიური ორკესტრის კონცერტი')),('2019','Black Sea Arena'),('2021',t('Davbrundebi duet with Keti Chanturidze','„დავბრუნდები“ — დუეტი ქეთი ჭანტურიძესთან')),('2022',t('Chamotova radio premiere','„ჩამოთოვა ისევ“ — რადიოპრემიერა')),('2023',t('Duet with Nanuka Karukhnishvili','დუეტი ნანუკა ქარუხნიშვილთან')),('2025',t('Chamiara premiere and music videos','„ჩამიარას“ პრემიერა და ვიდეოკლიპები')),('2026',t('Chemo Aprilo tribute video','„დაღამებულხარ, ჩემო აპრილო“ — კლიპი'))]; timeline=''.join(f'<div><b>{a}</b><p>{b}</p></div>' for a,b in milestones)
  body=self.pagehero(t('The artist','არტისტი'),t('More than a voice.','მეტი, ვიდრე ხმა.'),t('Goga Meskhi biography — over two decades of music, stage and creative exploration.','გოგა მესხის ბიოგრაფია — მუსიკალური და სცენური გზა.'))+f'<section class="section"><div class="wrap split"><div class="portrait">{self.img("portrait",priority=True)}</div><div><span class="eyebrow">GOGA MESKHI / გოგა მესხი</span><h2>{t("Singer. Actor. Performer.","მომღერალი. მსახიობი.")}</h2><p>{t("Goga Meskhi singer and Goga Meskhi actor — based in Tbilisi, he brings new life to familiar songs while developing his own repertoire. His journey spans vocal ensembles, television, orchestral stages and contemporary studio recordings.","გოგა მესხი მომღერალი და მსახიობი ნაცნობ სიმღერებს ახალ სიცოცხლეს სძენს და საკუთარ რეპერტუარს ავითარებს. მისი შემოქმედებითი გზა ვოკალური ჯგუფებიდან და ტელევიზიიდან სიმფონიურ სცენებსა და თანამედროვე სტუდიურ ჩანაწერებამდე მიდის.")}</p>{self.link("music",t("Discover the music","აღმოაჩინე მუსიკა"))}</div></div></section><section class="section bio-section"><div class="wrap bio-grid">{cards}</div></section><section class="compact"><div class="wrap"><h2>{t("Career timeline","შემოქმედებითი გზა")}</h2><div class="timeline">{timeline}</div>{self.link("press",t("Sources and interviews","წყაროები და ინტერვიუები"))}</div></section>'+self.connect();self.frame('about',t('About','ბიოგრაფია'),body,og_type='profile',og=[('profile:first_name',t('Goga','გოგა')),('profile:last_name',t('Meskhi','მესხი'))])

if __name__ == '__main__':
 for lang in ('en','ka'):
  for slug,method in [('index','home'),('music','music'),('videos','videos'),('live','live'),('about','about'),('stories','stories'),('press','presspage'),('contact','contact'),('privacy','privacy'),('listen','listenpage')]:getattr(Site(lang,f'{lang}/{slug}.html'),method)()
  for tr in tracks:Site(lang,f'{lang}/music/{tr["slug"]}.html').trackpage(tr)
  for s in stories:Site(lang,f'{lang}/stories/{s[0]}.html').storypage(s)
 # The root page is the canonical English homepage and the x-default for visitors in other languages.
 Site('en','index.html').home()
 Site('en','404.html').notfound()
 write_sitemap()
 write_robots()
