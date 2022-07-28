from selenium import webdriver
from selenium.webdriver.common.by import By
import requests
import io
from PIL import Image
import time

PATH = "C:\\Users\\Aakash Dubey\\Desktop\\india\\chromedriver.exe"
driver = webdriver.Chrome(executable_path=PATH)

wd = webdriver.Chrome(PATH)

def get_images_from_google(wd, delay, max_images):
	def scroll_down(wd):
		wd.execute_script("window.scrollTo(0, document.body.scrollHeight);")
		time.sleep(delay)

	url = "https://www.google.com/search?rlz=1C1ONGR_enIN1009IN1009&source=univ&tbm=isch&q=india+map+with+wrong+kashmir+border&fir=GY2oKULfKDPaSM%252CEuk230NFv7DZwM%252C_%253BO4_LYI1wTyMzvM%252ChVxyW6-mfXMk0M%252C_%253Byhac4hBekKDXCM%252CnH8vs6EMTChf6M%252C_%253BNRZT9FNvb7FbPM%252Cj567DE_PrjPUbM%252C_%253BpYZjDs2A4Q3rBM%252CdbOqpoPFz4OSUM%252C_%253Bji11GTKLmgpStM%252CEqO421PbNFXM9M%252C_%253Bh1Qz12fAMSXjZM%252CgSnrQtSDgzE82M%252C_%253BM0ppPAISHiNHRM%252Cj567DE_PrjPUbM%252C_%253BsB7tQqmShTNw_M%252CYBhVV5S5j9cvIM%252C_%253BtjN24KDByZOogM%252Cb3EZYSnnUbsPTM%252C_&usg=AI4_-kQNmX-900eZHLb_qaxRsn6MXbPmUA&sa=X&ved=2ahUKEwj_xsSGgtD4AhXtxjgGHWTmBUEQjJkEegQIAhAC&biw=1536&bih=722&dpr=1.25"
	wd.get(url)

	image_urls = set()
	skips = 0

	while len(image_urls) + skips < max_images:
		scroll_down(wd)

		thumbnails = wd.find_elements(By.CLASS_NAME, "Q4LuWd")

		for img in thumbnails[len(image_urls) + skips:max_images]:
			try:
				img.click()
				time.sleep(delay)
			except:
				continue

			images = wd.find_elements(By.CLASS_NAME, "n3VNCb")
			for image in images:
				if image.get_attribute('src') in image_urls:
					max_images += 1
					skips += 1
					break

				if image.get_attribute('src') and 'http' in image.get_attribute('src'):
					image_urls.add(image.get_attribute('src'))
					print(f"Found {len(image_urls)}")

	return image_urls


def download_image(download_path, url, file_name):
    
	try:
		image_content = requests.get(url).content
		image_file = io.BytesIO(image_content)
		image = Image.open(image_file)
		file_path = download_path + file_name

		with open(file_path, "wb") as f:
			image.save(f, "JPEG")

		print("Success")
	except Exception as e:
		print('FAILED -', e)

urls = get_images_from_google(wd, 1, 130)

for i, url in enumerate(urls):
	download_image("imgs/", url, str(i) + ".jpg")

wd.quit()