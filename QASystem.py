#!/usr/bin/env python3

import spacy
import sys
import requests
import re


def main(argv):
    input()
    

def input():
    #Hier open ik all_questions.txt en zorg ik ervoor dat alleen de vragen worden geanalyseerd en niet de s-nummers.
    f = open("all_questions.txt","r")
    f2 = open("output.txt","w+")
    counter = 0
    examples = []
    lines = f.readlines()
    for line in lines:
        line = line.split("\t")
        for x in line:
            x = x.strip()
            if not x.isdigit():
                examples.append(x)
    
    f.close()
    nlp = spacy.load('en')
    
    for line in examples:
        #print de vraag
        counter += 1
        f2.write(str(counter) + "\t")
        result = nlp(line.strip())
        query = ""
        ent = ""
        bent = ""
        iobents = ""
        for w in result:

            #Entity tagger
            if w.ent_iob_ == "I" and w.dep_ != "case" and w.dep != "punct":
                if ent == "":
                    ent = w.text
                else:
                    ent = ent + " " + w.text
            elif w.ent_iob_ == "B" and w.text.lower() != "the":
                bent = w.text
            query += w.text + " "
        if bent != "" or ent != "":
            iobents = bent + " " + ent
            
        result = nlp(query.strip())
        nsubj = []
        pobj = []
        dobj = []
        howx = []
        attr = []
        appos = []
        nsubjlist = ["nsubj","nsubjpass","ccsubj"]
        forbidden = ["what","who"]
        for w in result:
            if w.dep_ == "ROOT":
                root_string = w.text.lower()
            if w.dep_ == "appos":
                if w.pos_ == "NOUN" or w.pos_ == "PROPN":
                    appos.append(w)
            if w.dep_ in nsubjlist and w.text not in forbidden:
                if w.pos_ == "NOUN" or w.pos_ == "PROPN":
                    if result[w.i-1].dep_ == "amod" or result[w.i-1].dep_ == "acomp":
                        if result[w.i-1] not in howx:
                            nsubj.append(result[w.i-1])

                    nsubj.append(w)
            if w.lemma_ == "how":
                sub = list(w.ancestors)
                for anc in sub:
                    howx.append(anc)
                    break
            if w.dep_ == "pobj" or w.dep_ == "pcomp":
                if result[w.i-1].dep_ == "amod" or result[w.i-1].dep_ == "acomp":
                    if result[w.i-1] not in howx:
                        pobj.append(result[w.i-1])

                pobj.append(w)
            if w.dep_ == "dobj":
                if result[w.i-1].dep_ == "amod" or result[w.i-1].dep_ == "acomp":
                    if result[w.i-1] not in howx:
                        dobj.append(result[w.i-1])
                            
                dobj.append(w)
            if w.dep_ == "attr" and w.lemma_ not in forbidden:
                if result[w.i-1].dep_ == "amod" or result[w.i-1].dep_ == "acomp":
                    if result[w.i-1] not in howx:
                        attr.append(result[w.i-1])
                attr.append(w)
        

        nodep = ["det","predet"]
        nomany = ["many", "much","-pron-"]
        
        nsubj2 = [x.text.lower() for x in nsubj if x.dep_ not in nodep and x.dep_ == "amod" or x.dep_ == "acomp" and x.text.lower() not in nomany and x.text.lower() not in iobents.lower()]
        
        nsubj3 = [x.lemma_ for x in nsubj if x.dep_ not in nodep and x.dep_ != "amod" and x.dep_ != "acomp" and x.text.lower() not in iobents.lower() and x.lemma_ != "-PRON-"]
        nsubj = nsubj2 + nsubj3
        pobj2 = [x.text.lower() for x in pobj if x.dep_ not in nodep and x.dep_ == "amod" or x.dep_ == "acomp" and x.text.lower() not in nomany and x.text.lower() not in iobents.lower()]
        pobj3 = [x.lemma_ for x in pobj if x.dep_ not in nodep and x.dep_ != "amod" and x.dep_ != "acomp" and x.text.lower() not in iobents.lower() and x.lemma_ != "-PRON-"]
        pobj = pobj2 + pobj3
        dobj2 = [x.text.lower() for x in dobj if x.dep_ not in nodep and x.dep_ == "amod" or x.dep_ == "acomp" and x.text.lower() not in nomany and x.text.lower() not in iobents.lower()]
        dobj3 = [x.lemma_ for x in dobj if x.dep_ not in nodep and x.dep_ != "amod" and x.dep_ != "acomp" and x.text.lower() not in iobents.lower() and x.lemma_ != "-PRON-"]
        dobj = dobj2 + dobj3
        attr2 = [x.text.lower() for x in attr if x.dep_ not in nodep and x.dep_ == "amod" or x.dep_ == "acomp" and x.text.lower() not in nomany and x.text.lower() not in iobents.lower()]
        attr3 = [x.lemma_ for x in attr if x.dep_ not in nodep and x.dep_ != "amod" and x.dep_ != "acomp" and x.text.lower() not in iobents.lower() and x.lemma_ != "-PRON-"]
        attr = attr2 + attr3
        appos2 = [x.text.lower() for x in appos if x.dep_ not in nodep and x.dep_ == "amod" or x.dep_ == "acomp" and x.text.lower() not in nomany and x.text.lower() not in iobents.lower()]
        appos3 = [x.lemma_ for x in appos if x.dep_ not in nodep and x.dep_ != "amod" and x.dep_ != "acomp" and x.text.lower() not in iobents.lower() and x.lemma_ != "-PRON-"]
        appos = appos2 + appos3
        nsubj_string = False
        pobj_string = False
        dobj_string = False
        howx_string = False
        attr_string = False
        appos_string = False
        for item in nsubj:
            if nsubj_string == False:
                nsubj_string = item
            else:
                nsubj_string += " " + item
        for item in appos:
            if appos_string == False:
                appos_string = item
            else:
                appos_string += " " + item
        for item in pobj:
            if pobj_string == False:
                pobj_string = item
            else:
                pobj_string += " " + item
        for item in attr:
            if attr_string == False:
                attr_string = item
            else:
                attr_string += " " + item

        for item in dobj:
            if dobj_string == False:
                dobj_string = item
            else:
                dobj_string += " " + item
        
        for item in howx:
            if howx_string == False:
                howx_string = item.text
            else:
                howx_string += " " + item.text
        #queries for error handling
        #print("nsubj_string: ",nsubj_string)
        #print("appos: ",appos_string)
        #print("pobj_string:", pobj_string)
        #print("dobj_string: ", dobj_string)
        #print("howx_string: ", howx_string)
        #print("attr_string: ", attr_string)
        #print("iobents: ", iobents)
        #Geprobeerd iets te verzinnen waardoor die meerdere opties probeert, als er meerdere opties zijn om te zoeken.
        yesnokeys = ["is", "do", "does"]
        if result[0].text.lower() == "how":
            if howx_string != "many" and howx_string != "much":
                if iobents and nsubj_string:
                    make_query_what_complex(nsubj_string, iobents, howx_string)
                elif iobents:
                    make_query_how(howx_string,iobents)
                else:
                    if appos_string:
                        make_query_how(howx_string,appos_string)
                    else:
                        if nsubj_string:
                            make_query_how(howx_string,nsubj_string)
                            
            else:
                if dobj_string and iobents:
                    make_query_howmany(dobj_string,iobents)
                elif root_string and iobents:
                    make_query_howmany(root_string,iobents)
                
        elif result[0].text.lower() in yesnokeys:
            if result[0].text.lower() != "is":
                if iobents:
                    make_query_does(dobj_string, iobents)
                else:
                    make_query_does(dobj_string, nsubj_string)
            else:
                if iobents:
                    make_query_is(iobents, nsubj_string, attr_string)
                else:
                    try:
                        make_query_is(pobj_string, nsubj_string, attr_string)
                    except:
                        pass
                        
                        
        elif pobj_string and nsubj_string and iobents:
            make_query_what(nsubj_string,iobents)
            make_query_what(pobj_string,iobents)
            make_query_what_complex(pobj_string, iobents, nsubj_string)
        elif dobj_string and pobj_string and iobents:
            make_query_what(dobj_string,iobents)
            make_query_what(pobj_string,iobents)
            make_query_what_complex(pobj_string, iobents, dobj_string)
        elif iobents and nsubj_string and dobj_string:
            make_query_what(dobj_string, iobents)

        else:  
            if dobj_string and iobents:
                make_query_what(dobj_string, iobents)
            
            elif pobj_string and nsubj_string:
                make_query_what(nsubj_string, pobj_string)
        
            elif iobents and nsubj_string:
                make_query_what(nsubj_string, iobents)
            
            elif pobj_string and iobents:
                make_query_what(pobj_string, iobents)

            elif attr_string and iobents:
                if pobj_string:
                    make_query_complex(pobj_string,iobents,attr_string)
                make_query_what(attr_string, iobents)
        
            elif pobj_string and dobj_string:
                make_query_what(dobj_string, pobj_string)

            elif nsubj_string and not pobj_string and not iobents:
                make_query_definition(nsubj_string)
            
            elif iobents:
              make_query_definition(iobents)
        f2.write("\n")
    f2.close() 

def make_query_howmany(prop,entity):
    f3 = open("output.txt","a+")
    url = "https://www.wikidata.org/w/api.php"
    url2 = "https://query.wikidata.org/sparql"
    paramsE = {"action":"wbsearchentities", "language":"en", "format":"json"}
    paramsP = {"action":"wbsearchentities", "language":"en", "format":"json", "type": "property"}

    paramsE["search"] = entity
    paramsP["search"] = prop

    jsonE = requests.get(url,paramsE).json()
    jsonP = requests.get(url,paramsP).json()
    for result in jsonE["search"]:
        y = result["id"]
        break
    for result in jsonP["search"]:
        x = result["id"]
        break
    
    try:
        if prop == "citizen":
            prop = "population"
            make_query_what(prop,entity)
        else:
            query = """
            SELECT (COUNT(wdt:%s) AS ?count)
            WHERE { wd:%s wdt:%s ?count
            SERVICE wikibase:label {bd:serviceParam wikibase:language "nl" .} }
            """%(x, y, x)
            data = requests.get(url2, params={"query": query, "format": "json"}).json()
                    
            # If there is no answer to be found, send a message that says so
            if data["results"]["bindings"] != []:
                for item in data["results"]["bindings"]:
                    for var in item :
                        f3.write(item[var]["value"] + "\t")

    except UnboundLocalError as err:
        print(err)
    f3.close()
        
def make_query_how(prop,entity):
    f4 = open("output.txt","a+")
    url = "https://www.wikidata.org/w/api.php"
    url2 = "https://query.wikidata.org/sparql"
    paramsE = {"action":"wbsearchentities", "language":"en", "format":"json"}
    paramsP = {"action":"wbsearchentities", "language":"en", "format":"json", "type": "property"}

    sizesynonyms = ["big", "large", "high"]
    if prop in sizesynonyms:
        prop = "size"

    paramsE["search"] = entity
    paramsP["search"] = prop

    jsonE = requests.get(url,paramsE).json()
    jsonP = requests.get(url,paramsP).json()
    for result in jsonE["search"]:
        y = result["id"]
        break
    for result in jsonP["search"]:
        x = result["id"]
        break

    try:
        query = """
            SELECT ?answerLabel WHERE { 
            wd:%s wdt:%s ?answer. 
            SERVICE wikibase:label { bd:serviceParam wikibase:language "en" } 
            }""" %(y, x)
        data = requests.get(url2, params={"query": query, "format": "json"}).json()
                
        # If there is no answer to be found, send a message that says so
        if data["results"]["bindings"] == []:
            if prop == "size":
                prop = "area"
            paramsP["search"] = prop
            jsonP = requests.get(url,paramsP).json()
            for result in jsonP["search"]:
                x = result["id"]
                break
            query = """
                SELECT ?answerLabel WHERE { 
                wd:%s wdt:%s ?answer. 
                SERVICE wikibase:label { bd:serviceParam wikibase:language "en" } 
                }""" %(y, x)
            data = requests.get(url2, params={"query": query, "format": "json"}).json()
            if data["results"]["bindings"] != []:
                for item in data["results"]["bindings"]:
                    for var in item :
                        f4.write(item[var]["value"] + "\t")

        else:
            for item in data["results"]["bindings"]:
                for var in item :
                    f4.write(item[var]["value"] + "\t")
        
    except UnboundLocalError as err:
        print(err)
    f4.close()  

def make_query_what(prop, entity):
    f5 = open("output.txt","a+")
    url = "https://www.wikidata.org/w/api.php"
    url2 = "https://query.wikidata.org/sparql"
    paramsE = {"action":"wbsearchentities", "language":"en", "format":"json"}
    paramsP = {"action":"wbsearchentities", "language":"en", "format":"json", "type": "property"}

    paramsE["search"] = entity
    paramsP["search"] = prop

    jsonE = requests.get(url,paramsE).json()
    jsonP = requests.get(url,paramsP).json()
    for result in jsonE["search"]:
        y = result["id"]
        break
    for result in jsonP["search"]:
        x = result["id"]
        break

    # Define the question in a SPARQL query
    try:
        query = """
                SELECT ?answerLabel WHERE { 
                    wd:%s wdt:%s ?answer. 
                    SERVICE wikibase:label { bd:serviceParam wikibase:language "en" } }""" %(y, x)
        data = requests.get(url2, params={"query": query, "format": "json"}).json()

        # If there is no answer to be found, send a message that says so
        if data["results"]["bindings"] == []:
            # Solve the issue country of origin/nationality for objects and for people
            if x == "P17":
                x = "P27"
            elif x == "P131":
                x = "P36"
            elif x == "P1412":
                x = "P37"
                
            query = """
                SELECT ?answerLabel WHERE { 
                    wd:%s wdt:%s ?answer. 
                    SERVICE wikibase:label { bd:serviceParam wikibase:language "en" } }""" %(y, x)
            data = requests.get(url2, params={"query": query, "format": "json"}).json()
            if data["results"]["bindings"] == []:
                print()
            else:
                for item in data["results"]["bindings"]:
                    for var in item :
                        f5.write(item[var]["value"] + "\t")

        else:
            for item in data["results"]["bindings"]:
                for var in item :
                    f5.write(item[var]["value"] + "\t")

    #if x or y isnt defined 		
    except UnboundLocalError as err:
        print(err)
    f5.close()

def make_query_what_complex(prop, entity, subprop):
    f6 = open("output.txt","a+")
    url = "https://www.wikidata.org/w/api.php"
    url2 = "https://query.wikidata.org/sparql"
    paramsE = {"action":"wbsearchentities", "language":"en", "format":"json"}
    paramsP = {"action":"wbsearchentities", "language":"en", "format":"json", "type": "property"}
    paramsP2 = {"action":"wbsearchentities", "language":"en", "format":"json", "type": "property"}

    sizesynonyms = ["big", "large", "high"]
    if subprop in sizesynonyms:
        subprop = "height"

    paramsE["search"] = entity
    paramsP["search"] = prop
    paramsP2["search"] = subprop

    jsonE = requests.get(url,paramsE).json()
    jsonP = requests.get(url,paramsP).json()
    jsonP2 = requests.get(url,paramsP2).json()
    for result in jsonE["search"]:
        y = result["id"]
        break
    for result in jsonP["search"]:
        x = result["id"]
        break
    for result in jsonP2["search"]:
        n = result["id"]
        break
    # Define the question in a SPARQL query
    try:
        query = """
                SELECT ?height WHERE {
                    SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }
                    wd:%s wdt:%s ?item.
                    OPTIONAL { ?item wdt:%s ?height. }
                }""" %(y, x, n)
        data = requests.get(url2, params={"query": query, "format": "json"}).json()

        # If there is no answer to be found, send a message that says so
        if data["results"]["bindings"] == []:
            # Solve the issue country of origin/nationality for objects and for people
            if x == "P17":
                x = "P27"
            elif x == "P131":
                x = "P36"
            elif x == "P1412":
                x = "P37"
                
            query = """
                SELECT ?answerLabel WHERE { 
                    wd:%s wdt:%s ?answer. 
                    SERVICE wikibase:label { bd:serviceParam wikibase:language "en" } }""" %(y, x)
            data = requests.get(url2, params={"query": query, "format": "json"}).json()
            if data["results"]["bindings"] == []:
                if subprop == "height":
                    subprop = "area"
                paramsP["search"] = prop
                jsonP = requests.get(url,paramsP).json()
                for result in jsonP["search"]:
                    x = result["id"]
                    break
                query = """
                    SELECT ?answerLabel WHERE { 
                    wd:%s wdt:%s ?answer. 
                    SERVICE wikibase:label { bd:serviceParam wikibase:language "en" } 
                    }""" %(y, x)
                data = requests.get(url2, params={"query": query, "format": "json"}).json()
                if data["results"]["bindings"] == []:
                    pass
                else:
                    for item in data["results"]["bindings"]:
                        for var in item :
                            f6.write(item[var]["value"] + "\t")

            else:
                for item in data["results"]["bindings"]:
                    for var in item :
                        f6.write(item[var]["value"] + "\t")

        else:
            for item in data["results"]["bindings"]:
                for var in item :
                    f6.write(item[var]["value"] + "\t")

    #if x or y isnt defined 		
    except UnboundLocalError as err:
        print(err)
    f6.close()

def make_query_definition(entity):
    f7 = open("output.txt","a+")
    url = "https://www.wikidata.org/w/api.php"
    url2 = "https://query.wikidata.org/sparql"
    paramsE = {"action":"wbsearchentities", "language":"en", "format":"json"}

    paramsE["search"] = entity
    jsonE = requests.get(url,paramsE).json()
    for result in jsonE["search"]:
        y = result["id"]
        break


    # Define the question in a SPARQL query
    try:
        query = """
                SELECT ?item
                WHERE {
                    wd:%s schema:description ?item.
                    FILTER ( lang(?item) = "en" )
                }""" %(y)

        data = requests.get(url2, params={"query": query, "format": "json"}).json()

        # If there is no answer to be found, send a message that says so
        if data["results"]["bindings"] != []:
            for item in data["results"]["bindings"]:
                for var in item :
                    f7.write(item[var]["value"] + "\t")

    except UnboundLocalError as err:
        print(err)
    f7.close()
    
def make_query_does(prop, entity):
    f8 = open("output.txt","a+")
    url = "https://www.wikidata.org/w/api.php"
    url2 = "https://query.wikidata.org/sparql"
    paramsE = {"action":"wbsearchentities", "language":"en", "format":"json"}
    paramsP = {"action":"wbsearchentities", "language":"en", "format":"json", "type": "property"}

    paramsE["search"] = entity
    paramsP["search"] = prop


    jsonE = requests.get(url,paramsE).json()
    jsonP = requests.get(url,paramsP).json()
    for result in jsonE["search"]:
        y = result["id"]
        break
    for result in jsonP["search"]:
        x = result["id"]
        break
    # Define the question in a SPARQL query

    try:
        query = """
            ASK WHERE {
            wd:%s wdt:%s ?item.
            SERVICE wikibase:label { bd:serviceParam wikibase:language 'en'}
            }""" %(y, x)

        data = requests.get(url2, params={"query": query, "format": "json"}).json()

        # If there is no answer to be found, send a message that says so
        if data["boolean"] == True:
            f8.write("Yes" + "\t")
        elif data["boolean"] == False:
            f8.write("No" + "\t")
    except UnboundLocalError as err:
        print(err)
    f8.close()
        
def make_query_is(iobents, nsubj_string, attr_string):
    f9 = open("output.txt","a+")
    url = "https://www.wikidata.org/w/api.php"
    url2 = "https://query.wikidata.org/sparql"
    paramsE = {"action":"wbsearchentities", "language":"en", "format":"json"}
    paramsP = {"action":"wbsearchentities", "language":"en", "format":"json", "type": "property"}
    paramsN = {"action":"wbsearchentities", "language":"en", "format":"json"}    
    # Is Germany a country?
    if nsubj_string == False:
        paramsE["search"] = iobents
        paramsN["search"] = attr_string

        jsonE = requests.get(url,paramsE).json()
        jsonN = requests.get(url,paramsN).json()
        for result in jsonE["search"]:
            y = result["id"]
            break
        for result in jsonN["search"]:
            n = result["id"]
            break
        # Solve ambiguity with country and country music
        if n == "Q83440":
            n = "Q6256"
        # Define the question in a SPARQL query
        try:
            query = """
                ASK WHERE {
                wd:%s ?p wd:%s.
                FILTER (?p = wdt:P31 || ?p = wdt:P39)
                SERVICE wikibase:label { bd:serviceParam wikibase:language 'en'}
                }""" %(y, n)

            data = requests.get(url2, params={"query": query, "format": "json"}).json()

            if data["boolean"] == True:
                f9.write("\n,\t,Yes")
            elif data["boolean"] == False:
                f9.write("\n,\t,No")
                
        except UnboundLocalError as err:
            print(err)   
    
    else:
        paramsE["search"] = iobents
        paramsP["search"] = attr_string
        paramsN["search"] = nsubj_string

        jsonE = requests.get(url,paramsE).json()
        jsonP = requests.get(url,paramsP).json()
        jsonN = requests.get(url,paramsN).json()
        for result in jsonE["search"]:
            y = result["id"]
            break
        for result in jsonP["search"]:
            x = result["id"]
            break
        for result in jsonN["search"]:
            n = result["id"]
            break

        # Define the question in a SPARQL query
        try:
            query = """
                ASK WHERE {
                wd:%s wdt:%s wd:%s.
                SERVICE wikibase:label { bd:serviceParam wikibase:language 'en'}
                }""" %(y, x, n)

            data = requests.get(url2, params={"query": query, "format": "json"}).json()

            if data["boolean"] == True:
                f9.write("Yes" + "\t")
            elif data["boolean"] == False:
                f9.write("No" + "\t")
                
        except UnboundLocalError as err :
            print(err)
    f9.close()

                
if __name__ == "__main__":
        main(sys.argv)
