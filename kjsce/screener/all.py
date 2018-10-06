import convertapi
import pandas as pd
from github import Github, GithubException
from decouple import config
import base64
from selenium import webdriver
from bs4 import BeautifulSoup
from urllib.request import urlopen
import time
import requests
import nltk
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
import textrazor
from dandelion import DataTXT
import math
from .models import Applicant

def preprocessing(text):
   # text = text.decode("utf8")
   # tokenize into words
   text1 = text.replace('\n', ' ')
   tokens = [word for sent in nltk.sent_tokenize(text1) for word in nltk.word_tokenize(sent)]

   # remove stopwords
   stop = stopwords.words('english')
   tokens = [token for token in tokens if token not in stop]

   # remove words less than three letters
   tokens = [word for word in tokens if len(word) >= 3]

   # lower capitalization
   tokens = [word.lower() for word in tokens]

   # lemmatize
   lmtzr = WordNetLemmatizer()
   tokens = [lmtzr.lemmatize(word) for word in tokens]
   preprocessed_text= ' '.join(tokens)

   return preprocessed_text


def download_file_from_google_drive(id, destination):
    URL = "https://drive.google.com/uc?id="+id+"&export=download"
    session = requests.Session()

    response = session.get(URL, params = { 'id' : id }, stream = True)
    token = get_confirm_token(response)

    if token:
        params = { 'id' : id, 'confirm' : token }
        response = session.get(URL, params = params, stream = True)

    save_response_content(response, destination)

def get_confirm_token(response):
    for key, value in response.cookies.items():
        if key.startswith('download_warning'):
            return value

    return None

def save_response_content(response, destination):
    CHUNK_SIZE = 32768

    with open(destination, "wb") as f:
        for chunk in response.iter_content(CHUNK_SIZE):
            if chunk: # filter out keep-alive new chunks
                f.write(chunk)


def get_user_info_git(user_link):
    num_of_repos = 0
    repos = []
    followers = 0
    sample = """"""
    try:
        username = user_link.strip('/').split("/")[-1]
        user = g.get_user(username)
        for r in user.get_repos().sort(key=forks_count, reverse=True):
            temp = []
            temp.append(r.name)
            sample += r.name + ' '
            sample += str(r.language) + ' '
            temp.append(r.language)
            try:
                # temp.append(base64.b64decode(r.get_readme().content))
                sample += str(base64.b64decode(r.get_readme().content)) + ' '
            except GithubException:
                sample.append('')
            try:
                sample += "".join(r.get_topics()) + ' '
            except GithubException:
                sample += ''
            repos.append(temp)
            num_of_repos += 1
        followers = user.followers
    except GithubException:
        print("No user found")
        return None
    # print(type(sample))
    # return sample
    return [preprocessing(sample), repos]


def get_user_info_quora(user_link):
	print(user_link)
	print(type(user_link))
	if(math.isnan(user_link)):
		return ""
	else:
	    driver = webdriver.PhantomJS(service_args=['--ignore-ssl-errors=true', '--ssl-protocol=any'])
	    driver.get(user_link)
	    lenOfPage = driver.execute_script("window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
	    match=False
	    while(match==False):
	    	lastCount = lenOfPage
	    	time.sleep(0.5)
	    	lenOfPage = driver.execute_script("window.scrollTo(0, document.body.scrollHeight); var lenOfPage=document.body.scrollHeight;  return lenOfPage;")
	    	if lastCount==lenOfPage:
	    		match=True

	    html = driver.page_source

	    soup = BeautifulSoup(driver.page_source, "lxml")

	    ques_text= soup.find_all('span', {'class': 'TopicNameSpan'})
	    words = []
	    for i in range(0,len(ques_text)):
	        words.append(ques_text[i].get_text())

	    return ', '.join(words)


def final_score(event, keywords):

	textrazor.api_key = "9dcd16199684c470157ce02dc8ced9357b28f61dd685df6acc8dfd62"
	infocsv = pd.read_csv(event.csv_file.path, header=None)
	print("INFOOOO")
	print(infocsv.shape)
	print(infocsv.iloc[2,2])
	dandelionclient = DataTXT(app_id = '9355e03c7d5e4b879e6af9d8575159d2', app_key = '9355e03c7d5e4b879e6af9d8575159d2')
	# keywords = "reactjs, react.js, redux, React.js"

	a=[]
	output_data = []

	for count in range(infocsv.shape[0]):
		applicant = Applicant()
		applicant.name = str(infocsv.iloc[count, 0])
		applicant.college = str(infocsv.iloc[count, 1])
		applicant.email = str(infocsv.iloc[count, 2])
		applicant.github_url = str(infocsv.iloc[count,3])
		if(applicant.github_url == "nan"):
			applicant.delete()
			break
		applicant.quora_url = infocsv.iloc[count,4]
		applicant.resume_link = str(infocsv.iloc[count,5])
		applicant.number = infocsv.iloc[count, 6]
		applicant.event = obj
		applicant.save()
		print("CVLINK")
		print(cvlink)

		print("RESUME INFO")
		if __name__ == "__main__":
		    words = cvlink.split('/')
		    file_id = words[len(words)-2]
		    destination = './templates/screener/resumes/' + applicant.email + '.pdf'
		    download_file_from_google_drive(file_id, destination)

		convertapi.api_secret = 'Gd31ajmvRrWrmKQv'
		result = convertapi.convert('txt', { 'File': './templates/screener/resumes/' + applicant.email + '.pdf' })
		result.file.save('./templates/screener/resumes/' + applicant.email + '.txt')

		f1 = open('./templates/resumes/' + applicant.email + '.txt', "r", encoding="utf8")
		resumeinfo = f1.read()
		print(resumeinfo)
		print("="*100)
		try:
			client = textrazor.TextRazor(extractors=["entities", "topics"])
			response = client.analyze(resumeinfo)
			related_keyword_resume=[]
			for topic in response.topics():
				if topic.score>0.7:
					related_keyword_resume.append(topic.label)
			rel_key_resume=', '.join(related_keyword_resume)
			print(rel_key_resume)
			r = dandelionclient.sim(rel_key_resume, keywords, lang="en", bow="one_empty")
			resumesimilarity = r.similarity*25
		except:
			resumesimilarity = 0
		print("--"*100)

		print("QUORA INFO")
		quorainfo, extra_data = get_user_info_quora(applicant.quora_url)
		print(quorainfo)
		print("="*100)
		if(quorainfo is not ""):
			try:
				client = textrazor.TextRazor(extractors=["topics"])
				response = client.analyze(quorainfo)
				related_keyword_qra=[]
				for topic in response.topics():
					if topic.score>0.7:
						related_keyword_qra.append(topic.label)
				rel_key_quora=', '.join(related_keyword_qra)
				print(rel_key_quora)
				r = dandelionclient.sim(rel_key_quora, keywords, lang="en", bow="one_empty")
				quorasimilarity = r.similarity*15
			except Exception as e:
				print(e)
				quorasimilarity = 0
		else:
			quorasimilarity = 0
		print("--"*100)

		print("GITHUB INFO")
		g = Github(config('GITHUB_USER'), config('GITHUB_PASS'))
		gitinfo = get_user_info_git(applicant.github_url)
		print(gitinfo)
		print("=="*100)
		try:
			client = textrazor.TextRazor(extractors=["topics"])
			response = client.analyze(gitinfo)
			related_keyword_git=[]
			for topic in response.topics():
				if topic.score>0.7:
					related_keyword_git.append(topic.label)
			rel_key_git=', '.join(related_keyword_git)
			print(rel_key_git)
			print("--"*100)
			r = dandelionclient.sim(rel_key_git, keywords, lang="en", bow="one_empty")
			gitsimilarity = r.similarity*60
		except:
			gitsimilarity = 0
		print("+"*100)
		print(quorasimilarity, resumesimilarity, gitsimilarity)
		a.append(quorasimilarity+resumesimilarity+gitsimilarity)
		applicant.score = a[-1]
		applicant.save()
		output.append(applicant)

	output.sort(key=lambda x: x.score, reverse=True)
	print(a)
	return output
