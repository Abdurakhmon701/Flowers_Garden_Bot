import requests
import json

url = 'http://127.0.0.1:8000'

def get_category_id(idi):
	http = f'{url}/category/{idi}/'
	r = requests.get(http)
	data = json.loads(r.text)
	# print(data)
	return data

# print(get_category_id(3))

def get_product_by_category(idi: int):
	http = f'{url}/product/{idi}/'
	r = requests.get(http)
	data = json.loads(r.text)
	return data

# z = get_product_by_category(1)
# print(z)
# for i in z:
# 	print(i)


def category_get_all():
	http = f"{url}/category/"
	req = requests.get(http)
	data = json.loads(req.text)
	return data

# category_get_all()

def get_product_id(idi):
	http = f"{url}/get_product/{idi}"
	req = requests.get(http)
	data = json.loads(req.text)
	return data

# print(get_product_id(3))


def post_card(telegram_id,product_id,product_name,product_price):
	http = f"{url}/card/"
	req = requests.post(http,data={
		"telegram_id":telegram_id,
		"product_id":product_id,
		"product_name":product_name,
		"product_price":product_price
		})
	return 'OK'


# post_card(1,2)

def get_card_all_by_id(idi):
	http = f"{url}/card_all/{idi}"
	req = requests.get(http)
	data = json.loads(req.text)
	return data

# print(get_card_all_by_id(615003781))
	

def delete_for_card(product_id):
	http = f"{url}/card_delete/{product_id}/"
	req = requests.delete(http)
	return req

# print(delete_for_card(2))
