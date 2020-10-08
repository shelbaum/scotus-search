
import requests
import json
import re 

def searchopinions(search_terms, start_date, end_date=''):

    cases = {}
    header = {'Authorization': 'Token 472e34f1c59af4a121cbfd333ac8d262223810a1'}
    url_parts = ['https://www.courtlistener.com/api/rest/v3/clusters/?date_filed__gte=','&date_filed__lte=','&docket__court__id=scotus&fields=id,case_name,date_filed,sub_opinions']
    if end_date:
        url = url_parts[0] + start_date + url_parts[1] + end_date + url_parts[2]
    else:
        url = url_parts[0] + start_date + url_parts[2]

    # Case object to contain case metadata, opinion text, and list of matches

    class Case:
        def __init__ (self, case_id, date_filed, case_name, opinion_url):
            self.case_id = case_id
            self.date_filed = date_filed
            self.case_name = case_name
            self.opinion_url = opinion_url
            self.opinion_text = ''
            self.download_url = ''
            self.matches = dict.fromkeys(search_terms)
        
        def check_matches(self):
            return all([not elem for elem in self.matches.values()])

    # get SCOTUS opinions filed on given date or in date range using CourtListener API, add Case object to cases dict for each. 

    r = requests.get(url, headers=header)
    r = r.json()

    for result in r["results"]:
        cases[result['id']] = Case(result['id'], result['date_filed'], result['case_name'], result['sub_opinions'])


    # For each Case object, get opinion text and download URL from opinions API endpoint, and search text for terms.

    for case in cases:
        r = requests.get(cases[case].opinion_url[0] + "?fields=download_url,plain_text", headers=header)
        r = r.json()
        
        cases[case].opinion_text = r['plain_text'].replace('-\n','').replace('\n',' ')
        cases[case].download_url = r['download_url']
        
        for term in search_terms:
            cases[case].matches[term] = []
            match_objects = re.finditer(term, cases[case].opinion_text)
            for match in match_objects:
                cases[case].matches[term].append(match.span())
          
    # Each Case object now contains metadata about the case, the opinion text (opinion, concurrences, and dissents all in one string),
    # and the indexes of all matches for each term in list

    return cases