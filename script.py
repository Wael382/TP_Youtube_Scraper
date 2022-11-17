# Librairies

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



def videoUrl(video_id) :

    url = "https://www.youtube.com/watch?v="

    return url + video_id



def videoData(video_url) :

    video_requete =requests.get(video_url).text

    return BeautifulSoup(video_requete, "html.parser")



def videoTitre(video_data) :

    titre = video_data.find("meta", attrs = {"name":"title"})

    return titre.get("content")



def videoAuteur(video_data) :

    auteur = video_data.find("link", attrs = {"itemprop":"name"})

    return auteur.get("content")



def videoPoucesBleus(video_data) :

    scripts = video_data.find_all("script")    
    for script in scripts :
        if "clics" in script.get_text() :
            position_debut = script.string.index("LIKE") + 69
            position_fin = script.string.index("clics") - 1
            pouces_bleus = script.string[position_debut:position_fin].replace("\u202f", "")
            break

    return int(pouces_bleus)



def videoDescription(video_data) :

    scripts = video_data.find_all("script")
    for script in scripts :
        if "shortDescription" in script.get_text() :
            position_debut = script.string.index("shortDescription") + 19
            position_fin = script.string.index("isCrawlable") - 3
            description = script.string[position_debut:position_fin]
            break

    return description



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



def videoCommentaires(video_data, n = N) :

    return 0






# Script

ids = videosId()
urls = list(map(videoUrl, ids))
videos = list(map(videoData, urls))
titres = list(map(videoTitre, videos))
auteurs = list(map(videoAuteur, videos))
likes = list(map(videoPoucesBleus, videos))
descriptions = list(map(videoDescription, videos))
liens_timestamp = list(map(videoLiensTimestamp, videos))
liens_autres = list(map(videoLiensAutres, videos))
commentaires = list(map(videoCommentaires, videos))

class VideoYoutube :

    def __init__(self, i) :
        self.titre = titres[i]
        self.auteur = auteurs[i]
        self.likes = likes[i]
        self.description = descriptions[i]
        self.liens_timestamp = liens_timestamp[i]
        self.liens_autres = liens_autres[i]
        self.id = ids[i]
        self.commentaires = commentaires[i]

    def dictionnaire(self) :
        return {"titre":self.titre,
                "auteur":self.auteur,
                "likes":self.likes,
                "description":self.description,
                "liens":(self.liens_timestamp + self.liens_autres),
                "id":self.id,
                "commentaires":self.commentaires}

videos_youtube = dict()
for i in range(len(ids)) :
    video_youtube = VideoYoutube(i)
    videos_youtube["video_{}".format(i)] = video_youtube.dictionnaire()

with open("output.json", 'w') as output_file :
    json.dump(videos_youtube, output_file)