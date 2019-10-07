import requests, os
from PIL import Image
from bs4 import BeautifulSoup
from io import BytesIO


def concatenate_images_vertically(*args):
	height = sum([i.height for i in args])
	width = max([i.width for i in args])
	concatenated_image = Image.new('RGB',(width, height), 'white')

	y = 0
	for i in args:
		concatenated_image.paste(i,((width-i.width)//2,y))
		y += i.height

	return concatenated_image


os.makedirs('brown-paperbag', exist_ok=True)
url = 'https://www.webtoons.com/en/challenge/brown-paperbag/ep-1-late-night-shenanigans/viewer?title_no=32251&episode_no=1'

r = requests.get(url)
while 1:
	soup = BeautifulSoup(r.text, 'html.parser')
	image_urls = [i.get('data-url') for i in soup.find_all('img', {'class': '_images'})]
	images = []

	for i in image_urls:
		image = requests.get(i,headers={'Referer':url})
		if image.status_code != requests.codes.ok:
			print('Error while fetching episode. Going to next.')
			break
		images.append(Image.open(BytesIO(image.content)))

	else:	
		name = soup.title.string.replace(' | WEBTOON','')
		print(f'Saving {name}.')
		concatenate_images_vertically(*images).save(f'brown-paperbag/{name}.jpg', quality=95)

	try:
		url = soup.find('a', {'title':'Next Episode'}).get('href')
		r = requests.get(url)	

	except:
		print('\nDone.')
		break