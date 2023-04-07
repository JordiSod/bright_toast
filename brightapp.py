import streamlit as st
import numpy as np
import pandas as pd
import requests
import string
import json
# from PIL import Image

# A Streamlit app needs to start with a versionof this command.
st.set_page_config(layout='wide')

#Define dictionaries

# We need to setup some cleaning stuff for a few inputs.
def basic_cleaning(sentence):
    '''
    Preprocess user input to send it to the api that houses the model.
    '''

    sentence = sentence.lower()
    sentence = ''.join(char for char in sentence if not char.isdigit())

    for punctuation in string.punctuation:
        sentence = sentence.replace(punctuation, '')

    sentence = sentence.strip()
    sentence = sentence.replace(" ", "_" )

    return sentence

# Define lists and dictinaries with wine info, in order to make the code clearer

variety_list = ['White Blend', 'Portuguese Red', 'Pinot Gris', 'Riesling',
       'Pinot Noir', 'Tempranillo-Merlot', 'Frappato', 'Gewürztraminer',
       'Cabernet Sauvignon', 'Nerello Mascalese', 'Chardonnay', 'Malbec',
       'Tempranillo Blend', 'Meritage', 'Red Blend', 'Merlot',
       "Nero d'Avola", 'Chenin Blanc', 'Gamay', 'Sauvignon Blanc',
       'Viognier-Chardonnay', 'Primitivo', 'Catarratto', 'Inzolia',
       'Petit Verdot', 'Monica', 'Bordeaux-style White Blend', 'Grillo',
       'Sangiovese', 'Cabernet Franc', 'Champagne Blend',
       'Bordeaux-style Red Blend', 'Aglianico', 'Petite Sirah',
       'Touriga Nacional', 'Carmenère', 'Albariño', 'Petit Manseng',
       'Rosé', 'Zinfandel', 'Vernaccia', 'Rosato', 'Grüner Veltliner',
       'Viognier', 'Vermentino', 'Grenache Blanc', 'Syrah', 'Nebbiolo',
       'Shiraz-Cabernet Sauvignon', 'Pinot Blanc', 'Alsace white blend',
       'Barbera', 'Rhône-style Red Blend', 'Portuguese White', 'Graciano',
       'Tannat-Cabernet', 'Sauvignon', 'Sangiovese Grosso', 'Torrontés',
       'Prugnolo Gentile', 'G-S-M', 'Verdejo', 'Fumé Blanc', 'Furmint',
       'Pinot Bianco', 'Bonarda', 'Shiraz', 'Montepulciano', 'Moscato',
       'Grenache', 'Ugni Blanc-Colombard', 'Syrah-Viognier',
       'Blaufränkisch', 'Friulano', 'Assyrtico', 'Carignan-Grenache',
       'Sagrantino', 'Savagnin', 'Cabernet Sauvignon-Syrah', 'Prosecco',
       'Vignoles', 'Sparkling Blend', 'Muscat', 'Muscadelle',
       'Shiraz-Viognier', 'Garganega', 'Pinot Grigio', 'Tempranillo',
       'Zierfandler', 'Cortese', 'Mencía', 'Zweigelt', 'Melon',
       'Rhône-style White Blend', 'Vidal', 'Cannonau', 'Verdelho',
       'Marsanne', 'Scheurebe', 'Kerner', 'Syrah-Grenache', 'Dolcetto',
       'Vilana', 'Glera', 'Viura', 'Garnacha Tintorera', 'Pinot Nero',
       'Roter Veltliner', 'Pinotage', 'Sémillon', 'Pinot Noir-Gamay',
       'Antão Vaz', 'Cabernet Sauvignon-Carmenère', 'Verdejo-Viura',
       'Verduzzo', 'Verdicchio', 'Silvaner', 'Colombard', 'Carricante',
       'Sylvaner', 'Fiano', 'Früburgunder', 'Sousão', 'Roussanne',
       'Avesso', 'Cinsault', 'Chinuri', 'Tinta Miúda',
       'Muscat Blanc à Petits Grains', 'Portuguese Sparkling',
       'Monastrell', 'Xarel-lo', 'Greco', 'Trebbiano',
       'Corvina, Rondinella, Molinara', 'Port', 'Chenin Blanc-Chardonnay',
       'Insolia', 'Merlot-Malbec', 'Ribolla Gialla',
       'Cabernet Sauvignon-Merlot', 'Duras', 'Weissburgunder', 'Roditis',
       'Traminer', 'Papaskarasi', 'Tannat-Syrah', 'Marsanne-Roussanne',
       'Charbono', 'Merlot-Argaman', 'Prié Blanc', 'Sherry',
       'Provence red blend', 'Tannat', 'Zibibbo', 'Falanghina',
       'Garnacha', 'Negroamaro', 'Mourvèdre', 'Syrah-Cabernet',
       'Müller-Thurgau', 'Pinot Meunier', 'Cabernet Sauvignon-Sangiovese',
       'Austrian Red Blend', 'Teroldego', 'Pansa Blanca',
       'Muskat Ottonel', 'Sauvignon Blanc-Semillon', 'Claret',
       'Semillon-Sauvignon Blanc', 'Bical', 'Moscatel', 'Rosado',
       'Viura-Chardonnay', 'Baga', 'Malvasia Bianca',
       'Gelber Muskateller', 'Malbec-Merlot', 'Monastrell-Syrah',
       'Malbec-Tannat', 'Malbec-Cabernet Franc', 'Turbiana', 'Refosco',
       'Alvarinho', 'Manzoni', 'Aragonês', 'Agiorgitiko', 'Malagousia',
       'Assyrtiko', 'Ruché', 'Welschriesling', 'Tinta de Toro',
       'Cabernet Moravia', 'Rieslaner', 'Traminette', 'Chambourcin',
       'Nero di Troia', 'Lambrusco di Sorbara', 'Cesanese',
       'Feteasca Neagra', 'Lagrein', 'Tinta Fina', 'St. Laurent',
       'Marsanne-Viognier', 'Cabernet Sauvignon-Shiraz',
       'Syrah-Cabernet Sauvignon', 'Gewürztraminer-Riesling',
       'Pugnitello', 'Cerceal', 'Touriga Nacional Blend',
       'Austrian white blend', 'Tocai', 'Tinta Roriz',
       'Chardonnay-Viognier', 'Fernão Pires',
       'Cabernet Franc-Cabernet Sauvignon', 'Grenache-Syrah',
       'Seyval Blanc', 'Muscat Canelli', 'Cabernet Merlot',
       'Tempranillo-Cabernet Sauvignon', 'Arinto', 'Aragonez',
       'Merlot-Cabernet Franc', 'Syrah-Petite Sirah', 'Cabernet Blend',
       'Maturana', 'Pecorino', 'Rotgipfler', 'Kinali Yapincak',
       'Cabernet Franc-Carmenère', 'Magliocco', 'Gamay Noir',
       'Sauvignon Gris', 'Spätburgunder', 'Picpoul', 'Vidal Blanc',
       'Albanello', 'White Port', 'Arneis', 'Malvasia', 'Plavac Mali',
       'Lemberger', 'Saperavi', 'Altesse', 'Blanc du Bois',
       'Provence white blend', 'Nosiola', 'Dornfelder',
       'Roussanne-Viognier', 'Ojaleshi', 'Godello', 'Mondeuse',
       'Perricone', 'Pedro Ximénez', 'Auxerrois', 'Syrah-Merlot',
       'Albana', 'Muskat', 'Lambrusco', 'Cabernet Sauvignon-Malbec',
       'Tinto Fino', 'Malbec-Cabernet Sauvignon', 'Moschofilero',
       'Grechetto', 'Encruzado', 'Carignano', 'Cabernet Franc-Merlot',
       'Torbato', 'Syrah-Petit Verdot', 'Garnacha Blanca', 'Pallagrello',
       'Morava', 'Syrah-Mourvèdre', 'Aleatico', 'Carcajolu', 'Kisi',
       'Shiraz-Grenache', 'Palomino', 'Grenache-Carignan', 'Nascetta',
       'Siria', 'Malbec-Syrah', 'Asprinio', 'Feteascǎ Regalǎ',
       'Lambrusco Grasparossa', 'Marselan', 'Tocai Friulano', 'Schiava',
       'Alfrocheiro', 'Chardonnay-Semillon', 'Corvina', 'Norton',
       'Alicante Bouschet', 'Tokaji', 'Moscadello',
       'Cabernet Sauvignon-Tempranillo', 'Carignan', 'Loureiro-Arinto',
       'Cabernet-Syrah', 'Sauvignon Blanc-Chardonnay', 'Symphony',
       'Edelzwicker', 'Madeira Blend', 'Black Muscat', 'Grenache Noir',
       'Durella', 'Xinomavro', 'Tinto del Pais',
       'Merlot-Cabernet Sauvignon', 'Cercial', 'Johannisberg Riesling',
       'Petite Verdot', 'Passerina', 'Valdiguié',
       'Colombard-Sauvignon Blanc', 'Kangoun', 'Loureiro', 'Posip',
       'Uva di Troia', 'Gros and Petit Manseng', 'Jacquère',
       'Kalecik Karasi', 'Karasakiz', 'Mourvèdre-Syrah', 'Negrette',
       'Zierfandler-Rotgipfler', 'Clairette', 'Raboso', 'País', 'Mauzac',
       'Pinot Auxerrois', 'Chenin Blanc-Sauvignon Blanc', 'Diamond',
       'Marzemino', 'Tinta Barroca', 'Chardonnay-Sauvignon Blanc',
       'Castelão', 'Trebbiano Spoletino', 'Teran', 'Trepat', 'Freisa',
       'Neuburger', 'Sämling', 'Chasselas', 'Hárslevelü', 'Trincadeira',
       'Merlot-Tannat', 'Rkatsiteli', 'Melnik', 'Siegerrebe',
       'Trousseau Gris', 'Grenache Blend', 'Gros Manseng',
       'Portuguese Rosé', 'Brachetto', 'Mantonico', 'Ekigaïna',
       'Muskateller', 'Aligoté', 'Sangiovese Cabernet',
       'Touriga Nacional-Cabernet Sauvignon', 'Muscat Blanc', 'Argaman',
       'Viognier-Roussanne', 'Pallagrello Bianco', 'Bobal',
       'Malvasia Istriana', 'Cabernet Sauvignon-Cabernet Franc',
       'Baco Noir', 'Veltliner', 'Tempranillo-Tannat', 'Morillon',
       'Touriga Franca', 'Picolit', 'Barbera-Nebbiolo', 'Prieto Picudo',
       'Gaglioppo', 'Tokay', 'Sacy', 'Piedirosso', 'Piquepoul Blanc',
       'Mansois', 'Chardonnay-Sauvignon', 'Tempranillo-Garnacha',
       'Carmenère-Cabernet Sauvignon', 'Chenin Blanc-Viognier',
       'Susumaniello', 'Vitovska', 'Orange Muscat', 'Grauburgunder',
       'Carignane', 'Moscatel Roxo', 'Tannat-Merlot', 'Nerello Cappuccio',
       'Counoise', 'Macabeo', 'Mazuelo', 'Sauvignon-Sémillon',
       'Tinta del Pais', 'Vranec', 'Mavrud', "Cesanese d'Affile",
       'Moscato Giallo', 'Debit', 'Verdil', 'Cabernet',
       'Verduzzo Friulano ', 'Treixadura', "Loin de l'Oeil",
       'Coda di Volpe', 'Grenache-Mourvèdre', 'Forcallà', 'Viura-Verdejo',
       'Bombino Bianco', 'Pinot-Chardonnay', 'Syrah-Tempranillo',
       'Cabernet Sauvignon-Barbera', 'Merlot-Cabernet',
       "Muscat d'Alexandrie", 'Jaen', 'Tinta del Toro', 'Timorasso',
       'Pigato', 'Sangiovese-Cabernet Sauvignon', 'Shiraz-Cabernet',
       'Viognier-Gewürztraminer', 'Prunelard',
       'Sauvignon Blanc-Chenin Blanc', 'Gros Plant',
       'Malbec-Petit Verdot', 'Colombard-Ugni Blanc', 'Grignolino',
       'Garnacha-Syrah', 'Rufete', 'Tempranillo-Shiraz', 'Mtsvane',
       'Chardonnay-Pinot Gris', 'Marawi', 'Chardonnay-Pinot Blanc',
       'Mataro', 'Tinta Cao', 'Blauer Portugieser', 'Ugni Blanc',
       'Groppello', 'Semillon-Chardonnay', 'Irsai Oliver', 'Alvarelhão',
       'Poulsard', 'Grenache-Shiraz', 'Baga-Touriga Nacional', 'Carineña',
       'Pignoletto', 'Muscatel', 'Mavrodaphne', 'Ciliegiolo',
       'Viognier-Grenache Blanc', 'Greco Bianco',
       'Cabernet Sauvignon-Merlot-Shiraz', 'Sciaccerellu', 'Zelen',
       'Alicante', 'Emir', 'Rosenmuskateller', 'Tsolikouri', 'Narince',
       'Malbec-Cabernet', 'Touriga', 'Grecanico', 'Carmenère-Syrah',
       'Madeleine Angevine', 'Mavroudi', 'Pinot Blanc-Pinot Noir',
       'Muscat Hamburg', 'Tempranillo Blanco', 'Casavecchia',
       'Pinot Gris-Gewürztraminer', 'White Riesling', 'Tinto Velasco',
       'Hondarrabi Zuri', 'Nuragus', 'Xynisteri', 'Kadarka',
       'Sauvignon Musqué', 'Roussanne-Marsanne', 'Incrocio Manzoni',
       'Terrantez', 'Bual', 'Okuzgozu', 'Rivaner', 'Doña Blanca',
       'Graševina', 'Lambrusco Salamino', 'Sangiovese-Syrah',
       'Tannat-Cabernet Franc', 'Thrapsathiri', 'Fer Servadou', 'Mission',
       'Kekfrankos', 'Cococciola', 'Blauburgunder', 'Marquette',
       'Romorantin', 'Verdejo-Sauvignon Blanc', 'Braucol',
       'Malvasia-Viura', 'Savatiano', 'Cabernet Franc-Malbec',
       'Pallagrello Nero', 'Rebula', 'Vespolina', 'Shiraz-Malbec', 'Rebo',
       'Macabeo-Chardonnay', 'Tempranillo-Malbec', 'Tamjanika',
       'Trousseau', 'Bacchus', 'Syrah-Malbec', 'Syrah-Cabernet Franc',
       'Macabeo-Moscatel', 'Cariñena-Garnacha', 'Plyto',
       'Códega do Larinho', 'Sideritis', 'Çalkarası', 'Azal',
       'Moscatel Graúdo', 'Viosinho', 'Moschofilero-Chardonnay',
       'Paralleda', 'Rara Neagra', 'Malvasia di Candia', 'Maria Gomes',
       'Molinara', 'Malvar', 'Airen', 'Erbaluce', 'Muscat of Alexandria',
       'Verdosilla', 'Abouriou', 'Pinot Noir-Syrah', 'Nielluciu',
       'Malbec-Bonarda', 'Vespaiolo', 'Malbec-Carménère', 'Biancolella',
       'Sauvignon Blanc-Verdejo', 'Aidani', 'Garnacha-Monastrell',
       'Vinhão', 'Souzao', 'Roter Traminer', 'Moscatel de Alejandría',
       'Rolle', 'Tinta Francisca', 'Malvasia Nera', 'Orangetraube',
       'Riesling-Chardonnay', 'Žilavka', 'Portuguiser', 'Listán Negro',
       'Pinotage-Merlot', 'Muscadine', 'Maria Gomes-Bical', 'Grolleau',
       'Zlahtina', 'Syrah-Grenache-Viognier', 'Jacquez', 'Gouveio',
       'Canaiolo', 'Carignan-Syrah', 'Bombino Nero',
       'Chardonnay-Riesling', 'Malagouzia-Chardonnay', 'Mavrotragano',
       'Bovale', 'Frankovka', 'Shiraz-Roussanne', 'Cabernet-Shiraz',
       'Syrah-Carignan', 'Elbling', 'Gragnano', 'Garnacha Blend',
       'Pinot Blanc-Chardonnay', 'Schwartzriesling', 'Petit Meslier',
       'Bastardo', 'Vidadillo', 'Misket', 'Chardonnay Weissburgunder',
       'Other', 'Robola', 'Merlot-Shiraz', 'Malagouzia', 'Folle Blanche',
       'Malbec Blend', 'Merlot-Syrah', 'Tamianka', 'Cabernet Pfeffer',
       'Morio Muskat', 'Rabigato', 'Babić', 'Roviello', 'Yapincak',
       'Sauvignonasse', 'Viognier-Marsanne', 'Mandilaria', 'Meseguera',
       'Alvarinho-Chardonnay', 'Saperavi-Merlot', 'Pinot Blanc-Viognier',
       'Teroldego Rotaliano', 'Biancu Gentile', 'Garnacha-Tempranillo',
       'Xinisteri', 'Sauvignon Blanc-Sauvignon Gris',
       'Trebbiano di Lugana', 'Albarossa', 'Ryzlink Rýnský', 'Verdeca',
       'Cabernet Sauvignon Grenache', 'Tămâioasă Românească',
       'Black Monukka', 'Merlot-Grenache', 'Vranac', 'Tempranillo-Syrah',
       'Chardonel', 'Silvaner-Traminer', 'Uvalino',
       'Merseguera-Sauvignon Blanc', 'Cabernet-Malbec', 'Boğazkere',
       'Gelber Traminer', 'Vermentino Nero', 'Cayuga', 'Tinta Amarela',
       'Tinta Negra Mole', 'Moscato Rosa', 'Chelois',
       'Sauvignon Blanc-Assyrtiko', 'Muscadel', 'Shiraz-Tempranillo',
       'Roussanne-Grenache Blanc', 'Biancale', 'Ansonica',
       'Syrah-Bonarda', 'Durif', 'Franconia', 'Malbec-Tempranillo',
       'Nasco', 'Monastrell-Petit Verdot', 'Sirica', 'Vital', 'Espadeiro',
       'Apple', 'Pinot Grigio-Sauvignon Blanc', 'Blatina', 'Karalahna',
       'Feteasca', 'Sercial', 'Valvin Muscat', 'Malvasia Fina',
       'Roditis-Moschofilero', 'St. Vincent', 'Chancellor', 'Premsal',
       'Jampal', 'Tokay Pinot Gris', 'Colorino', 'Picapoll', 'Blauburger',
       'Tinta Madeira', 'Centesimino', 'Grenache Gris', 'Trajadura',
       'Merlot-Petite Verdot', 'Ramisco', 'Catalanesca',
       'Garnacha-Cabernet', 'Garnacha-Cariñena', 'Gamza',
       'Cabernet Franc-Lemberger', 'Chardonnay-Albariño',
       'Shiraz-Mourvèdre', 'Mavrokalavryta', 'Favorita', 'Babosa Negro',
       'Tintilia ', 'Dafni', 'Petit Courbu', 'Kotsifali', 'Parraleta',
       'Moscato di Noto', 'Roscetto', 'Torontel', 'Otskhanuri Sapere',
       'Viognier-Valdiguié', 'Trollinger', 'Tsapournakos', 'Francisa',
       'Kuntra', 'Pignolo', 'Caprettone', 'Ondenc', 'Athiri',
       'Bobal-Cabernet Sauvignon']

country_list = ['Italy', 'Portugal', 'US', 'Spain', 'France', 'Germany',
    'Argentina', 'Chile', 'Australia', 'Austria', 'South Africa',
    'New Zealand', 'Israel', 'Hungary', 'Greece', 'Romania', 'Mexico',
    'Canada', 'Turkey', 'Czech Republic', 'Slovenia', 'Croatia',
    'Georgia', 'Uruguay', 'England', 'Lebanon', 'Serbia', 'Brazil',
    'Moldova', 'Morocco', 'Peru', 'India', 'Bulgaria', 'Cyprus',
    'Armenia', 'Switzerland', 'Bosnia and Herzegovina', 'Slovakia',
    'Macedonia', 'Ukraine', 'Luxembourg', 'China', 'Egypt']

province_list = ['Sicily & Sardinia', 'Douro', 'Oregon', 'Michigan',
       'Northern Spain', 'Alsace', 'Rheinhessen', 'California', 'Mosel',
       'Other', 'Mendoza Province', 'Virginia', 'Beaujolais',
       'Colchagua Valley', 'Southern Italy', 'Maule Valley', 'Bordeaux',
       'Maipo Valley', 'Washington', 'Central Italy', 'Champagne',
       'Burgundy', 'South Australia', 'Tejo', 'Rapel Valley', 'Galicia',
       'France Other', 'Tuscany', 'Burgenland', 'New York',
       'Leyda Valley', 'Piedmont', 'Stellenbosch',
       'Simonsberg-Stellenbosch', 'Walker Bay', 'Alentejano',
       'Central Spain', 'Southwest France', 'Aconcagua Valley',
       'Loncomilla Valley', 'Marlborough', 'Northeastern Italy',
       'Casablanca Valley', 'Veneto', 'Western Cape', 'Judean Hills',
       'Alentejo', 'Coastal Region', 'Rhône Valley', 'Galilee',
       'Beira Atlantico', 'Tokaj', 'Leithaberg', 'Santorini', 'Kremstal',
       'Catalonia', 'Recas', "Hawke's Bay", 'Curicó Valley',
       'Limarí Valley', 'Colchagua Costa', 'Languedoc-Roussillon',
       'Provence', 'Victoria', 'Rheingau', 'Tokaji', 'Naoussa',
       'Valle de Guadalupe', 'Central Valley', 'Lontué Valley',
       'Italy Other', 'Weinviertel', 'Thermenregion', 'Niederösterreich',
       'Wagram', 'Loire Valley', 'Lombardy', 'Ontario',
       'Österreichischer Sekt', 'Kamptal', 'Steiermark', 'Südsteiermark',
       'Crete', 'Vinho Verde', 'Idaho', 'Western Australia', 'Levante',
       'Martinborough', 'Central Otago', 'Lisboa', 'Texas',
       'Península de Setúbal', 'Australia Other', 'Tasmania', 'Franken',
       'Ahr', 'Nahe', 'Dealu Mare', 'Port', 'Darling', 'Chile',
       'Südoststeiermark', 'Corinth', 'Halkidiki', 'Thrace', 'Pfalz',
       'Robertson', 'Dan', 'Northwestern Italy', 'Andalucia',
       'Awatere Valley', 'Wiener Gemischter Satz', 'Wachau',
       'Pennsylvania', 'Swartland', 'Dão', 'Wagram-Donauland',
       'Rio Claro', 'Villány', 'Cachapoal Valley', 'Jidvei', 'America',
       'Traisental', 'Bairrada', 'Negev Hills', 'Ribatejano', 'Duriense',
       'New Jersey', 'Beiras', 'Spanish Islands', 'Upper Galilee',
       'Vinho Espumante', 'Epanomi', 'Nemea', 'Peloponnese',
       'Aconcagua Costa', 'Moravia', 'Slovenia', 'Terras do Dão',
       'Beira Interior', 'Panciu', 'Bío Bío Valley', 'Romania',
       'Portuguese Table Wine', 'Minho', 'Missouri', 'New Mexico',
       'Nevada', 'Bucelas', 'Peumo', 'San Antonio', 'Carnuntum',
       'Estremadura', 'Canterbury', 'Spain Other', 'Drama', 'Ella Valley',
       'Moselle Luxembourgeoise', 'Württemberg', 'Baden', 'Pangeon',
       'Elqui Valley', 'Wairau Valley', 'Istria', 'Peljesac', 'Kakheti',
       'Canelones', 'England', 'Marchigue', 'Paarl', 'Durbanville',
       'Weinland Österreich', 'Mantinia', 'Chalkidiki', 'Lebanon',
       'Setubal', 'Mosel-Saar-Ruwer', 'Colorado', 'Pocerina',
       'British Columbia', 'Puente Alto', 'Kumeu', 'Trás-os-Montes',
       'Shomron', 'Rapsani', 'Vienna', 'New South Wales', 'Nelson',
       'Waipara Valley', 'Constantia', 'Arizona', 'Pinto Bandeira',
       'Primorska', 'Moldova', 'Uruguay', 'Zenata', 'South Africa',
       'Massachusetts', 'Ohio', 'Ica', 'San Vicente', 'Nashik',
       'Franschhoek', 'South Island', 'Atlantida', 'Thracian Valley',
       'Tarnave', 'Vipavska Dolina', 'Bekaa Valley', 'Elgin',
       'Itata Valley', 'Table wine', 'Samson', 'Madeira', 'Cyprus',
       'Pageon', 'Vinho Espumante de Qualidade', 'Wellington',
       'Danube River Plains', 'Gisborne', 'Obidos', 'Wairarapa',
       'Armenia', 'Santa Cruz', 'Korčula', 'Viile Timisului', 'Illinois',
       'Aegean', 'Simonsberg-Paarl', 'Juanico', 'Black Sea Coastal',
       'Santa Catarina', 'Overberg', 'Atalanti Valley', 'Sebes',
       'Moscatel de Setúbal', 'Macedonia', 'Ribatejo', 'Germany',
       'Palmela', 'Galil', 'Kras', 'Croatia', 'Waipara', 'Olifants River',
       'Montevideo', 'Campanha', 'Israel', 'Neusiedlersee', 'Hungary',
       'Lolol Valley', 'Cauquenes Valley', 'Groenekloof', 'Alenquer',
       'Goriska Brda', 'Murfatlar', 'Moscatel do Douro',
       'Washington-Oregon', 'New Zealand', 'Serra Gaúcha', 'San Jose',
       'Vale dos Vinhedos', 'Mittelburgenland', 'Lutzville Valley',
       'North Carolina', 'Apalta', 'Malleco', 'Guerrouane', 'Valais',
       'Choapa Valley', 'Georgia', 'Ankara', 'Samos', 'Mittelrhein',
       'Eisenberg', 'Sagrada Familia', 'Austria', 'Mostar', 'Iowa',
       'Tulbagh', 'Cederberg', 'Hemel en Aarde', 'Ceres Plateau',
       'Bot River', 'Patras', 'Korinthia', 'Greece', 'San Clemente',
       'Podunavlje', 'Florina', 'Buin', 'Haut-Judeé', 'Ukraine',
       'Terras do Sado', 'Maipo Valley-Colchagua Valley', 'Brazil',
       'Breedekloof', 'Leyda Valley-Maipo Valley', 'Vermont',
       'Switzerland', 'Waitaki Valley', 'Eger', 'Golan Heights',
       'Fruška Gora', 'Philadelphia', 'Muzla', 'Mátra', 'Pirque', 'Negev',
       'Pitsilia Mountains', 'East Coast', 'Mavrodaphne of Patras',
       'Attica', 'Progreso', 'Elazığ-Diyarbakir', 'Jonkershoek Valley',
       'Tikves', 'Vale Trentino', 'Turkey', 'Waiheke Island', 'Molina',
       'Serra do Sudeste', 'Dalmatian Coast', 'Eilandia',
       'Dealurile Munteniei', 'Thraki', 'Curicó and Maipo Valleys',
       'Štajerska', 'Middle and South Dalmatia', 'Kentucky', 'Župa',
       'Pafos', 'Monemvasia', 'Szekszárd', 'Elazığ', 'Cappadocia',
       'Kutjevo', 'Ismarikos', 'Connecticut', 'Sithonia',
       'Curicó and Leyda Valleys', 'Agioritikos',
       'Casablanca-Curicó Valley', 'Piekenierskloof', 'Elim', 'Malgas',
       'Beotia', 'Algarve', 'Retsina', 'Amindeo', 'Coelemu',
       'Cape South Coast', 'Sopron', 'Bulgaria', 'North Dalmatia',
       'Northern Cape', 'Vinho da Mesa', 'Hvar', 'Cephalonia', 'Lemesos',
       'Cahul', 'Cyclades', 'Breede River Valley', 'Ticino',
       'Vlootenburg', 'Brda', 'Dingač', 'Morocco', 'Achaia',
       'Polkadraai Hills', 'Rhode Island', 'Amyndeon', 'Vânju Mare',
       'Hrvatsko Primorje', 'Central Greece', 'Dolenjska',
       'Österreichischer Perlwein', 'Requinoa',
       'Mavrodaphne de Cephalonie', 'Goumenissa', 'Portugal', 'Messinia',
       'Lakonia', 'Markopoulo', 'Vinho Licoroso', 'Paardeberg',
       'San Antonio de las Minas Valley', 'Krania Olympus', 'Corinthia',
       'Slovenska Istra', 'Commandaria', 'Gladstone', 'Jerusalem Hills',
       'Mount Athos', 'Colares', 'Helderberg',
       'Casablanca & Leyda Valleys', 'Dealurile Hușilor', 'Urla-Thrace',
       'Südburgenland', 'Cape Peninsula', 'Codru Region', 'Sterea Ellada',
       'Muscat of Patras', 'Imathia', 'Alenteo', 'Canada Other',
       'Letrinon', 'Muscat of Kefallonian', 'Thessalikos', 'Hawaii',
       'China', 'Limnos', 'Egypt', 'Viile Timis', 'Devon Valley', 'Krk',
       'Arcadia', 'Cape Agulhas', 'Kathikas', 'Vin de Pays de Velvendo',
       'Landwein Rhein', 'Lesbos', 'Távora-Varosa', 'Neuchâtel']

provinces_dictionary = {'Portugal':['Douro', 'Alentejano', 'Alentejo', 'Beira Atlantico',
       'Vinho Verde', 'Tejo', 'Lisboa', 'Península de Setúbal', 'Port',
       'Dão', 'Bairrada', 'Ribatejano', 'Duriense', 'Beiras',
       'Vinho Espumante', 'Terras do Dão', 'Beira Interior', 'Minho',
       'Bucelas', 'Estremadura', 'Portuguese Table Wine', 'Setubal',
       'Trás-os-Montes', 'Table wine', 'Moscatel de Setúbal', 'Ribatejo',
       'Palmela', 'Alenquer', 'Obidos', 'Vinho Espumante de Qualidade',
       'Madeira', 'Algarve', 'Terras do Sado', 'Vinho da Mesa',
       'Portugal', 'Moscatel do Douro', 'Vinho Licoroso', 'Colares',
       'Alenteo', 'Távora-Varosa'], 'US':['Oregon', 'Michigan', 'California', 'Virginia', 'Washington',
       'New York', 'Idaho', 'Texas', 'Pennsylvania', 'America',
       'New Jersey', 'Missouri', 'New Mexico', 'Nevada', 'Colorado',
       'Arizona', 'Massachusetts', 'Ohio', 'Illinois',
       'Washington-Oregon', 'North Carolina', 'Iowa', 'Vermont',
       'Kentucky', 'Connecticut', 'Rhode Island', 'Hawaii'], 'Spain':['Northern Spain', 'Galicia', 'Central Spain', 'Catalonia',
       'Levante', 'Andalucia', 'Spanish Islands', 'Spain Other'], 'Italy':['Sicily & Sardinia', 'Southern Italy', 'Central Italy', 'Tuscany',
       'Piedmont', 'Northeastern Italy', 'Veneto', 'Italy Other',
       'Lombardy', 'Northwestern Italy'], 'France':['Alsace', 'Beaujolais', 'Bordeaux', 'Champagne', 'France Other',
       'Southwest France', 'Burgundy', 'Rhône Valley',
       'Languedoc-Roussillon', 'Provence', 'Loire Valley'], 'Germany':['Rheinhessen', 'Mosel', 'Rheingau', 'Franken', 'Ahr', 'Nahe',
       'Pfalz', 'Württemberg', 'Baden', 'Mosel-Saar-Ruwer', 'Germany',
       'Mittelrhein', 'Landwein Rhein'], 'Argentina':['Other', 'Mendoza Province'], 'Chile':['Colchagua Valley', 'Maule Valley', 'Maipo Valley', 'Rapel Valley',
       'Leyda Valley', 'Aconcagua Valley', 'Loncomilla Valley',
       'Casablanca Valley', 'Curicó Valley', 'Limarí Valley',
       'Colchagua Costa', 'Central Valley', 'Lontué Valley', 'Chile',
       'Rio Claro', 'Cachapoal Valley', 'Aconcagua Costa',
       'Bío Bío Valley', 'Peumo', 'Elqui Valley', 'Marchigue',
       'Puente Alto', 'San Antonio', 'Itata Valley', 'Santa Cruz',
       'Lolol Valley', 'Cauquenes Valley', 'Apalta', 'Malleco',
       'Choapa Valley', 'Sagrada Familia', 'San Clemente', 'Buin',
       'Maipo Valley-Colchagua Valley', 'Leyda Valley-Maipo Valley',
       'Pirque', 'Molina', 'Curicó and Maipo Valleys',
       'Curicó and Leyda Valleys', 'Casablanca-Curicó Valley', 'Coelemu',
       'Requinoa', 'Casablanca & Leyda Valleys'], 'Australia':['South Australia', 'Victoria', 'Western Australia',
       'Australia Other', 'Tasmania', 'New South Wales'], 'Austria':['Burgenland', 'Leithaberg', 'Kremstal', 'Weinviertel',
       'Niederösterreich', 'Wagram', 'Kamptal', 'Steiermark',
       'Südsteiermark', 'Südoststeiermark', 'Wiener Gemischter Satz',
       'Wachau', 'Traisental', 'Thermenregion', 'Carnuntum',
       'Weinland Österreich', 'Wagram-Donauland', 'Vienna',
       'Neusiedlersee', 'Mittelburgenland', 'Eisenberg', 'Austria',
       'Südburgenland'], 'South Africa':['Stellenbosch', 'Simonsberg-Stellenbosch', 'Western Cape',
       'Coastal Region', 'Darling', 'Robertson', 'Swartland',
       'Walker Bay', 'Paarl', 'Constantia', 'South Africa', 'Franschhoek',
       'Elgin', 'Wellington', 'Simonsberg-Paarl', 'Overberg',
       'Olifants River', 'Groenekloof', 'Lutzville Valley', 'Durbanville',
       'Breedekloof', 'Cederberg', 'Philadelphia', 'Jonkershoek Valley',
       'Eilandia', 'Tulbagh', 'Hemel en Aarde', 'Cape South Coast',
       'Northern Cape', 'Breede River Valley', 'Elim', 'Vlootenburg',
       'Polkadraai Hills', 'Bot River', 'Paardeberg', 'Helderberg',
       'Cape Peninsula', 'Malgas', 'Devon Valley', 'Cape Agulhas'], 'New Zealand':['Marlborough', "Hawke's Bay", 'Martinborough', 'Central Otago',
       'Awatere Valley', 'Canterbury', 'Wairau Valley', 'Kumeu', 'Nelson',
       'Waipara Valley', 'South Island', 'Gisborne', 'Wairarapa',
       'Waipara', 'New Zealand', 'Waitaki Valley', 'East Coast',
       'Waiheke Island', 'Gladstone'], 'Israel':['Judean Hills', 'Galilee', 'Dan', 'Negev Hills', 'Upper Galilee',
       'Ella Valley', 'Shomron', 'Samson', 'Galil', 'Israel',
       'Haut-Judeé', 'Golan Heights', 'Negev', 'Jerusalem Hills'], 'Hungary':['Tokaj', 'Tokaji', 'Villány', 'Hungary', 'Eger', 'Mátra',
       'Szekszárd', 'Sopron'], 'Greece':['Santorini', 'Crete', 'Corinth', 'Halkidiki', 'Epanomi', 'Nemea',
       'Peloponnese', 'Drama', 'Pangeon', 'Mantinia', 'Chalkidiki',
       'Rapsani', 'Pageon', 'Naoussa', 'Atalanti Valley', 'Macedonia',
       'Samos', 'Patras', 'Korinthia', 'Greece', 'Florina',
       'Mavrodaphne of Patras', 'Attica', 'Thraki', 'Monemvasia',
       'Ismarikos', 'Sithonia', 'Agioritikos', 'Beotia', 'Retsina',
       'Amindeo', 'Cephalonia', 'Cyclades', 'Achaia', 'Amyndeon',
       'Central Greece', 'Mavrodaphne de Cephalonie', 'Goumenissa',
       'Messinia', 'Lakonia', 'Markopoulo', 'Krania Olympus', 'Corinthia',
       'Mount Athos', 'Sterea Ellada', 'Muscat of Patras', 'Imathia',
       'Letrinon', 'Muscat of Kefallonian', 'Thessalikos', 'Limnos',
       'Arcadia', 'Vin de Pays de Velvendo', 'Lesbos'], 'Romania':['Recas', 'Dealu Mare', 'Jidvei', 'Panciu', 'Romania', 'Tarnave',
       'Viile Timisului', 'Sebes', 'Murfatlar', 'Dealurile Munteniei',
       'Vânju Mare', 'Dealurile Hușilor', 'Viile Timis'], 'Mexico':['Valle de Guadalupe', 'San Vicente',
       'San Antonio de las Minas Valley'], 'Canada':['Ontario', 'British Columbia', 'Canada Other'], 'Turkey':['Thrace', 'Aegean', 'Ankara', 'Elazığ-Diyarbakir', 'Turkey',
       'Elazığ', 'Cappadocia', 'Urla-Thrace'], 'Czech Republic':['Moravia'],'Slovenia':['Slovenia', 'Primorska', 'Vipavska Dolina', 'Kras', 'Goriska Brda',
       'Brda', 'Dolenjska', 'Slovenska Istra'], 'Luxembourg': ['Moselle Luxembourgeoise'], 'Croatia':['Istria', 'Peljesac', 'Korčula', 'Croatia', 'Podunavlje',
       'Dalmatian Coast', 'Middle and South Dalmatia', 'Kutjevo',
       'North Dalmatia', 'Hvar', 'Dingač', 'Hrvatsko Primorje', 'Krk'], 'Georgia':['Kakheti', 'Georgia'], 'Uruguay': ['Canelones', 'Uruguay', 'Atlantida', 'Juanico', 'Montevideo',
       'San Jose', 'Progreso'], 'England':['England'], 'Lebanon':['Lebanon', 'Bekaa Valley'], 'Serbia':['Pocerina', 'Fruška Gora'], 'Brazil':['Pinto Bandeira', 'Santa Catarina', 'Serra Gaúcha',
       'Vale dos Vinhedos', 'Brazil', 'Vale Trentino', 'Serra do Sudeste',
       'Campanha'], 'Moldova':['Moldova', 'Cahul', 'Codru Region'], 'Morocco':['Zenata', 'Guerrouane', 'Morocco'], 'Peru': ['Ica'], 'India':['Nashik'], 'Bulgaria':['Thracian Valley', 'Danube River Plains', 'Black Sea Coastal',
       'Bulgaria'], 'Cyprus':['Cyprus', 'Pitsilia Mountains', 'Pafos', 'Lemesos', 'Commandaria',
       'Kathikas'], 'Armenia':['Armenia'], 'Switzerland':['Valais', 'Switzerland', 'Ticino', 'Neuchâtel'], 'Bosnia and Herzegovina':['Mostar'], 'Ukraine':['Ukraine'], 'Slovakia':['Muzla'], 'Macedonia':['Tikves'], 'China':['China']}


# And now on with the show.

st.title(":sparkler: Welcome to Bright Toast! :sparkler:")

st.markdown(" Bright Toast is your personal computerized sommelier. Describe your ideal wine and Bright Toast will provide you with stunning suggestions.")
#st.image('./header.png')


element = st.empty()
element = st.empty()
#image = Image.open("C:\Users\mariana\OneDrive\Pictures\Saved Pictures\neon3.jpg")
st.sidebar.markdown(":star2: Please, tell us what you want to drink! ")

descriptors = st.sidebar.text_input('Describe your ideal wine making sure to detail the look, smell, and taste.', key = 33)
#st.sidebar.markdown(":star2: Example of a correct wine description: Aromas include tropical fruit, broom, brimstone and dried herb. The palate isn't overly expressive, offering unripened apple, citrus and dried sage alongside brisk acidity.")
st.sidebar.markdown(":star2: Example: I want a superb wine with soft and velvety tannins and a unique character of dark fruits, black olives, dark chocolate, earth and berries. I want a Petrus. I can't afford a Petrus. Tell me what to do.")

st.sidebar.markdown(":star2: These are optional parameters, don't worry if you don't know :) ")
variety =   st.sidebar.multiselect('Select a variety', variety_list)
countries = st.sidebar.multiselect('select a country',list(provinces_dictionary.keys()))
#countries = st.sidebar.multiselect('select a country', country_list)
#provinces = st.sidebar.multiselect('Select a province', province_list)

if len(countries) > 0:
    provinces_total = []
    for c in range(len(countries)):
        provinces_total = provinces_total + list(provinces_dictionary[countries[c]])
    provinces = st.sidebar.multiselect('Select a province', provinces_total)
else:
    provinces = st.sidebar.multiselect('Select a province', province_list)


min_price = st.sidebar.number_input('Minimum price',min_value=1, max_value= 3000,value=1)
max_price = st.sidebar.number_input('Maximum price (sky is the limit)', max_value=3500, value=3500)


#st.text(mingo)
price_range = st.sidebar.slider(
'Or select a range of prices',
0, 3500, (min_price, max_price))
# st.write('Values:', values)
# st.write('Values:', values[0])
min_price = price_range[0]
max_price = price_range[1]

if provinces == []:
    provinces = 'all'
else:
    provinces = '_'.join(provinces)

if countries == []:
    countries = 'all'
else:
    countries = '_'.join(countries)

if variety == []:
    variety = 'all'
else:
    variety = '_'.join(variety)



#    url='https://bright-toast-api-cqu7vos7fq-vp.a.run.app/predict'
url='https://bright-toast-api2-cqu7vos7fq-vp.a.run.app/predict'
#    url='http://127.0.0.1:8000/predict'


params ={'descriptors': basic_cleaning(descriptors),
        'countries': countries,
        'provinces': provinces,
        'regions': 'all',
        'variety': variety,
        'wineries': 'all',
        'min_price': int(min_price),
        'max_price': int(max_price) }


if descriptors:
    try:
        req = requests.get(url, params=params)
#        st.text(st.text(req.request.url))
        winerec = req.json()
#        st.table(winerec['suggestions'])
        contenido = winerec
        title = []
        variety = []
        winery = []
        country = []
        province = []
        region = []
        points = []
        price = []
        wine_descriptors = []
        wine = len(contenido['suggestions'])
        for w in range(wine):
            ws = str(w+1)
            title.append(contenido['suggestions'][ws]['title'])
            variety.append(contenido['suggestions'][ws]['variety'])
            winery.append(contenido['suggestions'][ws]['winery'])
            country.append(contenido['suggestions'][ws]['country'])
            province.append(contenido['suggestions'][ws]['province'])
            region.append(contenido['suggestions'][ws]['region_1'])
            points.append(contenido['suggestions'][ws]['points'])
            price.append(contenido['suggestions'][ws]['price'])
            wine_descriptors.append(contenido['suggestions'][ws]['wine_descriptors'])

        # Convertimos la lista en una cadena de caracteres
        clear_wd=[]
        for wd in wine_descriptors:
            clear_wd.append(' '.join(wd))
        datos = {'Title': title,
                'variety': variety,
                'winery': winery,
                'country':country,
                'province':province,
                'region':region,
                'points':points,
                'price':price,
                'wine_descriptors':clear_wd}
        sirve = pd.DataFrame(datos)
        sirve.drop_duplicates(inplace=True)
        # sirve.reset_index(inplace=True)
        #sirve.drop(['index'], axis=1,inplace=True)
        sirve = sirve.set_index('Title')

        for w in range(len(sirve)):
            fila = sirve.iloc[w]
            if w == 0:
                st.markdown(':wine_glass: Try this wonderful wine first!')
        #        st.text(fila.to_frame().T)
        #        st.text(fila[0])
                st.table(fila.T)
            else:
                st.markdown(':wine_glass: Or this!')
        #        st.text(fila.to_frame().T)
        #        st.text(fila[0])
                st.table(fila.T)

        st.markdown(':star2: Still thirsty? Tell us what else you want to try!')


    except:
        st.text('')
