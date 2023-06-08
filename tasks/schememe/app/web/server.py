from flask import Flask, render_template, request, send_from_directory
from werkzeug.middleware.proxy_fix import ProxyFix
import lxml.etree as ET
from memelib import create_meme, create_error

def make_app():

    app = Flask(__name__)
    app.wsgi_app = ProxyFix(app.wsgi_app, x_for = 1, x_host = 1)

    @app.route("/<token>/")
    def index(token):
        return render_template("index.html", token=token)
    
    @app.route("/<token>/static/<path:filename>")
    def serve_static(token, filename):
        return send_from_directory('static', filename)
    
    @app.route("/<token>/process", methods=['POST'])
    def process(token):
       
        try:
            xml = request.data
        except Exception as e:
            return create_error(0)
        
        parser = ET.XMLParser(huge_tree=True) # insecure
        try:
            tree = ET.fromstring(xml, parser)
        except Exception as e:
            return create_error(1)
        
        svg_tag = tree[0].tag
        if len(tree.getchildren()) == 3 and (svg_tag[svg_tag.rfind('}')+1:] == "svg" or svg_tag == "svg") and tree[1].tag == "upper" and tree[2].tag == "bottom":
            svg = tree[0]       
            upper = tree[1].text
            bottom = tree[2].text
            new_svg = create_meme(svg, upper, bottom)
        else:
            new_svg = create_error(2)
        
        return new_svg, 200    
    return app
