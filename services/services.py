@app.route("/services/")
def services():
    template = check_Session('Services')
    return template