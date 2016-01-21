#Yatzy pelin säännöt ja alustus:
#Yatzyn perus periaate on pelata nopilla pokeria, tässä voi pelata joko yksin
#tai kavereita vastaan. Heittokertoja on 3 per vuoro, josta kaikkia ei tarvitse
#käyttää. Sen lisäksi voi aina lukita joitakin heitettyjä noppia, helpottaakseen
#yhdistelmien saantia. Yatzya pelataan niin kauan, että kaikki yhdistelmät ovat
#saaneet pisteensä. Jos pelaaja ei pysty saamaan kaikkia yhdistelmiä, joutuu hän
#sijoittamaan pistemäärän 0 osaan pistesarakkeista. Pisteet lasketaan yhteen ja
#kaikkien sarakkeiden täytyttyä voittaja on se, jolla on eniten pisteitä.
#Ykkösistä kutosiin pisteet lasketaan kyseisen silmälukujen noppien määrästä
#kerrottuna kyseisellä silmäluvulla. #1 parista täyskäteen yhdistelmät ovat kuin
#pokerissa ja niistä saa pisteitä saman verran kuin kyseiseen yhdistelmään
#osallistuvien noppien silmälukujen yhteismäärä on. Pieni suora on yhdistelmä
#missä on kaikki nopat 1-5 ja siitä saa 15 pistettä, mikä on myös silmälukujen
#yhteismäärä. Vastaavasti isosuora on 2-6 ja siitä saa 20 pistettä. Sattumaan
#kelpaa kaikki noppien mahdolliset yhdistelmät ja siitä saa noppien silmälukujen
#yhteispistemäärän verran pisteitä. Yatzy taas on viidellä nopalla pelatessa
#kaikki viisi noppaa samaa, siitä saa pisteitä 50 ja silmäluvuista tulevan
#yhteispistemäärän. Jos ensimmäisetä kuudesta eli aina vaan samaa silmälukua
#olevista saa yhteensä 63 pistetettä tai enemmän on oikeutettu 50 bonukseen
#Tässä on myös mahdollista pelata pakkojatsia, mikä tarkoittaa
#sitä, että kaikki sarakkeet on täytettävä järjestyksessä ylhäältä alas. Toinen
#mahdollinen lisäasetus on pelata jatsia, missä heittoja saa ottaa jemmaan ja
#käyttää myöhemmin. Jemmaheitoilla pelatessa, jäljelle jääneet heitot lisätään
#lopputulokseen

#Osassa koodissa on käytetty rakenteita, mitkä toimii niin, että esim noppien
#määrän voi muuttaa helposti. Tämä on sen takia, että olen tehnyt tästä
#myös kuuden nopan version ja erilaisia muunnelmia erisäännöillä.

#selitän hieman tarkemmin alun graafisenkäyttöliittymän rakennetta, mutta en
#viitsi käyttää aikaa kaikkien rivien kommentointiin, sillä tässä on 500+ riviä


#Tuodaan tarvittavat elementit
from tkinter import *
from tkinter.messagebox import *
import random
import time

#noppa lista tehdään
nopat = [ "1.gif", "2.gif", "3.gif", "4.gif", "5.gif", "6.gif" ]

class Yatzy:
    def __init__(self):
        #muodostetaan kysely ikkuna, missä valitaan säännöt pelille.
        self.__ikkuna = Tk()
        self.__ikkuna.title("Yatzy")
        #Luodaan spinbox mistä saadaan pelaajien määrä, se on asetettu aluksi
        #neljäksi ja spinboxista löytyy valinnat väliltä 1-8, mutta siihen voi
        #myös syöttää tekstiä tai numeroita. (kaikki positiiviset numerot
        #hyväkystään, mutta tekstiä ei)
        self.__var = StringVar()
        self.__var.set("2")
        self.__määrä = Spinbox(from_=0, to=8, textvariable=self.__var)
        self.__määrä.grid(row=1)
        #luodaan myös labeli, missä on selite mitä kysytään.
        self.__label = Label(self.__ikkuna,text="Pelaajien määrä:")
        self.__label.grid(row=0)
        #kyselyille halutaanko pelata pakkojatsia tai kerätäänkö heittoja
        #tehdään checkboxit, ne saa arvoja 0 tai 1 ja ne saadaan käyttöön
        #allaolevien muuttujien avulla
        self.__var1 = IntVar()
        self.__var2 = IntVar()
        self.__vastus = IntVar()
        self.__pakkoko = Checkbutton(self.__ikkuna,text="Pelataanko pakkojatsia"
                                     , variable=self.__var1)
        self.__pakkoko.grid(row=2)
        self.__jemmataanko = Checkbutton(self.__ikkuna,text="Kerätäänkö heittoja"
                                     , variable=self.__var2)
        self.__jemmataanko.grid(row=3)
        self.__konettavastaa = Checkbutton(self.__ikkuna,text="Tietokone mukaan?"
                                     , variable=self.__vastus)
        self.__konettavastaa.grid(row=4)
        #näiden tietojen syötettyä päästään eteenpäin nappia painamalla eteenpäin
        self.__nappi= Button(self.__ikkuna, text="Eteenpäin"
                             ,command=self.kysynimet)
        self.__nappi.grid(row=5,columnspan=2, sticky=E+W)
        self.__ikkuna.mainloop()
    def kysynimet(self):
        try:
            try:
                #kokeillaan saadaanko numero, jossei valitetaan
                self.__pelaajat = int(self.__määrä.get())
            except  ValueError:
                raise ValueError("Syötä numero")
            #vastaavasti katotaan onko numero myöskin positiivinen.
            if self.__pelaajat > 0 or (self.__pelaajat == 0 and self.__vastus.get() == 1):
                #jos on tuhotaan aikaisemmat graafisenkäyttöliittymänkomponentit
                #jotta voidaan luoda uudet tilalle
                self.__määrä.destroy()
                self.__label.destroy()
                self.__pakkoko.destroy()
                self.__jemmataanko.destroy()
                self.__konettavastaa.destroy()
                #tehdään pelaaja määrän verran labeleita ja entryjä, jotta kaikki
                #saa syöttää itellensä hyvän aliaksen. Nämä tallennetaan listaan
                #ja näin saadaan tästä tehtyä skaalautuva
                self.__pelaajatiedot = []
                self.__label = []
                if self.__pelaajat > 1:
                    for i in range (self.__pelaajat):
                        label = Label(self.__ikkuna,text="Pelaaja"+str(i+1)+":")
                        label.grid(row=i)
                        uusi = Entry()
                        uusi.grid(row=i, column=1)
                        self.__pelaajatiedot.append(uusi)
                        self.__label.append(label)
                #paitsi jos pelaajamäärä oli 1, riittää yhdet labelit ja entryt
                #tämä tehdään siksi, että saadaan järkevä teksti nimen kyselyyn
                if self.__pelaajat == 1:
                    label = Label(self.__ikkuna,text="Pelinimesi:")
                    label.grid(row=1)
                    uusi = Entry()
                    uusi.grid(row=1, column=1)
                    self.__pelaajatiedot.append(uusi)
                    self.__label.append(label)
                #luodaan myös nappi, mistä päästään pelaamaan
                self.__nappi.configure(text="Pelaamaan", command=self.teepeli)
                self.__nappi.grid(row=self.__pelaajat+1, columnspan=8, sticky=E+W)
            #jos pelaaja määrä on alle yksi, valitetaan taas, näihin valituksiin
            #on tehty eritilanteissa järkevän kuuloiset tekstit
            elif self.__pelaajat < 1:
                    raise ValueError("Syötäpä positiivinen")
        except ValueError as viesti:
            showerror("Virhe", viesti)
    def teepeli(self):
        #peliluodaan, ensiksi haetaan pelaajamäärän verran äskeisiin listassa
        #oleviin entryihin sijoitettuja pelaajanimiä. Jos joihinkin ei olla
        #sijoitettu mitää, ne muutetaan vain Pelaaja1 tyylisiksi nimiksi.
        self.__pelailijat = []
        for i in range(self.__pelaajat):
            lisättävä = self.__pelaajatiedot[i].get()
            if lisättävä == "":
                lisättävä = "Pelaaja" + str(i+1)
            #muutetaan myös eka kirjain isoksi
            self.__pelailijat.append(lisättävä[0].upper()+lisättävä[1:])
        #tuhotaan taas edelliset elementit
            self.__label[i].destroy()
            self.__pelaajatiedot[i].destroy()
        self.__nappi.destroy()
        if self.__vastus.get() == 1:
            self.__pelailijat.append("Tietokone")
            self.__pelaajat += 1

        #sitten luodaan noppakuvalista
        self.__noppakuvat = []
        for kuvat in nopat:
            kuva = PhotoImage(file=kuvat)
            self.__noppakuvat.append(kuva)
        #otetaan arvot pakkojatsille ja jemmaheitoille ja niiden mukaan
        #kytketään päälle mahdollisesti lisäominaisuudet
        if self.__var1.get() == 1:
            self.__pakkojatsi = True
        else:
            self.__pakkojatsi = False
        if self.__var2.get() == 1:
            self.__heitotjemmaan = True
        else:
            self.__heitotjemmaan = False

        #tehdään kaikille ylös sarakket, josta nähdään kenen vuoro on
        #tuo sijoitus (column=6+1) on vähän typerä, mutten viitsinyt muuttaa
        self.__kukapelaa = []
        for i in range (self.__pelaajat):
            kuka  = Label(self.__ikkuna)
            kuka.grid(row=0, column=6+i)
            self.__kukapelaa.append(kuka)

        #jos heittojen jemmaus on päällä luodaan sille tarvitut vehkeet
        if self.__heitotjemmaan is True:
            self.__lisänappi = Button(self.__ikkuna, text="lisäheitto",
                                      state=DISABLED, command=self.heitä)
            self.__lisänappi.grid(row=19, column=30, columnspan=3, sticky=E+W)
            lisäheitto = Label(self.__ikkuna, text="Lisäheittoja")
            lisäheitto.grid(row=20, column=0)
            self.__lisäheittoja = []
            for i in range (self.__pelaajat):
                uusi = Label(self.__ikkuna)
                uusi.grid(row=20, column=6+i)
                self.__lisäheittoja.append(uusi)


        self.__lista = []
        self.__lista.append("Ykkösiä")      #tässä luodaan lista mikä sisältää
        self.__lista.append("Kakkosia")     #kaikki tekstit mitkä sijoitetaan
        self.__lista.append("Kolmosia")     #pisteriveihin. Näillä samoilla
        self.__lista.append("Nelosia")      #indekseillä löytyy jatkossa kaikki
        self.__lista.append("Vitosia")      #toimenpiteet, missä sijoitellaan,
        self.__lista.append("Kutosia")      #lasketaan tai otetaan ylös tuloksia
        self.__lista.append("Summa(63)")
        self.__lista.append("Bonus")
        self.__lista.append("1 pari")
        self.__lista.append("2 paria")
        self.__lista.append("Kolmoset")
        self.__lista.append("Neloset")
        self.__lista.append("Täyskäsi")
        self.__lista.append("Pieni suora")
        self.__lista.append("Iso suora")
        self.__lista.append("Sattuma")
        self.__lista.append("Yatzy")
        self.__lista.append("Total")
        for i in range (len(self.__lista)):
            Label(self.__ikkuna, text=self.__lista[i])\
                .grid(row=i+2, column=0, rowspan=1, sticky=N)

        #tehdään napit listan mukaan kaikille pisteen ottoa varten
        self.__napit = []
        for i in range (6):
            self.__nappi=Button(self.__ikkuna, text=" ",state=DISABLED,
                                command=lambda nro = i : self.samoja(nro))
            self.__nappi.grid(row=i+2, column=3, columnspan=1, sticky=E+W,)
            self.__napit.append(self.__nappi)
        #jätetään 2 välistä (summa ja bonus) jolloin myös indeksistä tulee 2
        #pienempi lisätäänpä siis 2 tyhjää väliin ja näin vältytään turhilta
        #sekoituksilta jatkossa!
        for i in range (2):
            self.__napit.append("")
        for i in range (8,17):
            self.__nappi=Button(self.__ikkuna, text=" ",state=DISABLED,
                                command=lambda nro = i : self.tapaus(nro))
            self.__nappi.grid(row=i+2, column=3, columnspan=1, sticky=E+W,)
            self.__napit.append(self.__nappi)

        #jokaiselle pistemäärälle paikat jotka löytyvät indekseillä, samat kuin
        #nappien indeksit + summalle, bonukselle ja tulokselle omat ja nämä siis
        #luodaan yhtämonta kertaa kuin pelissä on pelaajia.
        self.__pistelaabelit = []
        for i in range(self.__pelaajat):
            pistelabel = []
            for e in range(18):
                uusi = Label(self.__ikkuna,)
                uusi.grid(row=e+2, column=6+i)
                pistelabel.append(uusi)
            self.__pistelaabelit.append(pistelabel)

        #sitten noppienmäärän verran noppia ja niille lukitukset
        self.__noppienmäärä = 5
        self.__noppalista = []
        self.__lukitukset = []
        for i in range(self.__noppienmäärä):
            self.__noppa = Label(self.__ikkuna)
            self.__noppa.grid(row=3+3*i, column=30, rowspan=3, columnspan=3)
            self.__noppalista.append(self.__noppa)
            lukitus = Button(self.__ikkuna)
            lukitus.grid(row=5+3*i, column=35, columnspan=3, sticky=E+W)
            self.__lukitukset.append(lukitus)
            #ja lukituksille tottakai myös komennot
            self.__lukitukset[i].configure\
                        (command=lambda nro = i : self.lukinta(nro))
        #vielä nappula heittämiselle ja kaikki taitaa olla valmista
        self.__heitä = Button(self.__ikkuna, text="heitä",command=self.heitä)
        self.__heitä.grid(row=18, column=30, columnspan=3, sticky=E+W)

        #kutsutaan pelin alustusta, erottelu tosin on turha, mutta selkeyttävä
        self.alusta_peli()
    def alusta_peli(self):
        for i in range(self.__noppienmäärä):
            self.__noppalista[i].configure(image=self.__noppakuvat[0])

        self.__nopat = [0]*self.__noppienmäärä

        for i in range(6):
            self.__napit[i].configure(text=" ",state=DISABLED)
        for i in range(8,15):
            self.__napit[i].configure(text=" ",state=DISABLED)
        self.__napit[16].configure(text="xD",state=DISABLED)

        self.__lukinta = []
        for i in range (self.__noppienmäärä):
            lukko = False
            self.__lukinta.append(lukko)
            self.__lukitukset[i].configure(text="valitse",
                         background="lime green", state=DISABLED)

        self.__kukapelaa[0].configure(text=self.__pelailijat[0],state=NORMAL)
        for i in range (1,self.__pelaajat):
            self.__kukapelaa[i].configure\
                (text=self.__pelailijat[i][0],state=DISABLED)

        self.__summa = []
        self.__total = []
        self.__jemmaheitot = []
        self.__bonus = []
        self.__mitkä = []
        self.__summailtavat = []
        self.__summattujo = []
        for i in range(self.__pelaajat):
            mitkä = 0
            summa = 0
            total = 0
            jemmaheitot = 0
            bonus = 0
            summailtavat = []
            self.__mitkä.append(mitkä)
            self.__bonus.append(bonus)
            self.__summa.append(summa)
            self.__total.append(total)
            self.__jemmaheitot.append(jemmaheitot)
            self.__summailtavat.append(summailtavat)
            self.__summattujo.append(False)
        self.__pelaaja = 0
        self.__heitot = 0
        self.__kierrokset = 0
        if self.__heitotjemmaan is True:
            for i in range (self.__pelaajat):
                self.__lisäheittoja[i].configure\
                        (text=self.__jemmaheitot[self.__pelaaja])

        #luodaan kaikille käsille totuusarvot, jotka kertovat, onko niihin jo
        #laitettu pisteitä edellisillä kierroksilla, luodaan myös summalle ja
        #bonukselle omat, niitä ei käytetä mutta koodia on helpompi seurata
        self.__käytetty = []
        for i in range(self.__pelaajat):
            käytetty = []
            for i in range(17):
                käytetty.append(False)
            self.__käytetty.append(käytetty)
    def lukinta(self, i):
        if self.__lukinta[i] == False:
            self.__lukinta[i] = True
            self.__lukitukset[i].configure(background="lawn green",text="valittu")
        else:
            self.__lukinta[i] = False
            self.__lukitukset[i].configure(background="lime green", text="valitse")
    def heitä(self):
        for i in range(self.__noppienmäärä):
            if self.__lukinta[i] is not True:
                for e in range(0, 10):
                    self.__silmäluku = random.randint(1, 6)
                    self.__noppalista[i]["image"] = \
                        self.__noppakuvat[self.__silmäluku - 1]
                    time.sleep(0.03)
                    self.__ikkuna.update_idletasks()
                    self.__nopat[i] = self.__silmäluku
        if self.__heitotjemmaan is True:
            if self.__heitot < 3:
                self.__heitot += 1
            else:
                self.__jemmaheitot[self.__pelaaja] -= 1
                self.__lisäheittoja[self.__pelaaja].configure\
                    (text=self.__jemmaheitot[self.__pelaaja])
            if self.__jemmaheitot[self.__pelaaja] == 0:
                self.__lisänappi.configure(state=DISABLED)
        else:
            self.__heitot += 1
        self.pisteitä_vai_ei()
    def pisteitä_vai_ei(self):

        #annetaan aluksi kaikille totuusarvot false myös summalle ja bonukselle,
        #ihan vaan, että koodista ei tulisi yhtään pidempi
        self.__ehto = []
        for i in range(17):
            self.__ehto.append(False)

        #jos tietty luku löytyy nopista se saa totuusarvon true
        for i in range(6):
            if (i+1) in self.__nopat:
                self.__ehto[i] = True

        #parit, kolmoset, täkärit yms löydetään vertaamalla kaikkia noppia
        #toisiinsa, esimerkiksi täkäri voi tulla vain jos 10:stä vertailusta
        #neljässä on ollut samat nopat. Pari taas tulee jos yksikin noppa on
        #sama kuin joku muu, mutta jatsi vaatii kaikki eli 10 "samaa"
        samat = 0
        for e in range (self.__noppienmäärä-1):
            for i in range (1,self.__noppienmäärä-e):
                if self.__nopat[e] == self.__nopat[e+i]:
                    samat += 1
        if samat > 0:
            self.__ehto[8] = True
        if samat == 2 or samat == 4:
            self.__ehto[9] = True
        if samat > 2:
            self.__ehto[10] = True
        if samat == 4:
            self.__ehto[12] = True
        if samat > 5:
            self.__ehto[11] = True
        if samat == 10:
            self.__ehto[16] = True

        #suorat seulotaan niin, että ensin katsotaan löytyykö kaikki 2-5 nopista
        #jos löytyy ja myös 1 löytyy pienisuora saa totuusarvon true ja jos 6
        #löytyy vastaavasti silloin isosuora saa totuusarvon true
        peräkkäisiä = 0
        for i in range(2,6):
            if i in self.__nopat:
                peräkkäisiä += 1
        if peräkkäisiä == 4:
            if  1 in self.__nopat:
                self.__ehto[13] = True
            if 6 in self.__nopat:
                self.__ehto[14] = True
        self.pisteytys()
    def pisteytys(self):

        self.__pisteitä = []
        for i in range(6):
            if self.__ehto[i] is True:
                self.yhtä(i+1)
            else:
                self.__pisteet = 0
            self.__pisteitä.append(self.__pisteet)

        #lisätään kaksi tyhjää alkiota taas, ettei indeksit mene sekaisin
        for i in range(2):
            self.__pisteitä.append("")

        if self.__ehto[8] is True:
            self.montasamaa(2)
            self.__pisteitä.append(self.__pisteet)
        else:
            self.__pisteitä.append(0)

        if self.__ehto[9] is True:
            self.kaksparia()
            self.__pisteitä.append(self.__pisteet)
        else:
            self.__pisteitä.append(0)

        if self.__ehto[10] is True:
            self.montasamaa(3)
            self.__pisteitä.append(self.__pisteet)
        else:
            self.__pisteitä.append(0)

        if self.__ehto[11] is True:
            self.montasamaa(4)
            self.__pisteitä.append(self.__pisteet)
        else:
            self.__pisteitä.append(0)

        if self.__ehto[12] is True:
            self.muille_pisteet()
            self.__pisteitä.append(self.__pisteet)
        else:
            self.__pisteitä.append(0)

        if self.__ehto[13] is True:
           self.__pisteitä.append(15)
        else:
            self.__pisteitä.append(0)

        if self.__ehto[14] is True:
            self.__pisteitä.append(20)
        else:
            self.__pisteitä.append(0)

        self.muille_pisteet()
        self.__pisteitä.append(self.__pisteet)

        if self.__ehto[16] is True:
            self.__pisteitä.append(50+self.__pisteet)
        else:
            self.__pisteitä.append(0)
        self.sijoita()
    def yhtä(self, mitä):
    #pisteiden talteen otto niissä tilanteissa, että halutaan vaan yhtä samaa
    #silmälukua olevien noppien pisteet pistetaululle
    #lukitaan haluttu noppa
        self.__määrähaluttua = 0
        for i in range(self.__noppienmäärä):
            if self.__nopat[i] == mitä:
                self.__määrähaluttua += 1
        self.__pisteet = self.__määrähaluttua*mitä
    def montasamaa(self, montako):
    #pisteytetään samoja olevat, montako on siis 2,3 tai 4
    #tarkastellaan numero kerrallaan kutoseen asti, näin saadaan varmasti
    #kahdesta parista tai täyskädestä varmasti se isompi, sillä looppi on
    #kasvavassa järjestyksessä ja näin myöskin isoin pistemäärä jää voimaan
        for i in range(6):
            self.__samoja = 0
            #ja jokainen noppa yksitellen
            for e in range(self.__noppienmäärä):
                if self.__nopat[e] == 1+i:
                    self.__samoja +=1
                    if self.__samoja == montako:
                        self.__pisteet = (montako)*(1+i)
    def kaksparia(self):
        #pisteytetään kaksi paria, selvitetään mitä silmälukuja on ainakin 2 kpl
        #noppien joukossa, nämä summataan yhteen ja kerrotaan kahdella
        kerrottava = 0
        for i in range(6):
            määrä = 0
            self.__kaksparialukittavat = []
            for e in range(self.__noppienmäärä):
                if self.__nopat[e] == i+1:
                    määrä +=1
                    self.__kaksparialukittavat.append(e)
                    if määrä == 2:
                        kerrottava += i+1
        self.__pisteet = 2*kerrottava
    def muille_pisteet(self):
        #pisteytetään täkäri tai sattuma, eli yksinkertaisesti viidellä nopalla
        #pelatessa näiden pistemäärä on kaikkien noppien summa
        self.__pisteet = 0
        for i in range(self.__noppienmäärä):
            self.__pisteet += self.__nopat[i]
    def sijoita(self):
        for i in range(6):
            self.__napit[i].configure(text=self.__pisteitä[i])
        for i in range(8,17):
            self.__napit[i].configure(text=self.__pisteitä[i])

        self.järjestelijä()
    def järjestelijä(self):
        for i in range(self.__noppienmäärä):
                self.__lukitukset[i].configure(state=NORMAL)
        if self.__pakkojatsi is True:
            self.__napit[self.__kierrokset].configure(state=NORMAL)
        else:
            for i in range(6):
                if self.__käytetty[self.__pelaaja][i] is False:
                    self.__napit[i].configure(state=NORMAL)
            for i in range(8,17):
                if self.__käytetty[self.__pelaaja][i] is False:
                    self.__napit[i].configure(state=NORMAL)
        if self.__heitot == 3:
            self.__heitä.configure(state=DISABLED)
            for i in range(self.__noppienmäärä):
                self.__lukitukset[i].configure(state=DISABLED)
            #jos kuitenkin pelataan jemmaheittojen kanssa on mahdollisuus, että
            #heittoja on vielä jäljellä, silloin myös lukitukset sallitaan
            if self.__heitotjemmaan is True:
                if self.__jemmaheitot[self.__pelaaja] > 0:
                    for i in range(self.__noppienmäärä):
                        self.__lukitukset[i].configure(state=NORMAL)
                    self.__lisänappi.configure(state=NORMAL)
        if self.__vastus.get() == 1 and self.__pelaaja == self.__pelaajat-1:
            for i in range(self.__noppienmäärä):
                self.__lukitukset[i].configure(state=DISABLED)
            self.__heitä.configure(state=DISABLED)
            for i in range(6):
                if self.__käytetty[self.__pelaaja][i] is False:
                    self.__napit[i].configure(state=DISABLED)
            for i in range(8,17):
                if self.__käytetty[self.__pelaaja][i] is False:
                    self.__napit[i].configure(state=DISABLED)
            if self.__heitotjemmaan is True:
                self.__lisänappi.configure(state=DISABLED)
            self.tekoäly()
    def samoja(self,i):
        self.__pistelaabelit[self.__pelaaja][i].configure(text=str(self.__pisteitä[i]))
        self.__käytetty[self.__pelaaja][i] = True
        self.__summa[self.__pelaaja] +=self.__pisteitä[i]
        self.__summailtavat[self.__pelaaja].append(self.__pisteitä[i])
        self.__total[self.__pelaaja] +=self.__pisteitä[i]
        self.__mitkä[self.__pelaaja] +=i+1
        self.eteenpäin()
    def tapaus(self,i):
    #pisteiden talletus muissa tapauksissa, tässä taas i on indeksi joka vastaa
    #taas samaa riviä kuin muuallakin
        pisteet = self.__pisteitä[i]
        self.__pistelaabelit[self.__pelaaja][i].configure(text=pisteet)
        self.__käytetty[self.__pelaaja][i] = True
        self.__total[self.__pelaaja] += pisteet
        self.eteenpäin()
    def yhteenveto(self):
        if len(self.__summailtavat[self.__pelaaja]) > 0:
            self.__pistelaabelit[self.__pelaaja][6].\
                configure(text=self.__summa[self.__pelaaja])
            if len(self.__summailtavat[self.__pelaaja]) == 6:
                if self.__summa[self.__pelaaja] >= 63:
                    self.__bonus[self.__pelaaja] = (self.__noppienmäärä-4)*50
                    self.__pistelaabelit[self.__pelaaja][7].\
                        configure(text=self.__bonus[self.__pelaaja])
                else:
                    self.__bonus[self.__pelaaja] = 0
                    self.__pistelaabelit[self.__pelaaja][7].\
                        configure(text=self.__bonus[self.__pelaaja])
                #lisätään tämä myös kerran loppupisteisiin, mutta vain kerran
                if self.__summattujo[self.__pelaaja] is False:
                    self.__total[self.__pelaaja] += self.__bonus[self.__pelaaja]
                    self.__summattujo[self.__pelaaja] = True
            #jos ei ole vielä kaikki täynnä annetaan arvio siitä, kuinka hyvin
            #ollaan tavoitteessa, eli tässä tilanteessa siis tavoite on aina
            #3x kutakin silmäluku (yht. 63)
            else:
                vertailu = self.__summa[self.__pelaaja]-(self.__noppienmäärä-2)\
                                        *self.__mitkä[self.__pelaaja]
                if vertailu > 0:
                    tavote = "+" + str(vertailu)
                elif vertailu < 0:
                    tavote = vertailu
                else:
                    tavote = "0"
                self.__pistelaabelit[self.__pelaaja][7].configure(text=tavote)
        self.__pistelaabelit[self.__pelaaja][17].\
            configure(text=self.__total[self.__pelaaja])
        #arvotaan nopat ja laitetaan silmäluvut noppalistaan
    def eteenpäin(self):
        self.yhteenveto()
        self.__heitäppä = False
        self.__äläheitä = True
        for i in range(self.__noppienmäärä):
                self.__lukinta[i] = False
                self.__lukitukset[i].configure(text="valitse",
                         background="lime green", state=DISABLED)
        for i in range(6):
            self.__napit[i].configure(text=" ",state=DISABLED)
        for i in range(8,16):
            self.__napit[i].configure(text=" ",state=DISABLED)
        self.__napit[16].configure(state=DISABLED,text="xD")
        if self.__kierrokset < 16 or (self.__kierrokset == 16 and
                                self.__pelaaja < self.__pelaajat-1):
            self.__heitä.configure(state=NORMAL)
            #jemmaheitot on erilaista pelimuotoa varten, siinä käyttämättömät
            #heitot voidaan säästää ja saadaan käyttää sitten myöhemmin
            if self.__heitotjemmaan is True:
                self.__jemmaheitot[self.__pelaaja] += (3-self.__heitot)
                self.__lisäheittoja[self.__pelaaja].configure\
                    (text=self.__jemmaheitot[self.__pelaaja])
                self.__lisänappi.configure(state=DISABLED)
            self.__heitot = 0
            #jos heittovuorossa oli kierroksen viimeinen pelaaja siirtyy vuoro
            #ensimmäiselle ja kierroksia kirjataan yksi lisää
            if self.__pelaaja == self.__pelaajat-1:
                self.__kukapelaa[self.__pelaaja].configure\
                    (text=self.__pelailijat[self.__pelaaja][0],state=DISABLED)
                self.__kukapelaa[0].configure\
                    (text=self.__pelailijat[0],state=NORMAL)
                #jos ollaan menossa kutosten kohdalla lisätään kierroksiin
                #kolme, jotta summa ja bonus jää välistä, näin vältytään taas
                #sekaannuksilta. Tämä toiminto on pakkojatsia varten.
                if self.__kierrokset == 5:
                    self.__kierrokset += 3
                else:
                    self.__kierrokset += 1
                self.__pelaaja = 0
            #muuten taas seuraava pelaaja saa vuoron
            else:
                self.__kukapelaa[self.__pelaaja].configure\
                    (text=self.__pelailijat[self.__pelaaja][0],state=DISABLED)
                self.__kukapelaa[self.__pelaaja+1].configure\
                    (text=self.__pelailijat[self.__pelaaja+1],state=NORMAL)
                self.__pelaaja += 1
                if self.__vastus.get() == 1 and self.__pelaaja == self.__pelaajat-1:
                    self.__heitä.configure(state=DISABLED)
                    self.__heitäppä = True

            if self.__vastus.get() == 1 and self.__pelaajat == 1:
                self.__heitä.configure(state=DISABLED)
                self.__heitäppä = True

        else:
            #jos jemmaheitot ovat päällä toimitaan vaan sen mukaisesti eli
            #lisätään kaikille jäljelle jääneet heitot pisteisiin
            if self.__heitotjemmaan is True:
                self.__jemmaheitot[self.__pelaaja] += (3-self.__heitot)
                self.__lisäheittoja[self.__pelaaja].configure\
                    (text=self.__jemmaheitot[self.__pelaaja])
                self.__lisänappi.configure(state=DISABLED)
                for i in range(self.__pelaajat):
                    self.__total[i] += self.__jemmaheitot[i]
                    self.__pistelaabelit[i][17].\
                        configure(text=self.__total[i])
            self.__heitä.configure(state=DISABLED)
            #jos pelaajia on yks tulos on yksinkertainen
            if self.__pelaajat == 1:
                tulos = "Tuloksesi",self.__total[self.__pelaaja]
            #muuten lasketaan se, kuka johtaa
            else:
                johdossa = 0
                #vai tulisko tasapeli..
                tasapeli = False
                for i in range (self.__pelaajat-1):
                    if self.__total[johdossa] < self.__total[i+1]:
                        johdossa = i+1
                        tasapeli = False
                    elif self.__total[johdossa] == self.__total[i+1] and johdossa == i:
                        tasapeli = True
                if tasapeli == False:
                    #jos ei tullut niin joku on voittaja!!
                    tulos = self.__pelailijat[johdossa], "voitti!"
                else:
                    #ja koska eihän kukaan tasapeliä halua
                    tulos = "Tasapeli... joo tiiän tuntuu pahemmalta ku häviö"
            #tehdään labeli jonne sijoitetaan tulosteksti
            label = Label(self.__ikkuna,text=tulos)
            label.grid(row=21, columnspan=38, sticky=E+W)
        if self.__heitäppä == True:
            self.heitä()
    def unlock(self):
        for i in range(self.__noppienmäärä):
            self.__lukinta[i] = False
            self.__lukitukset[i].configure(text="valitse",
                     background="lime green")

    def tekoäly(self):
        if self.__heitot < 3 or self.__jemmaheitot[self.__pelaaja] > 0:
            self.__vieläheittoja = True
        else:
            self.__vieläheittoja = False
        if self.__pakkojatsi is False:
            self.pelureistaparhain()
        else:
            self.pakkojatsittaja()

    def pelureistaparhain(self):
        time.sleep(0.5)
        self.__äläheitä = False
        self.__toimittu = False
        if self.__pisteitä[16] > 0 and self.__käytetty[self.__pelaaja][16] is False:
            self.tapaus(16)
        if self.__pisteitä[11] > 0 and self.__käytetty[self.__pelaaja][16] is False:
            self.lukitse(4)
        tarkasteltava = int((self.__pisteitä[11]/4)-1)
        if self.__pisteitä[11] > 0 and (self.__käytetty[self.__pelaaja][11] is False
                or self.__käytetty[self.__pelaaja][tarkasteltava] is False) and self.__käytetty[self.__pelaaja][16] is True:
            if self.__käytetty[self.__pelaaja][tarkasteltava] is True:
                self.tapaus(11)
            else:
                self.lukinta(4)
        elif self.__pisteitä[14] > 0 and self.__käytetty[self.__pelaaja][14] is False:
            self.tapaus(14)
        elif self.__pisteitä[13] > 0 and self.__käytetty[self.__pelaaja][13] is False:
            self.tapaus(13)
        elif self.__pisteitä[12] >= 22 and self.__käytetty[self.__pelaaja][12] is False:
            self.tapaus(12)
        if self.__vieläheittoja is True and self.__äläheitä is False:
            self.unlock()
            if self.__pisteitä[9] >= 18 and self.__käytetty[self.__pelaaja][12] is False:
                if self.__pisteitä[9] == 18:
                    self.parivalinta(4,5)
                elif self.__pisteitä[9] == 20:
                    self.parivalinta(4,6)
                elif self.__pisteitä[9] == 22:
                    self.parivalinta(5,6)
            if self.__pisteitä[9] >= 18 and self.__käytetty[self.__pelaaja][9] is False:
                self.tapaus(9)
            if self.__käytetty[self.__pelaaja][13] is False and self.__käytetty[self.__pelaaja][14] is False:
                self.suorailu(2,6)
            if self.__käytetty[self.__pelaaja][14] is False and self.__toimittu is False:
                self.suorailu(2,7)
            if self.__käytetty[self.__pelaaja][13] is False and self.__toimittu is False:
                self.suorailu(1,6)
            if self.__pisteitä[11] > 0 and self.__käytetty[self.__pelaaja][11] is False:
                self.lukitse(4)
            elif self.__pisteitä[10] >= 12 and self.__käytetty[self.__pelaaja][10] is False:
                self.lukitse(3)

            if self.__toimittu == False:
                self.enitenisointa()
            if self.__toimittu == False and (self.__käytetty[self.__pelaaja][11] is
                    False or self.__käytetty[self.__pelaaja][16] is False):
                self.lukitse(3)
            if self.__toimittu == False and self.__käytetty[self.__pelaaja][9] is False:
                self.kakspariaveto()
            if self.__toimittu == False and (self.__käytetty[self.__pelaaja][10] is False
                    or self.__käytetty[self.__pelaaja][11] is False or self.__käytetty[self.__pelaaja][16] is False):
                self.lukitse(2)
            if self.__toimittu == False and (self.__käytetty[self.__pelaaja][16]
                    is False or self.__käytetty[self.__pelaaja][11] is False
                        or self.__käytetty[self.__pelaaja][10] is False):
                for i in range(4):
                    self.lukitse(int(4-i))
                    if self.__toimittu is True:
                        break
            if self.__toimittu == False and self.__käytetty[self.__pelaaja][12] is False:
                self.täyskäsitys()
            if self.__toimittu == False and self.__käytetty[self.__pelaaja][10] is False:
                if self.__käytetty[self.__pelaaja][16] is False:
                    for i in range(4):
                        self.lukitse(int(4-i))
                        if self.__toimittu is True:
                            break
                elif self.__pisteitä[10] > 0:
                    self.tapaus(10)
            if self.__toimittu == False and self.__käytetty[self.__pelaaja][14] is False:
                self.puolisuorailu(2,7)
            if self.__toimittu == False and self.__käytetty[self.__pelaaja][13] is False:
                self.puolisuorailu(1,6)
            if self.__toimittu == False and self.__käytetty[self.__pelaaja][16] is False:
                for i in range(4):
                    self.lukitse(int(4-i))
                    if self.__toimittu is True:
                        break
            if self.__toimittu == False and self.__käytetty[self.__pelaaja][15] is False:
                for i in range(self.__noppienmäärä):
                    laskuri = 0
                    if self.__nopat[i] >= 4:
                        self.lukinta(i)
                        laskuri += 1
                    if laskuri == 5:
                        self.tapaus(15)
                self.__toimittu = True
            if self.__toimittu == False and self.__äläheitä is True and self.__käytetty[self.__pelaaja][11] is False:
                if self.__pisteitä[11] > 0:
                    self.tapaus(11)
            if self.__toimittu == False and self.__äläheitä is True and self.__käytetty[self.__pelaaja][10] is False:
                if self.__pisteitä[10] > 0:
                    self.tapaus(10)

            if self.__kierrokset < 16 or (self.__kierrokset == 16 and self.__vieläheittoja is True and self.__äläheitä == False):
                time.sleep(1)
                self.heitä()

        if self.__äläheitä is False:
            self.päättäjä()

    def pakkojatsittaja(self):
        self.__toimittu = False
        self.unlock()
        if self.__kierrokset <6:
            if self.__vieläheittoja is True and self.__pisteitä[self.__kierrokset] < 5*(self.__kierrokset+1):
                self.kaikkihalutut(int(self.__kierrokset+1))
                time.sleep(1)
                self.heitä()
            else:
                self.samoja(self.__kierrokset)


        if self.__toimittu is False and self.__kierrokset >= 8:
            if  self.__vieläheittoja is True:
                if self.__kierrokset == 8:
                    if self.__pisteitä[self.__kierrokset] >= 8:
                        self.tapaus(self.__kierrokset)
                    else:
                        self.lukitse(2)
                        time.sleep(1)
                        self.heitä()
                elif self.__kierrokset == 15:
                    if self.__pisteitä[self.__kierrokset] > 18:
                        self.tapaus(self.__kierrokset)
                    else:
                        for i in range(5):
                            if self.__nopat[i] > 3:
                                self.lukitse(i)
                        time.sleep(1)
                        self.heitä()
                else:
                    if self.__pisteitä[self.__kierrokset] > 0:
                        self.tapaus(self.__kierrokset)
                    else:
                        if self.__kierrokset == 9:
                            self.kakspariaveto()
                        elif self.__kierrokset == 10:
                            self.enitenisointa()
                        elif self.__kierrokset == 11:
                            self.enitenisointa()
                        elif self.__kierrokset == 12:
                            for e in range(len(self.__kaksparialukittavat)):
                                self.lukinta(self.__kaksparialukittavat[e])
                        elif self.__kierrokset == 13:
                            self.suorailu(1,6)
                        elif self.__kierrokset == 14:
                            self.suorailu(2,7)
                        elif self.__kierrokset == 16:
                            self.enitenisointa()
                        time.sleep(1)
                        self.heitä()
            else:
                if self.__toimittu == False:
                    self.tapaus(self.__kierrokset)

    def päättäjä(self):
        self.__päätetty = False
        for i in range(6):
            if self.__käytetty[self.__pelaaja][5-i] is False:
                if self.__pisteitä[5-i] >= 3*(6-i):
                    self.samoja(int(5-i))
                    self.__päätetty = True
        self.pisteettalteen(12)
        self.pisteettalteen(9)
        self.pisteettalteen(11)
        self.pisteettalteen(10)
        if self.__pisteitä[8] <=6:
            self.eikaimuuauta()
            self.pisteettalteen(8)
            self.pisteettalteen(15)
        else:
            self.pisteettalteen(8)
            self.pisteettalteen(15)
            self.eikaimuuauta()


        järjestys = [8,13,10,14,9,11,12,16]
        for i in range(8):
            if self.__päätetty == False and self.__käytetty[self.__pelaaja][järjestys[i]] is False:
                self.tapaus(järjestys[i])
                self.__päätetty = True
                break
        if self.__päätetty is False:
            for i in range(6):
                if self.__päätetty == False and self.__käytetty[self.__pelaaja][i] is False:
                    self.samoja(i)
                    self.__päätetty = True

    def täyskäsitys(self):
        if self.__pisteitä[9] > 0:
            self.lukitse(3)
            self.isoinmuumukaan(int(self.__pisteitä[9]/3))
        else:
            self.kakspariaveto()

    def eikaimuuauta(self):
        if self.__päätetty == False:
            for e in range(2):
                määrä = 2-e
                for i in range(6):
                    if self.__käytetty[self.__pelaaja][i] is False:
                        if self.__pisteitä[i] >= määrä*(1+i):
                            self.samoja(int(i))
                            self.__päätetty = True
                            break
                if self.__päätetty == True:
                    break

    def pisteettalteen(self, mikä, mitä = 0):
        if self.__päätetty == False and self.__käytetty[self.__pelaaja][mikä] is False:
            if self.__pisteitä[mikä] > mitä:
                self.tapaus(mikä)
                self.__päätetty = True

    def kakspariaveto(self):
        if self.__pakkojatsi is True:
            self.lukitse(2)
            self.isoinmuumukaan(self.__pisteitä[8]/2)
        elif self.__pisteitä[8] >= 6 and self.__käytetty[self.__pelaaja][9] is False:
            if self.__pisteitä[9] >= 14 and self.__käytetty[self.__pelaaja][9] is False:
                self.tapaus(9)
            else:
                self.lukitse(2)
                self.isoinmuumukaan(self.__pisteitä[8]/2)
        self.__toimittu = True

    def isoinmuumukaan(self,eikäy):
        riittää = False
        for i in range (6):
            numero = 6-i
            if numero != eikäy:
                for a in range(5):
                    if numero == self.__nopat[a]:
                        self.lukinta(a)
                        riittää = True
                        break
                if riittää == True:
                    break

    def kaikkihalutut(self, mikä):
        for i in range(5):
            if self.__nopat[i] == mikä:
                self.lukinta(i)

    def enitenisointa(self):
        lukittu = False
        if self.__pakkojatsi is True:
            for i in range(17):
                self.__käytetty[self.__pelaaja][i] = False
        for e in range(4):
            if e == 3 and self.__pakkojatsi is False:
                if self.__käytetty[self.__pelaaja][9] is False:
                    self.kakspariaveto()
                if self.__toimittu == False and self.__käytetty[self.__pelaaja][10] is False:
                    if self.__pisteitä[8] >= 8:
                        for i in range(4):
                            self.lukitse(int(4-i))
                            if self.__toimittu is True:
                                break

            if self.__toimittu == False:
                for i in range(6):
                    if self.__käytetty[self.__pelaaja][5-i] is False:
                        if self.__pisteitä[5-i] == (4-e)*(6-i):
                            for a in range(5):
                                if self.__nopat[a] == 6-i:
                                    self.lukinta(a)
                                    lukittu = True
                                    self.__toimittu = True

                    if lukittu is True:
                       break
                if lukittu is True:
                       break

    def lukitse(self,määrä):
        for i in range(6):
            if self.__pisteitä[5-i] >= määrä*(6-i):
                mones = 0
                for a in range(5):
                    if self.__nopat[a] == 6-i:
                        self.lukinta(a)
                        mones += 1
                        if mones == määrä:
                            self.__toimittu = True
                            break
                if self.__toimittu == True:
                    break
                    
    def puolisuorailu(self,mistä,mihin):
        for e in range(mistä,mihin):
            for i in range(self.__noppienmäärä):
                if self.__nopat[i] == e:
                    self.lukinta(i)
        self.__toimittu = True


    def suorailu(self,mistä,mihin):
        laskuri = 0
        indeksi = []
        for i in range(mistä,mihin):
            if i in self.__nopat:
                laskuri += 1
                indeksi.append(self.__nopat.index(i))
            if laskuri == 4:
                for i in range(len(indeksi)):
                    self.lukinta(indeksi[i])
                self.__toimittu = True
                break

    def parivalinta(self,joko,tai):
        self.__toimittu = True
        for i in range(5):
            if self.__nopat[i] == joko or self.__nopat[i] == tai:
                self.lukinta(i)

def main():
    Yatzy()


main()