# -*- coding: utf-8 -*-
import re

def test():
	s='韓子는 싫고, 한글은 nice하다. English 쵝오 -_-ㅋㅑㅋㅑ ./?!'
	hangul = re.compile('[^ ㄱ-ㅣ가-힣]+') # 한글과 띄어쓰기를 제외한 모든 글자
	# hangul = re.compile('[^ \u3131-\u3163\uac00-\ud7a3]+')  # 위와 동일
	result = hangul.sub('', s) # 한글과 띄어쓰기를 제외한 모든 부분을 제거
	print (result)

	result = hangul.findall(s) # 정규식에 일치되는 부분을 리스트 형태로 저장
	print (result)

test()
