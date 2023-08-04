import xml.etree.ElementTree as ET
from bunc2tei import extract_data


def test_extract_data():
    tree = ET.parse('sample.xml')
    root = tree.getroot()

    data = extract_data('sample.xml')
    assert len(data) == len(root.findall(".{http://www.tei-c.org/ns/1.0}text"))

    assert data[0]['title'] == 'Най-ефективните методи за справяне с махмурлука'
    assert data[1]['title'] == 'Полицията регистрира няколко катастрофи с пияни шофьори в новогодишната нощ'
    assert data[2]['title'] == 'Какво влиза в сила от 1 януари 2020 г.'

    assert data[0]['url'] == 'https://www.dnevnik.bg/detski_dnevnik/zdrave/2020/01/01/4011288_nai-efektivnite_metodi_za_spraviane_s_mahmurluka/'
    assert data[1]['url'] == 'https://www.dnevnik.bg/skorost/2020/01/01/4011314_policiiata_registrira_niakolko_katastrofi_s_piiani/'
    assert data[2]['url'] == 'https://www.dnevnik.bg/bulgaria/2020/01/01/4007490_kakvo_vliza_v_sila_ot_1_ianuari_2020_g/'

    assert data[0]['author'] == 'Дневник'
    assert data[1]['author'] == 'Георги Пауновски'
    assert data[2]['author'] == 'Елена Геловска'

    for i in range(len(data)):
        assert data[i]['date'] == '2020-01-01'

    assert data[0]['time'] == '10:41'
    assert data[1]['time'] == '12:07'
    assert data[2]['time'] == '07:33'

  



