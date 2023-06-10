import csv
import requests

def download_csv_from_drive(file_url):
    # Function to download the CSV file from Google Drive
    file_id = file_url.split("/")[-2]
    download_url = f"https://drive.google.com/uc?id={file_id}"
    response = requests.get(download_url)
    content = response.content.decode("utf-8")
    return content

def datasetgenerator(givenfile):
    #function to read the translator csv file
    dataset = {}

    content = download_csv_from_drive(givenfile)
    reader = csv.reader(content.splitlines())

    #using this the csv file will be represented as a dictionary with the alphabets as key and morse as values
    for row in reader:
        if len(row) >= 2:
            key = row[1].strip()
            value = row[0].strip()
            dataset[key] = value

    return dataset

def translator(msg, dataset):
    #function to translate the given message.

    #to store each word of the translated message
    text_msg_lst = []

    words = msg.split('/')

    for word in words:
        #to store each letters from a particular word
        text_word_lst = []

        word_lst = word.split()

        for letters in word_lst:
            text_word_lst.append(dataset[letters])

        #joining the translated letters to form a word.
        text_word = ''.join(text_word_lst)

        #adding the word to the translated list
        text_msg_lst.append(text_word)

    #joining the translated words to get the whole msg
    text_msg = ' '.join(text_msg_lst)

    return text_msg

def sendmsg(msg, reciever_num):
    # Fast2SMS API endpoint
    url = "https://www.fast2sms.com/dev/bulkV2"

    # Your Fast2SMS API key
    api_key = "eoxAYV7G5Hpj6XxhEHVfMDs7Xizu1lbCwLRuwyQEphHtCbBvB7XrGWixBvmd"

    payload = {"authorization": api_key,
               "message": msg,
               "language": "english",
               "route": "q",
               "numbers": reciever_num,
               }

    # Prepare the headers
    headers = {
        'cache-control': "no-cache"
    }
    # Send the request
    response = requests.request("GET", url, headers=headers, params=payload)

    # Process the response
    print(response.text)

def main():
    file_url = 'https://drive.google.com/file/d/1IQnjzYly825jIZvszH4Y5E4fsrBhU_4Y/view?usp=drive_link'
    dataset = datasetgenerator(file_url)

    user_msg = input("Enter your message: ")
    reciever_num = input("Enter your phone number: ")

    output = translator(user_msg, dataset)

    print("The translated text is: ", output)

    message = 'The translated text is: ' + output + '\nThanks for visiting the link & using the code.\nRegards Ekarsi.'
    #print(message)
    sendmsg(message, reciever_num)

if __name__ == "__main__":
    main()