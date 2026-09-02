import subprocess
import os

releases = [
    ("Kim Scott", "Y'all Ain't Ready", "https://youtube.com/playlist?list=PLNLN1sVBMYzk"),
    ("Lade Bac", "For All the Ladies", "https://youtube.com/playlist?list=PLUG4bviFn-HQ"),
    ("Latrelle", "Dirty Girl Wrong Girl Bad Girl", "https://www.youtube.com/playlist?list=PLsYn0j75RJPyJcGAcM8hqZDRV0VwtyK9K"),
    ("Me 2 U", "Me 2 U", "https://youtube.com/playlist?list=PLf3_Dt5U2TWM"),
    ("Menageri", "Menageri", "https://youtube.com/playlist?list=PLVKrID5avtJ3xdqTHzehY-Wkh5FIb1jp8"),

    ("Michael Sterling", "The Artist", "https://youtube.com/playlist?list=PLDidmuOQfTnM"),
    ("Michael Sterling", "No Such Animal", "https://youtube.com/playlist?list=PLPE1rq9lHi0s"),
    ("Michael Sterling", "Trust", "https://youtube.com/playlist?list=PLRshkinLh32w"),

    ("Michel'le", "Hung Jury", "https://youtube.com/playlist?list=PLzXn8cAHEDCjmahEJGJWPyHdPFjQeAiZZ"),
    ("Michelle Williams", "Unexpected", "https://music.youtube.com/playlist?list=PL_ZwbIqDlpTWFph4jwFofE76FAtnV8tA5"),
    ("Mike Davis", "Mike Davis", "https://music.youtube.com/playlist?list=PLQqvhh0LeK0g"),
    ("Millie Scott", "I Can Make It Good for You", "https://music.youtube.com/playlist?list=PLdGec_eTWK4A"),
    ("Mind", "Mind", "https://music.youtube.com/playlist?list=PLSup-LdGmG-stTxx5c-sfwkTXuPkLPCy0"),
    ("Nais", "Nais", "https://music.youtube.com/playlist?list=PLKD5h9btUEzrPQ0ttfWp45iAdVSURN6Oi"),
    ("Natasha Ramos", "Natasha Ramos", "https://music.youtube.com/playlist?list=PLCECX4Om4lHs"),
    ("Nicole Wray", "Independence Day", "https://music.youtube.com/playlist?list=PLL11b1KxxHtU"),
    ("Nikita Germaine", "As Sweet as It Comes", "https://music.youtube.com/playlist?list=PLKb-miH2habk"),
    ("Olivia", "Behind Closed Doors", "https://music.youtube.com/playlist?list=PLP-KAfdqiIlk"),

    ("One Chance", "Private", "https://music.youtube.com/playlist?list=PLoeCT-uXIQ9C9iYU78mOZ6BD6FF04aaVZ"),
    ("One Chance", "Ain't No Room for Talkin", "https://music.youtube.com/playlist?list=PLoeCT-uXIQ9AqNIoZQFzJoYNFZmPsmVx2"),

    ("Oran Jones", "Gangstas Takin Over", "https://music.youtube.com/playlist?list=PLsoTC3800Rxp2rGOVDzK-ilsodVS2lEPf"),
    ("Oran Jones", "To Be Immortal", "https://music.youtube.com/playlist?list=PLsoTC3800RxrNMk9JSB-jgZgHxnnPyb9S"),
    ("POV", "POV", "https://music.youtube.com/playlist?list=PLd_k0J6l1HAI"),
    ("Pretty Willie", "Compilation", "https://www.youtube.com/playlist?list=PLyJtZ76MkZR4Hw_s5YCcoEG3v30aJW9kG"),
    ("Projection", "Compilation", "https://music.youtube.com/playlist?list=PLBnDvznPyVxE"),
    ("Rachelle Ferrell", "Japan", "https://music.youtube.com/playlist?list=PLjQjuNu3vVC9-j_yjMa0STVRO9Zqtre54"),

    ("Ray Lavender", "Ray Lavender", "https://music.youtube.com/playlist?list=PLoeCT-uXIQ9Dxt_HC2lXmaBiaVE1FZyoR"),
    ("Ray Lavender", "Compilation", "https://music.youtube.com/playlist?list=PLONVknXRbHyE"),

    ("Reel Tight", "Reel Tight", "https://music.youtube.com/playlist?list=PLi-E-XTGVcg_XLscklyhM2Fdzk_xC-OFx"),

    ("Rome", "To Infinity", "https://music.youtube.com/playlist?list=PLV0py5jFVayU"),
    ("Rome", "To the Highest", "https://music.youtube.com/playlist?list=PLZXCPOxt71HI"),

    ("Ryan Leslie", "Just Right", "https://music.youtube.com/playlist?list=PLi-E-XTGVcg8P_Bk7vEW-3CmYBwQGPLD8"),
    ("Sam Salter", "Little Black Book", "https://youtube.com/playlist?list=PLJGrEHv0hU_Q"),
    ("Samantha Mumba", "Woman", "https://youtube.com/playlist?list=PLC4I1ZA2mfOO3Sje0CD36ofRNvw0wizFj"),
    ("Sean Barney Thomas", "Album", "https://music.youtube.com/playlist?list=PLAibupxnlYaQbGpgznXKWsaTOrkyeZh-7"),
    ("Shawn Harris", "Soulful Moaning Reincarnated", "https://youtube.com/playlist?list=PLKsCWLymgwsbyxvA-lnprQdH_4B1_k8Hv"),

    ("Sammie", "Sammie", "http://music.youtube.com/playlist?list=PLoeCT-uXIQ9B1V-C_U4pQAaFafYhPIhPd"),
    ("Sammie", "It's Just a Mixtape", "https://music.youtube.com/playlist?list=PLn2RClp0Qs4C158Zk5k96COCLUAdRbKZo"),
    ("Sammie", "It's Just a Mixtape 2", "https://music.youtube.com/playlist?list=PLA11DE5668E81E0ED"),
    ("Sammie", "Insomnia", "https://music.youtube.com/playlist?list=PLMyw0dWAIHv6sBhciUUafv0GF60wjhjyD"),

    ("Sat-R-Day", "The Weekend Is for You", "https://music.youtube.com/playlist?list=PLONfbLdfTfL4"),
    ("Sat-R-Day", "That's How We're Livin'", "https://music.youtube.com/playlist?list=PLVqwVsmWsyjw"),
    ("Shades", "Shades", "https://music.youtube.com/playlist?list=PLjQjuNu3vVC9ZwLsOJpGFuCAfHWGMVMs4"),

    ("Shannon", "Let the Music Play", "https://music.youtube.com/playlist?list=PLs9zwqXsceUheNMZYNK5Js4NGBy-ECaNi"),
    ("Shannon", "Love Goes All the Way", "https://music.youtube.com/playlist?list=PLV5Q0tPwJttmtrnYTHX9vfEoA0oPB2jf_"),
    ("Shannon", "The Best Is Yet to Come", "https://music.youtube.com/playlist?list=PLvo10NZ0hILYrFBpxiV29hD_rjWdci5xY"),

    ("Shareefa", "The Misunderstanding Of...", "https://music.youtube.com/playlist?list=PLRrXcAEhS0PVZbcnNzWh94MT2k5iRDBHx"),
    ("Skillz", "Skillz", "https://music.youtube.com/playlist?list=PLKkKI7czQ3Dk"),
    ("Smooth", "Smooth & Legit", "https://music.youtube.com/watch?v=LKJwcTuHsEU"),
    ("Sol", "Unity", "https://music.youtube.com/playlist?list=PL8qnqEWNAGBZ1ZDn44KecdAMi-3okEzaQ"),
    ("Static Major", "Compilation", "https://www.youtube.com/playlist?list=PLCG8xE0xxTkrxo807fH2cYXgfEB5UVABD"),

    ("Sue Ann Carwell", "Blue Velvet", "https://music.youtube.com/playlist?list=PLXlm0PpfwxUc"),
    ("Sue Ann Carwell", "Pain Killer", "https://music.youtube.com/playlist?list=PLLzzaIg_KBuI"),
    ("Sunday", "Sunday", "https://music.youtube.com/playlist?list=PLsoTC3800Rxra_Lf82LA2QG9Esy4Vq2-W"),
    ("Sweet Obsession", "Sweet Obsession", "https://music.youtube.com/playlist?list=PLGY9JTh9QLyI"),
    ("Syleena Johnson", "Love Hangover", "https://music.youtube.com/playlist?list=PLsyPOesMW07COk7FqqSpsAd7RRi5hKpF2"),

    ("SZA", "S", "https://music.youtube.com/playlist?list=PLhxEtBIEYHIRyUlQlYH_Grkh02l9X7-bf"),
    ("SZA", "See.SZA.Run", "https://music.youtube.com/playlist?list=PLLDkE2zxlBAdugLHmhHBv_qiPVicbZVcn"),

    ("Taggiz", "Knowledge of Self", "https://music.youtube.com/playlist?list=PLGUb6ssOCgCI"),
    ("Tamar", "Unofficial", "https://music.youtube.com/playlist?list=PLoJO_JfuSj01tEX9TKzjbrGx50rIhj6rC"),
    ("Tasha Holiday", "Just the Way You Like It", "https://music.youtube.com/playlist?list=PLcpLfvE6TIhk"),
    ("Tayla Parx", "Tayla Made", "https://www.youtube.com/playlist?list=PLJry09fo25UA"),

    ("Teairra Mari", "Get Away", "https://www.youtube.com/watch?v=tiKKTu2w9GQ"),
    ("Teairra Mari", "Compilation", "https://www.youtube.com/playlist?list=PLIvBV9LwIX-kioRwHvMSYSs1zt5uX8Wxb"),

    ("The Fratz", "The Fratz", "https://music.youtube.com/playlist?list=PLU-1aZXWWdMs"),
    ("The Irvin Lee Project", "The Irvin Lee Project", "https://music.youtube.com/playlist?list=PLAVRUZjGxf1k"),
    ("Tiffany Evans", "143", "https://www.youtube.com/watch?v=VuljXFnh1WE"),

    ("Teedra Moses", "Young Hustla Vol. 2", "https://www.youtube.com/playlist?list=PLAJYfXWRiUfPUnwqNn10GNUq0N8t7_D_n"),
    ("Teedra Moses", "Young Hustla Vol. 1", "https://www.youtube.com/playlist?list=PLAJYfXWRiUfNvj_-dXtwVIB8bHsyCB52M"),
    ("Teedra Moses", "Young Hustla Vol. 3", "https://www.youtube.com/playlist?list=PLrQsFfYx-ivsDmjP0CvnKclt7xHNS3MQh"),
    ("Teedra Moses", "Royal Patience", "https://www.youtube.com/playlist?list=PLn2RClp0Qs4DTT89gYkmK9lVLxIuILjaN"),

    ("Tink", "Think Tink", "https://www.youtube.com/playlist?list=PLEFBtZMs4T5M"),
    ("Tyra B", "Compilation", "https://music.youtube.com/playlist?list=PLE06GJB5pN-c"),
    ("U-Mind", "Prove My Heart", "https://music.youtube.com/playlist?list=PLVB_Q8uEKo78"),
    ("UNV", "UNV", "https://music.youtube.com/playlist?list=PLjQjuNu3vVC8ISf8wxcG-iJLra1Toozl3"),
    ("VA", "VA", "https://music.youtube.com/playlist?list=PLAeQJCD0N0-c"),
    ("Voices", "Voices", "https://music.youtube.com/playlist?list=PLsoTC3800RxoqBfTHoVGG9aya7iy-7dtL"),
    ("XL", "XL", "https://music.youtube.com/playlist?list=PLJmgFN-nS7Kk"),
    ("Xplicit", "Xplicit", "https://music.youtube.com/playlist?list=PLP43dtF72Kd8"),
    ("Yasmeen", "Yasmeen", "https://music.youtube.com/playlist?list=PLN3K2d3MEjPOMOX8g4icK_OTrq6tG97KB"),
    ("Y?N-Vee", "Y?N-Vee", "https://music.youtube.com/playlist?list=PLDhDrBgX-LpY"),
    ("Young DeBarge", "Young DeBarge", "https://music.youtube.com/browse/MPREb_JejZlFnWULc"),
    ("Yvette Michele", "Yvette Michele", "https://music.youtube.com/playlist?list=OLAK5uy_kNJ4Q1aYlHAyFFBMuGPfH5xtBo7w97ZlU"),
]


for artist, title, url in releases:
    print(f"\n{'=' * 70}")
    print(f"Downloading: {artist} — {title}")
    print(f"{'=' * 70}")

    # yt-dlp will create these directories through the output template,
    # but making them explicitly makes the structure predictable.
    os.makedirs(f"music/{artist}/{title}", exist_ok=True)

    result = subprocess.run([
        "yt-dlp",
        "-v",
        "--yes-playlist",
        "--extractor-args",
        "youtube:player_client=default,web_embedded",
        "-f",
        "m4a",
        "--download-archive",
        "downloaded.txt",
        "-o",
        f"music/{artist}/{title}/%(playlist_index)02d - %(title)s.%(ext)s",
        url
    ])

    if result.returncode != 0:
        print(f"\nFAILED: {artist} — {title}")
    else:
        print(f"\nDONE: {artist} — {title}")

print("\nAll releases processed.")