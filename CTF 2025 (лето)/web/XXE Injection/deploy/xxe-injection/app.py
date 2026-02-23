from flask import Flask, request, render_template
import lxml.etree as lET

app = Flask(__name__)

FLAG = "FECTF{xxe_injection_works_here}"

with open("/flag", "w") as f:
    f.write(FLAG)

@app.route('/', methods=['GET', 'POST'])
def index():
    user_name = ""
    error = ""

    if request.method == 'POST':
        xml_data = request.form.get('xml_data', '')
        try:
            parser = lET.XMLParser(resolve_entities=True, load_dtd=True)
            tree = lET.fromstring(xml_data.encode(), parser)

            # Ищем <username> в XML
            username_elem = tree.find('.//username')
            if username_elem is not None and username_elem.text:
                user_name = username_elem.text.strip()
            else:
                user_name = "No username found"
        except Exception as e:
            error = str(e)

    return render_template("index.html", user_name=user_name, error=error)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)