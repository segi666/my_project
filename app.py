from pymongo import MongoClient
from flask import Flask, render_template, jsonify, request
from urllib.parse import urlencode, quote_plus
import xml.etree.ElementTree as elemTree
import requests

client = MongoClient('localhost', 27017)
db = client.dbsparta

app = Flask(__name__)


@app.route('/')
def home():  # 함수명 수정 - 이름만 보고 접속되는 페이지를 확인할 수 있게!
    return render_template('index.html')


@app.route('/search')
def search():
    name_receive = request.args.get('name')
    return render_template('search.html', name=name_receive)


@app.route('/result')
def result():
    name_receive = request.args.get('name')
    code_receive = request.args.get('code')
    return render_template('result.html', name=name_receive, code=code_receive)

@app.route('/course')
def course():  # 함수명 수정 - 이름만 보고 접속되는 페이지를 확인할 수 있게!
    return render_template('tranggle.html')

# 산 name으로 산 정보 검색
@app.route('/find_mt', methods=['GET'])
def find_mt():
    name_receive = request.args.get('name')
    mountain_list = get_mountain(name_receive)

    # 최종 산 배열
    return jsonify({'result': 'success', 'data': mountain_list})

# 산 name과 mntnid로 하나의 산 정보 가져오기
@app.route('/find_mt_one', methods=['GET'])
def find_mt_one():
    name = request.args.get('name')
    code_receive = request.args.get('code')
    mountain_list = get_mountain(name)
    mountain = {}
    for mnt in mountain_list:

        if mnt['mntnid'] == code_receive:
            mountain = mnt
            break # mntnid가 일치하는 산을 찾으면 반복문 종료

    # 최종 산
    return jsonify({'result': 'success', 'data': mountain})


# 산 정보를 가져오는 함수가 여러 곳에서 쓰이기 때문에 별도의 함수로 분리
def get_mountain(name):
    # 발급 받으신 일반 인증키를 입력해주세요
    service_key = 'XqZgwrNvip5uzGt4Or30eqpEbhmFB%2FATnalq2ZUPZ5X0LAd%2B8fZpL%2BwXRG44MU%2FJ%2Fn7Zd5OKehu4xayFvVb48Q%3D%3D'
    # 산 이름을 입력해주세요
    queryParams = '?' + urlencode(
        {quote_plus('ServiceKey'): service_key, quote_plus('mntnNm'): name, quote_plus('mntnHght'): '',
         quote_plus('mntnAdd'): '', quote_plus('mntnInfoAraCd'): '', quote_plus('mntnInfoSsnCd'): '',
         quote_plus('mntnInfoThmCd'): ''})
    url = 'http://api.forest.go.kr/openapi/service/trailInfoService/getforeststoryservice' + queryParams
    print(f'요청 URL : {url}')
    res = requests.get(url)
    tree = elemTree.fromstring(res.text)
    items = tree.find('body').find('items').findall('item')
    mountain_list = []
    for item in items:
        mountain = {
            'crcmrsghtngetcimageseq': item.find('crcmrsghtngetcimageseq').text.strip(),
            'crcmrsghtnginfodscrt': item.find('crcmrsghtnginfodscrt').text.strip(),
            'crcmrsghtnginfoetcdscrt': item.find('crcmrsghtnginfoetcdscrt').text.strip(),
            'hkngpntdscrt': item.find('hkngpntdscrt').text.strip(),
            'hndfmsmtnmapimageseq': item.find('hndfmsmtnmapimageseq').text.strip(),
            'hndfmsmtnslctnrson': item.find('hndfmsmtnslctnrson').text.strip(),
            'mntnattchimageseq': item.find('mntnattchimageseq').text.strip(),
            'mntnid': item.find('mntnid').text.strip(),
            'mntninfodscrt': item.find('mntninfodscrt').text.strip(),
            'mntninfodtlinfocont': item.find('mntninfodtlinfocont').text.strip(),
            'mntninfohght': item.find('mntninfohght').text.strip(),
            'mntninfomangrtlno': item.find('mntninfomangrtlno').text.strip(),
            'mntninfomapdnldfilenm': item.find('mntninfomapdnldfilenm').text.strip(),
            'mntninfomngmemnbdnm': item.find('mntninfomngmemnbdnm').text.strip(),
            'mntninfopoflc': item.find('mntninfopoflc').text.strip(),
            'mntninfotrnspinfoimageseq': item.find('mntninfotrnspinfoimageseq').text.strip(),
            'mntnnm': item.find('mntnnm').text.strip(),
            'mntnsbttlinfo': item.find('mntnsbttlinfo').text.strip(),
            'pbtrninfodscrt': item.find('pbtrninfodscrt').text.strip(),
            'ptmntrcmmncoursdscrt': item.find('ptmntrcmmncoursdscrt').text.strip(),
            'rcmmncoursimageseq': item.find('rcmmncoursimageseq').text.strip(),
        }
        print(f'{mountain["mntnnm"]} / {mountain["mntninfopoflc"]}')
        mountain_list.append(mountain)
    return mountain_list

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
