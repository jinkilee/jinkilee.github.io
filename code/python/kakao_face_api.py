import json
json_data=open('tmp.json').read()

# sending data with curl
# curl -v -X POST "https://kapi.kakao.com/v1/vision/face/detect" \
# -d "image_url=https://peopledotcom.files.wordpress.com/2018/12/books-8.jpg" \
# -H "Authorization: KakaoAK 32d78007dbc029c6a1d80b5aa28feb34"

data = json.loads(json_data)

result = data['result']
faces = result['faces']

for f in faces:
	x, y = f['x'], f['y']
	x, y = "{0:.2f}".format(round(x, 2)), "{0:.2f}".format(round(y, 2))
	f = f['facial_attributes']
	gender = f['gender']
	mf = 'male' if gender['male'] > gender['female'] else 'female'
	age = int(f['age'])
	print(mf, age, (x, y))

