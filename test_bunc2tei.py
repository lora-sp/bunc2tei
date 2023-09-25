import xml.etree.ElementTree as ET
from bunc2tei import extract_data


def test_extract_data():

    # Assertions concerning the Chitanka corpus
    data_lit, genre_lit = extract_data('sample/chitanka.info - Lady Pol the BELOVED.xml')

    assert data_lit[0]['author'] == "Lady Pol the BELOVED"
    assert data_lit[1]['author'] == "Lady Pol the BELOVED"

    assert data_lit[0]['title'] == "Наследството"
    assert data_lit[1]['title'] == "Морска звезда"

    assert data_lit[0]['genre'] == "Българско фентъзи/Разказ"
    assert data_lit[1]['genre'] == "Българско фентъзи/Разказ"

    assert data_lit[0]['url'] == "http://chitanka.info/text/42282/0"
    assert data_lit[1]['url'] == "http://chitanka.info/text/39970/0"



    # Assertions concerning the ParlaMint corpus    
    data_parl, genre_parl = extract_data('sample/ParlaMint-BG_2014-10-27.xml')

    assert data_parl[0]['speaker'] == '#DanailovStefan'
    assert data_parl[1]['speaker'] == '#PlevnelievRosen'

    assert data_parl[0]['sex'] == 'M'
    assert data_parl[1]['sex'] == 'M'



    # Assertions concerning the online newspaper corpus
    data_news, genre_news = extract_data('sample/dnevnik.bg - 2020-01-01.xml')

    assert data_news[0]['author'] == "Дневник"
    assert data_news[1]['author'] == "Георги Пауновски"
    assert data_news[2]['author'] == "Елена Геловска"
   
    assert data_news[0]['title'] == "Най-ефективните методи за справяне с махмурлука"
    assert data_news[1]['title'] == "Полицията регистрира няколко катастрофи с пияни шофьори в новогодишната нощ"
    assert data_news[2]['title'] == "Какво влиза в сила от 1 януари 2020 г."  

    assert data_news[0]['time'] == "10:41"
    assert data_news[1]['time'] == "12:07"
    assert data_news[2]['time'] == "07:33"

