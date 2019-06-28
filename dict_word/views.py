from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.http import HttpResponse

from .models import YoudaoResult, ContList
from .forms import SearchForm

import io
import sys
from bs4 import BeautifulSoup


# Create your views here.

def dict_word_index(request):
    youdao_result = YoudaoResult.get_all()
    #text_add = ContList.get_all()
    form = SearchForm()
    context = { 
        'youdao_result': youdao_result,
        'form':form
        }
    return render(request, 'dict_word/dict_word.html', context = context)

def dict_word_spider(request):

    # youdao_result = YoudaoResult.get_all()
    # context = { 'youdao_result': youdao_result }
    # return render(request, 'dict_word/dict_word.html', context = context)

    if request.method == 'POST':

        # delete last found results
        YoudaoResult.objects.all().delete()

        result = YoudaoResult()
        #text_add = ContList()
        form = SearchForm(request.POST)
        if form.is_valid():
            to_be_searched = form.cleaned_data.get('word')
            result.word = to_be_searched
            tmp = search_word(to_be_searched)
            result.text_ec = tmp[0]
            result.text_ce = tmp[1]
            result.text_cj = tmp[2]
            result.text_jc = tmp[3]
            # text_add = tmp[3]
            
            result.save()
            # text_add.save()

        #return render(request, 'dict_word/dict_word.html', context=context)
        return HttpResponseRedirect('/dict_word/')

    else:
        return HttpResponseRedirect('/dict_word/')

import requests
import re

def getHTMLText(url):
    try:
        headers = {
            'User-Agent': 'MMozilla/5.0 (Windows NT 6.1; WOW64; rv:31.0) Gecko/20100101 Firefox/31.0',
            'Cookie': '_REG=www.baidu.com|; _SREF_20=https://www.baidu.com/link?url%3DYgZhiKU4cjZA3BUbWbMl91N2DEyHtJn_CRhpzr8ltNCqxbmIAQ2TL-Lts-Cay_VF&wd%3D&eqid%3Db95db17a00019297000000035cf78f72; _SREG_20=www.baidu.com|; HJ_UID=50d90208-f823-b6cd-1388-8098b186714b; _REF=https://www.baidu.com/baidu.php?sc.Kf0000Ks1acltSXAQiWED2K29fCDLhh2CNRBdrIRxaG8_9yPE69ZQ5NQizP9Z_PibQvx1EqMDTqw94jwuYuEZ-fLBAVowgYlW_2GL_pVAst67aWdZ3KJ0MV4TpgaE0zoqeD5ilAR4T54dTwYaxMsckbDsA0--hDF4ZoUWRzPArEAHcuBfpQ0w0eV5ISBPwOD7eeLuO5yHQA4Bgh8Ns.DR_NR2Ar5O; HJ_CSST_3=1; HJ_SID=2622f51a-f843-b58e-c529-269fb5758bd2; HJ_SSID_3=575d00a9-c86f-93e7-f9aa-6bb141c0bb6a; _SREF_3=https://www.baidu.com/link?url%3DfXKyO1PCNRueg2-E2TII1wLwBsXvnAJm1DYtmoqrbcGtvucbzOEwtCC-MUURwAAe&wd%3D&eqid%3Dd248170d0000b1ef000000035d009a08; _SREG_3=www.baidu.com|; HJ_CST=0; TRACKSITEMAP=3%2C6%2C20%2C; _UZT_USER_SET_106_0_DEFAULT=2|09f709dcdd5456ab556468ed9a72d9bb'
        }

        r = requests.get(url , headers=headers)
        r.raise_for_status()    #如果状态不是200，引发HTTPError异常
        r.encoding = r.apparent_encoding
        return r.text
    except:
        return "产生异常"

def trans_youdao(text):
    soup = BeautifulSoup(text, 'html.parser')
    a = soup.select('div[class="trans-container"] p[class="wordGroup"] a')
    #b = soup.select('p[class="wordGroup"]')
    trans_res = ""
    trans_list = []
    for el in a:
        trans_list.append( el.get_text()  )
        trans_res = ", ".join(trans_list)
    return trans_res

def trans_youdao_ec(text):
    soup = BeautifulSoup(text, 'html.parser')
    trans_res = ""
    trans_list = []
    a = soup.select('div[class="trans-container"] ul')
    res = re.sub('\n', '  ', a[0].get_text() )
    trans_list.append( res  )
    trans_res = "\n".join(trans_list)
    #a = soup.find(class_="trans-container")
    # if a:
    #     trans_list.append( a.get_text()  )

    return trans_res

def trans_hj(text):
    soup = BeautifulSoup(text, 'html.parser')
    a = soup.select('section[class="detail-groups"] p')
    trans_res = ""
    trans_list = []
    for el in a:
        tmpTxt = el.get_text().strip()
        trans_list.append( tmpTxt  )
        trans_res = "\r\t".join(trans_list)
    #print(trans_res)
    return trans_res

def check_contain_eng(check_str):
    my_re = re.compile(r'[A-Za-z]',re.S)
    res = re.findall(my_re,check_str)
    if len(res):
        return True
    else:
        return False

def search_word(word):

    result = []
    if check_contain_eng(word):
        isCh = False
    else:
        isCh = True

    title = '英->中：<p></p>'
    if isCh==False:
        url = "http://dict.youdao.com/w/eng/" + word + "/#keyfrom=dict2.index"
        text = getHTMLText(url)
        result.append( trans_youdao_ec(text) )
    else:
        result.append('This word is Chinese')

    title = '中->英：<p></p>'
    if isCh:
        url = "http://dict.youdao.com/w/" + word + "/#keyfrom=dict2.index"
        text = getHTMLText(url)
        result.append(trans_youdao(text))
    else:
        result.append('This word is English')

    title = '\n 日->中：<p></p>'
    url = "https://dict.hjenglish.com/jp/jc/" + word
    text = getHTMLText(url)
    tmp = trans_hj(text)
    result.append(tmp)

    title = '中->日：<p></p>'
    url = "https://dict.hjenglish.com/jp/cj/" + word
    text = getHTMLText(url)
    tmp = trans_hj(text)
    result.append(tmp)


    #sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='utf8')
    # for kkk in result:
    #     print(kkk)

    # result_str = "<hr>".join(result)
    
    # with open("myfirst.html", "w", encoding='utf-8') as f:
    #     f.write(result_str)

    return result