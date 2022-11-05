# Скрипт считывает дату из файла ./date.txt, инкрементирует на 2 дня 
# и перезаписывает исходный файл

from datetime import datetime, timedelta

increment = timedelta(days=2)

def main():
	with open('./date.txt') as f:
		date_str = f.readline()
	date_object = datetime.strptime(date_str, '%Y-%m-%d').date()
	new_date_object = date_object + increment
	new_date_str = new_date_object.strftime("%Y-%m-%d")
	with open('./date.txt', 'w') as f:
		f.write(new_date_str)

if __name__ == '__main__':
	main()