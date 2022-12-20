# Test qilib ko'rish uchun nima kelayotganini 
import requests 
import json 

url = "http://127.0.0.1:8000"


# Categoriyani idisi boyicha olish
def get_category_id(idi):
  http = f"{url}/category/{idi}"
  req = requests.get(http)
  data = json.loads(req.text)
  return data
 
# print(get_category_id(3))





def get_product_by_category(idi: int):
  http = f"{url}/product/{idi}"
  req = requests.get(http)
  data = json.loads(req.text)
  return data
  
# z = get_product_by_category(2)
# for i in z:
#   print(i)




def category_get_all():
  http = f"{url}/category/"
  req = requests.get(http)
  data = json.loads(req.text)
  # print(data)
  return data
# category_get_all()





def get_product_id(idi):
  http = f"{url}/get_product/{idi}"
  req = requests.get(http)
  data = json.loads(req.text)
  # print(data)
  return data
# print(get_product_id(2))



#Korzinani post qilish 
def post_for_basket(telegram_id,product_id,product_name,product_price,count):
  http = f"{url}/basket/"
  req = requests.post(http,data={
  "telegram_id":telegram_id,
  "product_id":product_id,
  "product_name":product_name,
  "product_price":product_price,
  "count":count
  })
  return "OK"

# post_for_basket(1,1)




def get_basket_all_by_telegram_id(telegram_id):
  http = f"{url}/basket_all/{telegram_id}"
  req = requests.get(http)
  data = json.loads(req.text)
  # print(data)
  return data
# print(get_basket_all_by_telegram_id(615003781))




def delete_for_basket(telegram_id,product_id):
  http = f"{url}/basket_delete/{telegram_id}/{product_id}"
  req = requests.delete(http)
  return req.status_code

# print(delete_for_basket(615003781,2))


def get_for_basket(telegram_id:str,product_id:str):
  http = f"{url}/basket_delete/{telegram_id}/{product_id}"
  req = requests.get(http)  
  if req.status_code == 200:
    return True
  else:
    return False

# print(get_for_basket(615003781,2))


def delete_all_basket_products(telegram_id):
  http = f"{url}/basket_delete_all/{telegram_id}"
  req = requests.delete(http)
  return req.status_code

# print(delete_all_basket_products(615003781))



def count_basket(telegram_id:str,product_id:str,count):
  http = f"{url}/basket_delete/{telegram_id}/{product_id}/"
  req = requests.put(http,data={
  "count":count
  })
  return req.status_code

# print(count_basket('615003781',2))



def post_for_user(telegram_id:int,username:str):
  http = f"{url}/user/"
  req = requests.post(http,data={
  "telegram_id":telegram_id,
  "username":username
  })
  return "Qo'shildi"

# print(post_for_user(615003781,"test1"))

# Userni tekshirish bazada bormi yoqmi, kegin uni UserModelga qo'shish

def user_scaning(telegram_id):
  http = f"{url}/user_id/{telegram_id}"
  req = requests.get(http)
  data = json.loads(req.text)
  # return data
  if req.status_code == 200:
    return True
  else:
    return False
# print(user_scaning(8))


# User zakaz uchun post qilish
def post_for_order(address,contact,payment,idi,product_name,total_price,order_name,telegram_id,username,phone_number):
  http = f"{url}/order/"
  req = requests.post(http,data={
  "address":address,
  "user_phone":contact,
  "payment":payment,
  "order_id":idi,
  "products":product_name,
  "products_price":total_price,
  'user_name':order_name,
  "telegram_id":telegram_id,
  "telegram_username":username,
  "phone_number":phone_number
  })
  return req.status_code
# post_for_order("tashkent","977703550",'click',"2641421130209489967","Fikus","115000000","Abdurahmon","615003781","djuraev721","998997215333")



# post apiga yozish kerak barcha fieldslari uchun

# # Order dan get qilish telegram id bo'yicha
# def get_order_information(telegram_id):
#   http = f"{url}/order_id/{telegram_id}"
#   req = requests.get(http)
#   data = json.loads(req.text)
#   return data
# # print(get_order_information(6551235))