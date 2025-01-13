import requests
import urllib.parse
import json

# writing to file
outfile = open('Heart_NHLBI_2002_oneline.txt', 'w', encoding="utf-8")
 
# Using readlines()
infile = open('Heart_disease_publications_NHLBI_2002.txt', 'r', encoding="utf-8")
institution_info = ''
pmid = ''
journal = ''

def determine_ror_id(institution_info):
    response =  None
    try:
        response = requests.get('https://api.ror.org/organizations?affiliation=' + urllib.parse.quote(institution_info)).json()
        number_of_results = response['number_of_results']
        if number_of_results > 0:
            institution_name = response['items'][0]['organization']['name']
            country = response['items'][0]['organization']['country']['country_name']        
        else:
            institution_name = 'not found'
            country = 'not found'
            print(institution_info, response)
    except:
        institution_name = 'not found'
        country = 'not found'
        print(institution_info)
        print(response)
    return (institution_name, country)

# Strips the newline character
while True:
    # Get next line from file
    line = infile.readline()
    # if line is empty
    # end of file is reached
    if not line:
        break
    if line.startswith('PMID'):

        if institution_info:
            institution_name, country = determine_ror_id(institution_info.strip())
            
            outfile.write(pmid.strip() + '|' + institution_info.strip() + '|' + institution_name + '|' + country + '|' + journal.strip() + '\n')
            institution_info = ''
            institution_name = ''
            country = ''
            
        line_tokens = line.split('- ')
        pmid = line_tokens[1].strip()

    if line.startswith('AD'):
        if not institution_info:
            line = line.replace('|',' ')
            line_tokens = line.split('- ')
            institution_info = line_tokens[1].strip()
            line = infile.readline()
            while line and line.startswith(' '):
                line = line.replace('|',' ')
                institution_info = institution_info + ' ' + line.strip()
                line = infile.readline()

    if line.startswith('JT'):       
        line_tokens = line.split('- ')
        journal = line_tokens[1].strip().lower()
        if journal.startswith('the'):
            sep = 'the'
            journal = journal.split(sep, 1)[1]
        if '(' in journal:
            sep = '('
            journal = journal.split(sep, 1)[0]
        elif ' :' in journal:
            sep = ' :'
            journal = journal.split(sep, 1)[0]

        line = infile.readline()
                
infile.close()
outfile.close()
