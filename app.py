from flask import Flask, jsonify, request
from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup

app = Flask(__name__)

baseUrl = 'http://nepalstock.com.np'

@app.route('/')
def index():
        return """
                Welcome to NEPSE API by Ashutosh Sharma
                <br>Visit <a href="/live">/live</a> for Live Data
                <br>Visit <a href="/floorsheet">/floorsheet</a> for Floorsheet
                <br>Visit <a href="/floorsheet?symbol=ADBL">/floorsheet/?contract=&symbol=&buyer=&seller=</a> for company's Floorsheet
                <br>Visit <a href="/brokers">/brokers</a> for brokers' information
                <br>Visit <a href="/indices">/indices</a> for Index and Sub Index
                <br>Visit <a href="/gainers">/gainers</a> for Top Gainers
                <br>Visit <a href="/losers">/losers</a> for Losers
                """

@app.route('/live/')
def live_market():
        url_link = baseUrl + '/main/todays_price/?_limit=300'
        uClient = uReq(url_link)
        page_html = uClient.read()
        uClient.close()
        page_soup = soup(page_html, "html.parser")
        table = page_soup.findAll('table')[0]
        rows = table.findAll('tr')
        rows.pop(0)
        rows.pop(0)
        rows.pop()
        rows.pop()
        rows.pop()
        rows.pop()
        json = []
        for row in rows:
                data = row.findChildren()
                json.append({
                "Company Name": data[1].text,
                "No. of Transaction": data[2].text,
                "Max Price": data[3].text,
                "Min Price": data[4].text,
                "Closing Price": data[5].text,
                "Traded Shares": data[6].text,
                "Amount": data[7].text,
                "Previous Closing": data[8].text,
                "Difference Rs": data[9].text.strip()
                })
        return jsonify(json)

@app.route('/floorsheet/')
def floorsheet():
        contract = request.args.get('contract', default="")
        symbol = request.args.get('symbol', default="")
        buyer = request.args.get('buyer', default="")
        seller = request.args.get('seller', default="")
        url_link = baseUrl + '/main/floorsheet/?contract-no='+contract+'&stock-symbol='+symbol+'&buyer='+buyer+'&seller='+seller+'&_limit=500'
        uClient = uReq(url_link)
        page_html = uClient.read()
        uClient.close()
        page_soup = soup(page_html, "html.parser")
        table = page_soup.findAll('table')[0]
        rows = table.findAll('tr')
        rows.pop(0)
        rows.pop(0)
        if(rows[0].td.text == "No Data Available!"):
                return jsonify({"error": "No Data Available!"})
        rows.pop()
        rows.pop()
        rows.pop()
        json = []
        for row in rows:
                data = row.findChildren()
                json.append({
                "Contract No": data[1].text,
                "Stock Symbol": data[2].text,
                "Buyer Broker": data[3].text,
                "Seller Broker": data[4].text,
                "Quantity": data[5].text,
                "Rate": data[6].text,
                "Amount": data[7].text
                })
        return jsonify(json)

@app.route('/brokers/')
def brokers():
        url_link = baseUrl + '/brokers/?_limit=500'
        uClient = uReq(url_link)
        page_html = uClient.read()
        uClient.close()
        page_soup = soup(page_html, "html.parser")
        rows = page_soup.findAll("div", {"class": "content"})
        json = []
        for row in rows:
                data = row.findAll("div", {"class": "row-content"})
                json.append({
                "Broker Name": row.h4.text,
                "Address": data[0].text.strip(),
                "Code": data[1].text.strip(),
                "Phone": data[2].text.strip()
                })
        return jsonify(json)

@app.route('/indices/')
def indices():
        url_link = baseUrl + ''
        uClient = uReq(url_link)
        page_html = uClient.read()
        uClient.close()
        page_soup = soup(page_html, "html.parser")
        stats = page_soup.find("div", {"id": "nepse-stats"})
        panel = stats.findAll("div", {"class": "panel"})
        panel_body = panel[1].find("div", {"class": "panel-body"})
        tables = panel_body.findAll("table")
        indices = tables[0].tbody.findAll("tr")
        indices.pop()
        subindices = tables[1].tbody.findAll("tr")
        subindices.pop()
        indexList = []
        for index in indices:
                row = index.findAll("td")
                indexList.append({
                        "Index": row[0].text.strip(),
                        "Current": row[1].text.strip(),
                        "Points Change": row[2].text.strip(),
                        "% Change": row[3].text.strip()
                })
        subindexList = []
        for subindex in subindices:
                row = subindex.findAll("td")
                subindexList.append({
                        "Sub-Indices": row[0].text.strip(),
                        "Current": row[1].text.strip(),
                        "Points Change": row[2].text.strip(),
                        "% Change": row[3].text.strip()
                })
        return jsonify({"indices": indexList, "sub-indices": subindexList})

@app.route('/gainers/')
def gainers():
        url_link = baseUrl + '/gainers'
        uClient = uReq(url_link)
        page_html = uClient.read()
        uClient.close()
        page_soup = soup(page_html, "html.parser")
        table = page_soup.find("table")
        rows = table.findAll("tr")
        rows.pop(0)
        rows.pop(0)
        rows.pop()
        json = []
        for row in rows:
                data = row.findAll("td")
                json.append({
                        "Symbol": data[0].text,
                        "LTP": data[1].text,
                        "% Change": data[2].text
                        })
        return jsonify(json)

@app.route('/losers/')
def losers():
        url_link = baseUrl + '/losers'
        uClient = uReq(url_link)
        page_html = uClient.read()
        uClient.close()
        page_soup = soup(page_html, "html.parser")
        table = page_soup.find("table")
        rows = table.findAll("tr")
        rows.pop(0)
        rows.pop(0)
        rows.pop()
        json = []
        for row in rows:
                data = row.findAll("td")
                json.append({
                        "Symbol": data[0].text,
                        "LTP": data[1].text,
                        "% Change": data[2].text
                        })
        return jsonify(json)

if __name__ == '__main__':
   app.run(debug = True)
