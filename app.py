from flask import Flask, escape, request, render_template
import stanford_parse


app = Flask(__name__)


@app.route('/', methods=["GET", "POST"])
def hello():
    sentence = request.args.get("sentence",
                                "Россия объявила в международный розыск журналиста Александра Шварева из-за публикаций о миллиардере Алишере Усманове.")
    parse = stanford_parse.stanford_print_parse(sentence)
    return render_template('parse.html',
                           sentence=sentence, parse=parse)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port='8090')
