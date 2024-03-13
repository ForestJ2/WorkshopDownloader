from os.path import exists, abspath
from src import workshop, steamcmd
from src.cleanup import run_background
from flask import Flask, render_template, jsonify, abort, send_from_directory


app = Flask(__name__)


@app.route("/")
def index_page():
    """ Return HTML form to user. """
    return render_template("index.html")


@app.route("/info/<int:content_id>")
def workshop_info(content_id: int):
    """ Obtain content information from community workshop. """

    try:
        content = workshop.get_content(content_id)

        return jsonify({
            "game": {
                "id": content.game_id,
                "name": content.game_name
            },
            "content": {
                "id": content.content_id,
                "name": content.content_name
            },
            "error": False
        })
    except Exception as e:
        print(f"[ERROR] exception when handling info request: {e}")
    
    return jsonify({"error": True})


@app.route("/request/<int:game_id>/<int:content_id>")
def download_content(game_id: int, content_id: int):
    """ Have server download workshop content. """

    if exists(f"./archives/{content_id}.zip"):
        return jsonify({"error": False, "url": f"/archive/{content_id}"})

    try:
        if steamcmd.download_workshop(game_id, content_id) is False:
            return jsonify({"error": True, "url": ""})
        
        steamcmd.compress_content(game_id, content_id)
        return jsonify({"error": False, "url": f"/archive/{content_id}"})

    except Exception as e:
        print(f"[ERROR] exception when handling download request: {e}")
    
    return jsonify({"error": True, "url": ""})


@app.route("/archive/<int:content_id>")
def user_download(content_id: int):
    """ Supply content archive to user. """

    if exists(f"./archives/{content_id}.zip") is False:
        abort(404)

    return send_from_directory(abspath("./archives/"),
                               f"{content_id}.zip",
                               as_attachment=True)


def main():
    run_background()
    app.run(debug=False, port=5000)


if __name__ == "__main__":
    main()
