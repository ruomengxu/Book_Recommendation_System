import string
import json
from pprint import pprint


def load_genre_dic():
	dic_list=['criminal_fic.txt','fantasy.txt','horror.txt','inspiration_fic.txt','sci_fic.txt']
	dic=[]
	for dic_file in dic_list:
		with open(dic_file,'r') as dic_data:
			data=dic_data.read().lower()
			dic.append(data.split(", "))
	return dic

def genre_analysis(text,dic):
	text=text.replace('\n', ' ')
	text=text.replace('\'s','')
	text=text.translate(None, string.punctuation).lower()
	text=text.split(" ")
	dic_score=[]
	for i in range(0,5):
		match=set(text).intersection(dic[i])
		dic_score.append(len(match))
	return dic_score

def find_isbn(title,bookdb):
	return [item['isbn'].encode('utf-8') for item in bookdb if item["title"].encode('utf-8') == title]

def book_genre_json(jsonfile,dic):
	file=open(jsonfile).read()
	data=json.loads(file)
	books_genre=[]
	if jsonfile == "BooksWithExtracts.json":
		books_info=data["Extracts"]
		isbn_file=open('isbn_title_author.json').read()
		isbn_data=json.loads(isbn_file)
		isbn_info=isbn_data['books']
		for book_info in books_info:
			Extract=book_info["Extract"].encode('utf-8')
			isbn=find_isbn(book_info["Title"].encode('utf-8'),isbn_info)
			genre_info={"isbn":isbn,"title":book_info["Title"].encode('utf-8'),"genre": genre_analysis(Extract,dic)}
			books_genre.append(genre_info)
	elif jsonfile == "isbn_description.json":
		books_info=data["books"]
		for book_info in books_info:
			description=book_info["description"].encode('utf-8')
			genre_info={"isbn":book_info["isbn"].encode('utf-8'),"genre":genre_analysis(description,dic)}
			books_genre.append(genre_info)
	elif jsonfile == "isbn_avgrating_reviews.json":
		books_info=data["books"]
		for book_info in books_info:
			reviews=book_info["reviews"]
			review_genre=[0,0,0,0,0]
			for review in reviews:
				temp=genre_analysis(review.encode('utf-8'),dic)
				review_genre=[review_genre[j]+temp[j] for j in xrange(5)]
			genre_info={"isbn":book_info["isbn"].encode('utf-8'),"avg_rating":book_info["avg_rating"],"genre":review_genre}
			books_genre.append(genre_info)
	else:
		print("Illegal Parameter")
		exit(1)
	output={"books":books_genre}
	with open(jsonfile[:-5]+'_genre.json','w') as fp:
		json.dump(output,fp)




def main():
	dic=load_genre_dic()
	book_genre_json("BooksWithExtracts.json",dic)
	book_genre_json("isbn_avgrating_reviews.json",dic)
	book_genre_json("isbn_description.json",dic)



if __name__ == '__main__':
    main()






