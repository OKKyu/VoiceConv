#!python3
# -*- coding:utf-8 -*-
import io
import sys, os
import logging
from pathlib import Path
from werkzeug.datastructures import FileStorage

from google.cloud import speech_v1
from google.cloud.speech_v1 import enums

#Please set GOOGLE_APPLICATION_CREDENTIALS environment variables on run.sh
#authJsonFile = ''
#os.environ.setdefault('GOOGLE_APPLICATION_CREDENTIALS',authJsonFile)
logger = logging.getLogger("ttospeech")

def sample_recognize(file, config={}):
    
    if file == None:
        logger.error("please input target image file on first argument.")
        return None
    elif type(file) not in (str, FileStorage):
        logger.error("please input target filename or FileStorage on first argument.")
        return None        
    
    if config is None:
        logger.error("please set config argument")
        return None
    elif type(config) is not dict:
        logger.error("argument config need to dict type.")
        return None
    else:
        if config.get("language_code",None) is None:
            logger.error("please set config.language_code ")
            return None
        if config.get("sample_rate_hertz",None) is None:
            logger.error("please set config.sample_rate_hertz ")
            return None            
        if config.get("max_alternatives",None) is None:
            logger.error("please set config.max_alternatives ")
            return None
        
    client = speech_v1.SpeechClient()
    
    # Encoding of audio data sent. This sample sets this explicitly.
    # This field is optional for FLAC and WAV audio formats.
    encoding = enums.RecognitionConfig.AudioEncoding.LINEAR16
    cfg = {
        "language_code": config.get("language_code",None),
        "sample_rate_hertz": config.get("sample_rate_hertz",None),
        "encoding": encoding,
        "max_alternatives": config.get("max_alternatives",None),
    }
    
    audio = None
    if type(file) is str:
        with io.open(file, "rb") as f:
            content = f.read()
        audio = {"content": content}
    elif type(file) is FileStorage:
        content = file.stream.read()
        audio = {"content": content}
        file.stream.close()
    
    strs = []
    response = client.recognize(cfg, audio)
    for result in response.results:
        # First alternative is the most probable result
        alternative = result.alternatives[0]
        logger.info(u"Transcript: {}".format(alternative.transcript))
        strs.append(alternative.transcript)
        
    return strs
