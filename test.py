# Librairies

import pytest
import json
import requests
from bs4 import BeautifulSoup






# Constantes

N = 3 # nombre de commentaires souhaités






# Fonctions

def videosId() :

    with open("input.json", 'r') as input_file :
        input_data = json.load(input_file)

    return input_data["videos_id"]

def testVideosId() :

    assert type(videosId()) == list and type(videosId()[0]) == str



def videoUrl(video_id) :

    url = "https://www.youtube.com/watch?v="

    return url + video_id

def testVideoUrl() :

    assert videoUrl("fmsoym8I-3o") == "https://www.youtube.com/watch?v=fmsoym8I-3o"



def videoData(video_url) :

    video_requete =requests.get(video_url).text

    return BeautifulSoup(video_requete, "html.parser")

def testVideoData() :

    assert type(videoData("https://www.youtube.com/watch?v=fmsoym8I-3o")) == BeautifulSoup



def videoTitre(video_data) :

    titre = video_data.find("meta", attrs = {"name":"title"})

    return titre.get("content")

def testvideoTitre() :

    assert videoTitre(videoData("https://www.youtube.com/watch?v=fmsoym8I-3o")) == "Pierre Niney : L’interview face cachée par HugoDécrypte"



def videoAuteur(video_data) :

    auteur = video_data.find("link", attrs = {"itemprop":"name"})

    return auteur.get("content")

def testVideoAuteur() :

    assert videoAuteur(videoData("https://www.youtube.com/watch?v=fmsoym8I-3o")) == "HugoDécrypte"



def videoPoucesBleus(video_data) :

    scripts = video_data.find_all("script")    
    for script in scripts :
        if "clics" in script.get_text() :
            position_debut = script.string.index("LIKE") + 69
            position_fin = script.string.index("clics") - 1
            pouces_bleus = script.string[position_debut:position_fin].replace("\u202f", "")
            break

    return int(pouces_bleus)

def testVideoPoucesBleus() :

    assert type(videoPoucesBleus(videoData("https://www.youtube.com/watch?v=fmsoym8I-3o"))) == int



def videoDescription(video_data) :

    scripts = video_data.find_all("script")
    for script in scripts :
        if "shortDescription" in script.get_text() :
            position_debut = script.string.index("shortDescription") + 19
            position_fin = script.string.index("isCrawlable") - 3
            description = script.string[position_debut:position_fin]
            break

    return description

def testVideoDescription() :

    assert videoDescription(videoData("https://www.youtube.com/watch?v=fmsoym8I-3o")) == "🍿 L'acteur Pierre Niney est dans L’interview face cachée ! Ces prochains mois, le format revient plus fort avec des artistes, sportifs, etc.\\n🔔 Abonnez-vous pour ne manquer aucune vidéo.\\n\\nInterview réalisée à l’occasion de la sortie du film «\xa0Mascarade\xa0» réalisé par Nicolas Bedos, le 1er novembre 2022 au cinéma. Avec Pierre Niney, Isabelle Adjani, François Cluzet, Marine Vacth.\\n\\nChaleureux remerciements au cinéma mk2 Bibliothèque pour son accueil.\\n\\n—\\n\\n00:00 Intro\\n00:22 1\\n03:32 2\\n10:11 3\\n14:09 4\\n17:28 5\\n20:10 6\\n23:13 7\\n39:22 8\\n\\n—\\n\\nPrésenté par Hugo Travers\\n\\nRéalisateur : Julien Potié\\nJournalistes : Benjamin Aleberteau, Blanche Vathonne\\n\\nChargée de production déléguée : Romane Meissonnier\\nAssistant de production déléguée : Clément Chaulet\\nChargée de production exécutive : Marie Delvallée\\n\\nChef OPV : Lucas Stoll\\nOPV : Pierre Amilhat, Vanon Borget\\nElectricien : Alex Henry\\nChef OPS : Victor Arnaud\\nStagiaire image : Magali Faizeau\\n\\nMaquilleuse : Kim Desnoyers\\nPhotographe plateau : Erwann Tanguy\\n\\nMonteur-étalonneur : Stan Duplan\\nMixeuse : Romane Meissonnier\\n\\nCheffe de projets partenariats : Mathilde Rousseau\\nAssistante cheffe de projets partenariats : Manon Montoriol\\n\\n—\\n\\n© HugoDécrypte / 2022"



def videoLiensTimestamp(video_data) :

    scripts = video_data.find_all("script")
    nombre = 0
    liens = []
    for script in scripts :
        if "continuePlayback" in script.get_text() :
            nombre = script.string.count("continuePlayback")//4
            marqueur = 0
            for i in range(nombre) :
                position = script.string[marqueur:].index("continuePlayback") + marqueur
                position_debut = script.string[:position].rindex("url") + 6
                position_fin = script.string[:position].rindex("webPageType") - 3
                liens.append("https://www.youtube.com" + script.string[position_debut:position_fin].replace("\\u0026", "&"))
                marqueur = position + 1
            break

    return liens

def testVideoLiensTimestamp() :

    assert videoLiensTimestamp(videoData("https://www.youtube.com/watch?v=fmsoym8I-3o")) == ['https://www.youtube.com/watch?v=fmsoym8I-3o&t=0s',
     'https://www.youtube.com/watch?v=fmsoym8I-3o&t=22s',
     'https://www.youtube.com/watch?v=fmsoym8I-3o&t=212s',
     'https://www.youtube.com/watch?v=fmsoym8I-3o&t=611s',
     'https://www.youtube.com/watch?v=fmsoym8I-3o&t=849s',
     'https://www.youtube.com/watch?v=fmsoym8I-3o&t=1048s',
     'https://www.youtube.com/watch?v=fmsoym8I-3o&t=1210s',
     'https://www.youtube.com/watch?v=fmsoym8I-3o&t=1393s',
     'https://www.youtube.com/watch?v=fmsoym8I-3o&t=2362s']



def videoLiensAutres(video_data) :

    scripts = video_data.find_all("script")
    liens_https = []
    liens_http = []
    for script in scripts :
        if "shortDescription" in script.get_text() :
            position = script.string.index("shortDescription")
            marqueur = script.string.index("isCrawlable")
            nombre_https = script.string[position:marqueur].count("https://")
            while len(liens_https) < nombre_https :
                position_debut = script.string[position:].index("https://") + position
                position_fin = script.string[position_debut:].index("\\n") + position_debut
                liens_https.append(script.string[position_debut:position_fin])
                position = position_fin + 1
            position = script.string.index("shortDescription")
            marqueur = script.string.index("isCrawlable")
            nombre_http = script.string[position:marqueur].count("http://")
            while len(liens_http) < nombre_http :
                position_debut = script.string[position:].index("http://") + position
                position_fin = script.string[position_debut:].index("\\n") + position_debut
                liens_http.append(script.string[position_debut:position_fin])
                position = position_fin + 1
            break

    return liens_https + liens_http

def testVideoLiensAutres() :

    assert videoLiensAutres(videoData("https://www.youtube.com/watch?v=JhWZWXvN_yo")) == ['https://www.youtube.com/user/ZeratoRSC2/?sub_confirmation=1',
     'https://www.twitch.tv/zerator',
     'https://www.twitch.tv/videos/1630581181',
     'https://boutiquezerator.com/',
     'https://www.facebook.com/ZeratoR',
     'https://twitter.com/ZeratoR',
     'https://www.instagram.com/zerator',
     'https://discord.gg/zerator',
     'https://www.tiktok.com/@ZeratoR',
     'https://www.mandatory.gg/',
     'https://twitter.com/MandatoryGG',
     'https://www.instagram.com/mandatory.gg/',
     'https://www.tiktok.com/@mandatory.gg',
     'https://discord.gg/3uHncKP',
     'https://www.twitch.tv/mandatory',
     'https://www.facebook.com/MandatoryGG/',
     'http://www.ZeratoR.com/',
     'http://e.lga.to/ZeratoR']



def videoCommentaires(video_data, n = N) :

    return 0






# Tests

testVideosId()
testVideoUrl()
testVideoData()
testvideoTitre()
testVideoAuteur()
testVideoPoucesBleus()
testVideoDescription()
testVideoLiensTimestamp()
testVideoLiensAutres()
#testVideoCommentaires()