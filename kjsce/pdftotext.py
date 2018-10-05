# import requests

# url = 'http://scholarships.dtemaharashtra.gov.in/InformationPages/UploadFile/Web%20Nofication-2016-17.pdf'
# r = requests.get(url, allow_redirects=True)
# open('dte.pdf', 'wb').write(r.content)

import requests

def download_file_from_google_drive(id, destination):
    URL = "https://drive.google.com/uc?id=1_0IFxyTsKMiyBu_MMDRF782xXjl6AE12&export=download"

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

if __name__ == "__main__":
    file_id = '1_0IFxyTsKMiyBu_MMDRF782xXjl6AE12'
    destination = './temp3.pdf'
    download_file_from_google_drive(file_id, destination)



import convertapi

convertapi.api_secret = 'Gd31ajmvRrWrmKQv'


result = convertapi.convert('txt', { 'File': './temp3.pdf' })
# result = convertapi.convert('txt', { 'File': 'https://drive.google.com/uc?authuser=0&id=1_0IFxyTsKMiyBu_MMDRF782xXjl6AE12&export=download' })


# save to file
result.file.save("./")