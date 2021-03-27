# # import toAudio
# import speech_recognition as sr
#
# var = "a"
# r = sr.Recognizer()
# with sr.WavFile("/Users/blakeankner/Desktop/myAudio.wav") as source:
#     audio = r.record(source)
# try:
#     list = r.recognize_google(audio,key=None)
#     if var in list:
#         print("word found")
#
# except LookupError:
#     print("Could not understand audio")





from __future__ import print_function
from google.oauth2 import service_account
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

import googleapiclient.discovery
import os
import os.path
import summary


from google.cloud import storage

desktopPath = os.path.expanduser("~/Desktop")

def upload_to_bucket(blob_name, path_to_file, bucket_name):
    """ Upload data to a bucket"""
    print("Uploading")

    # Explicitly use service account credentials by specifying the private key
    # file.
    storage_client = storage.Client.from_service_account_json(
        'sttproject-1616427184591-c72881fa04a7.json')

    #print(buckets = list(storage_client.list_buckets())

    bucket = storage_client.get_bucket(bucket_name)
    blob = bucket.blob(blob_name)
    blob.upload_from_filename(path_to_file)

    print("finished uploading")
    #returns a public url
    return blob.public_url

# upload_to_bucket("myAudio", f"{desktopPath}/myAudio.flac", "sttproject")

def implicit():
    from google.cloud import storage

    # If you don't specify credentials when constructing the client, the
    # client library will look for credentials in the environment.
    storage_client = storage.Client()

    # Make an authenticated API request
    buckets = list(storage_client.list_buckets())
    print(buckets)
# implicit()

def transcribe_gcs_with_word_time_offsets(gcs_uri, words):
    """Transcribe the given audio file asynchronously and output the word time
    offsets."""
    from google.cloud import speech
    process_words = words.lower()
    process_words = process_words.split(",")
    requested_words = []
    print("processing words")
    for word in process_words:
        requested_words.append(word.strip())
    matches = []

    client = speech.SpeechClient()

    audio = speech.RecognitionAudio(uri=gcs_uri)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.FLAC,
        language_code="en-US",
        enable_word_time_offsets=True,
        enable_automatic_punctuation=False,
    )

    operation = client.long_running_recognize(config=config, audio=audio)

    print("Waiting for operation to complete...")
    result = operation.result(timeout=90)

    for result in result.results:
        alternative = result.alternatives[0]
        # print("Transcript: {}".format(alternative.transcript))
        # print("Confidence: {}".format(alternative.confidence))

        for word_info in alternative.words:
            word = (str(word_info.word)).lower()
            start_time = word_info.start_time
            end_time = word_info.end_time
            for option in requested_words:
                if word == option:
                    # print(word + " Matched with " + option)
                    matches.append(word)
                    matches.append(start_time.total_seconds())

        # print(
        #     f"Word: {word}, start_time: {start_time.total_seconds()}, end_time: {end_time.total_seconds()}"
        # )
    # print(summary.summarize(fullTranspcript))

    return matches

def get_transcript(gcs_uri):
    from google.cloud import speech

    client = speech.SpeechClient()

    audio = speech.RecognitionAudio(uri=gcs_uri)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.FLAC,
        language_code="en-US",
        enable_word_time_offsets=True,
        enable_automatic_punctuation=True,
    )

    operation = client.long_running_recognize(config=config, audio=audio)

    print("Waiting for operation to complete...")
    result = operation.result(timeout=90)

    fullTranspcript = ""

    for result in result.results:
        alternative = result.alternatives[0]
        fullTranspcript = fullTranspcript + alternative.transcript
        # print("Transcript: {}".format(alternative.transcript))
        # print("Confidence: {}".format(alternative.confidence))

        # print(
        #     f"Word: {word}, start_time: {start_time.total_seconds()}, end_time: {end_time.total_seconds()}"
        # )
    # print(summary.summarize(fullTranspcript))

    return fullTranspcript


# print(transcribe_gcs_with_word_time_offsets("gs://sttproject/myAudio", "coconut, pineapple"))
# transcribe_gcs_with_word_time_offsets("gs://sttproject/myAudio", "how")
