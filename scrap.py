import requests
from requests_html import HTMLSession

def parser(first_name, last_name, birth_date):
    session = HTMLSession()
    url = 'https://isir.justice.cz/isir/ueu/vysledek_lustrace.do?'

    data = {
        # 'nazev_osoby': 'Novak',
        'nazev_osoby': last_name,
        # 'jmeno_osoby': 'Jan',
        'jmeno_osoby': first_name,
        'ic': '',
        # 'datum_narozeni': '08.07.1952',
        'datum_narozeni': birth_date,
        'rc': '',
        'mesto': '',
        'cislo_senatu': '',
        'bc_vec': '',
        'rocnik': '',
        'id_osoby_puvodce': '',
        'druh_stav_konkursu': '',
        'datum_stav_od': '',
        'datum_stav_do': '',
        'aktualnost': 'AKTUALNI_I_UKONCENA',
        'druh_kod_udalost': '',
        'datum_akce_od': '',
        'datum_akce_do': '',
        'nazev_osoby_f': '',
        'cislo_senatu_vsns': '',
        'druh_vec_vsns': '',
        'bc_vec_vsns': '',
        'rocnik_vsns': '',
        'cislo_senatu_icm': '',
        'bc_vec_icm': '',
        'rocnik_icm': '',
        'rowsAtOnce': 50,
        'captcha_answer': '',
        'spis_znacky_datum': '',
        'spis_znacky_obdobi': '14DNI'
    }

    r = requests.post(url, params = data)
    r = session.get(r.url)
    detail = r.html.find('a', containing='Detail')[0]
    detail_url = detail.absolute_links.pop()
    r = requests.get(detail_url)
    r = session.get(r.url)
    tr = r.html.find('tr', containing='Datum poslední zveřejněné události')[0]
    b = tr.find('b')[0]
    date_of_last_published_event = b.text

    zalozkaB = r.html.find('#zalozkaB', first=True)
    table = zalozkaB.find('.evidenceUpadcuDetailTable', first=True)
    trs = table.find('tr')[1::]
    dates = []
    for x in trs:
        dates.append(x.find('td')[1].text)
    return dates

# print('Dates:')
# txt = '{}: '
# for x in dates:
#   print(txt.format(dates.index(x) + 1) + x)
# print()
# print('Date of last published event: ' + date_of_last_published_event)