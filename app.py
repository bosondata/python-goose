import importlib

import msgpack
import chardet
from flask import Flask, request, jsonify
from goose import Goose
from goose.text import StopWordsChinese


app = Flask(__name__)

g = Goose({
    'stopwords_class': StopWordsChinese,
    'enable_image_fetching': False,
    'use_meta_language': False,
    'target_language': 'zh'
})


@app.route('/extract', methods=['POST'])
def extract():
    args = msgpack.loads(request.data)
    if 'url' in args:
        url = args['url']
        article = g.extract(url=url)
    else:
        raw_html = args['raw_html']
        if 'compressed' in args:
            algo = importlib.import_module(args['compressed'])
            raw_html = algo.decompress(raw_html)
        if 'encoding' in args:
            encoding = args['encoding']
        else:
            encoding = chardet.detect(raw_html)['encoding']
        article = g.extract(raw_html=raw_html.decode(encoding, errors='ignore'))
    result = {'title': article.title, 'text': article.cleaned_text}
    return jsonify(result=result)


if __name__ == "__main__":
    app.run(debug=True)
