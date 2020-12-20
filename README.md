# Audiobook for Grandma

## Ideas

### Interface

Simple, clean interface. 

Something like this : [easy MP3](https://www.amazon.fr/Solo-Lecteur-MP3-Audio-Personnel/dp/B07W6NKZL7/ref=sr_1_6?__mk_fr_FR=%C3%85M%C3%85%C5%BD%C3%95%C3%91&dchild=1&keywords=lecteur+audio+malvoyant&qid=1608483543&sr=8-6)

Or use the raspberry pi : 
  * [button raspberry pi](https://www.amazon.fr/EG-classique-bricolage-Joystick-Raspberry/dp/B06WWRKGGD/ref=asc_df_B06WWRKGGD/?tag=googshopfr-21&linkCode=df0&hvadid=228517671828&hvpos=&hvnetw=g&hvrand=9975758559269508943&hvpone=&hvptwo=&hvqmt=&hvdev=c&hvdvcmdl=&hvlocint=&hvlocphy=9055137&hvtargid=pla-425411946892&psc=1)

### Where to find the AUDIOBOOKS

https://www.capretraite.fr/blog/style-de-vie/guide-livre-audio-continuer-a-profiter-de-lecture-grand-age/

Use AUDIBLE API : seems like a bad idea since AUDIBLE doesn't like it
  * https://www.reddit.com/r/audible/comments/ara6vw/audible_api/
  * https://www.reddit.com/r/audible/comments/8uhgsv/audible_public_api/

Use Kobo API : 
  * https://community.kobotoolbox.org/t/kobo-api-examples-using-new-kpi-endpoints/2742

Free books :
  * [Projet Gutenberg](http://www.gutenberg.org/browse/languages/fr) + wget
    * no AUDIO : https://azure.microsoft.com/fr-fr/services/cognitive-services/text-to-speech/#features is a nice TTS (cost ?)
      * on raspberry : [wine + windows TTS](https://www.reddit.com/r/linux/comments/6z41qb/my_text_to_speech_tts_solution_wine_microsoft/)
  * [Internet Archive](https://archive.org/details/AuFilDesLectures)
  * [Audiocité](https://www.audiocite.net/?)
  * [Biblioboom](http://www.bibliboom.com/)
  
Possible storage : https://86.243.32.119

### How to choose AUDIOBOOKS

Machine learning algorithm that propose interresting books. 

Or use an existing algorithm like KOBO algorithm. 
