#!python3
# coding: utf-8
import os,sys
from pathlib import Path
from flask import Flask, render_template, Markup, request, jsonify
import ttospeech as speech

app = Flask(__name__)

@app.route('/')
@app.route('/index')
def main():
    return render_template('views/index.html')

@app.route('/convVoice', methods=['POST'])
def convVoice():
    try:
        
        if request.files.get('voicefile',None) is None:
            return app.make_response(jsonify({'result':'uploadFile is required.'}))
        
        file = request.files['voicefile']
        fileName = file.filename
        if '' == fileName:
            return app.make_response(jsonify({'result':'filename must not empty.'}))
        
        config = {}
        config.setdefault('language_code', 'ja-JP')
        config.setdefault('sample_rate_hertz', 44100)
        config.setdefault('max_alternatives', 1)
        
        strs = speech.sample_recognize(file,config=config)
        #return app.make_response(jsonify(strs))
        return jsonify(strs)
    
    except Exception as ex:
        app.logger.error(ex)
        return  app.make_response(jsonify({'result':'error has occured.'}))

if __name__ == '__main__':
    #authJsonFile
    existsAuth = False
    if os.environ.get('GOOGLE_APPLICATION_CREDENTIALS',None) is None:
        if len(sys.argv) >= 2 and os.path.exists(sys.argv[1]):
            authJsonFile = sys.argv[1]
            os.environ.setdefault('GOOGLE_APPLICATION_CREDENTIALS',authJsonFile)
            existsAuth = True
        else:
            app.logger.fatal('No GCP auth json file')
    else:
        existsAuth = True
    
    #run
    if existsAuth is True:
        app.run(host='0.0.0.0', debug=True, port=5005)
