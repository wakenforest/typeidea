from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.http import HttpResponse

from .models import YoudaoResult
from .forms import SearchForm

import io
import sys

# Create your views here.

def dict_word_index(request):
    youdao_result = YoudaoResult.get_all()
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
        form = SearchForm(request.POST)
        if form.is_valid():
            to_be_searched = form.cleaned_data.get('word')
            result.word = to_be_searched
            result.text = search_word(to_be_searched)
            result.save()

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

def anaText(text):
    result = ''

    pat = re.compile('<span class="pronounce">英.*?<span class="phonetic">(.*?)</span>',re.S)
    grp = pat.search(text)
    if grp:
        result = result + grp[1]

    pat = re.compile('<span class="pronounce">美.*?<span class="phonetic">(.*?)</span>', re.S)
    grp = pat.search(text)
    if grp:
        result = result + '   ' + grp[1]

    pat = re.compile('<div class="trans-container">(.*?)</div>',re.S)
    grp = pat.search(text)
    if grp:
        result = result + grp[1]

    return result

def anaText_hj(text):
    result = ''
    pat = re.compile('<div class="pronounces">.*?<span>(.*?)</span>.*?<span>(.*?)</span>.*?<span class="pronounce-value-jp">',re.S)
    grp = pat.search(text)
    if grp:
        result = result + grp[1]

    pat = re.compile('<div class="simple">(.*?)</div>',re.S)
    grp = pat.search(text)
    if grp:
        result = result + grp[1]

    return result

def search_word(word):

    result = []

    title = '英->中：<p></p>'
    url = "http://dict.youdao.com/w/eng/" + word + "/#keyfrom=dict2.index"
    text = getHTMLText(url)
    result.append( title + anaText(text) )

    title = '中->英：<p></p>'
    url = "http://dict.youdao.com/w/" + word + "/#keyfrom=dict2.index"
    text = getHTMLText(url)
    result.append( title + anaText(text) )

    result_hj = ""
    title = '\n 日->中：<p></p>'
    url = "https://dict.hjenglish.com/jp/jc/" + word
    #print(url)
    text = getHTMLText(url)
    result_hj =  title + anaText_hj(text)
    result.append( result_hj )

    title = '中->日：<p></p>'
    url = "https://dict.hjenglish.com/jp/cj/" + word
    #print(url)
    text = getHTMLText(url)
    result_hj =  title +  anaText_hj(text)
    result.append(result_hj)

    result_str = "<hr>".join(result)
    
    with open("myfirst.html", "w", encoding='utf-8') as f:
        f.write(result_str)

    return result_str

    # with open("2.html", "w", encoding='utf-8') as f:
    #     f.write(result_str)

    # with open("3.html", "w", encoding='utf-8') as f:
    #     f.write(text)