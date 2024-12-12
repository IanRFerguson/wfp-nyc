from flask import Flask, render_template

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/wfp_nyc")
def wfp_nyc():
    return render_template("wfp_nyc.html")


# For local development
if __name__ == "__main__":
    app.run(debug=True)
