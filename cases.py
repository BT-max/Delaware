import csv

import requests
from bs4 import BeautifulSoup


def get_pages(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    page_numbers = [1]
    li = next((li for li in soup.find_all('li', {'class': 'active'}) if li.find('a', string='1')), None)
    if not li:
        return page_numbers
    page_numbers.extend([
        int(page_number.find('a').text)
        for page_number in li.find_next_siblings()
        if page_number.find('a') and page_number.find('a').text
    ])
    return page_numbers


def crawl_response(response, headers):
    soup = BeautifulSoup(response.content, "html.parser")
    table = soup.find("table", {"class": "table table-bordered table-striped"})
    data = []
    for row in table.find_all("tr")[1:]:
        row_data = []
        link = ""
        for cell in row.find_all("td"):
            row_data.append(cell.text.strip())
            if cell.find("a"):
                link = "".join(["https://courts.delaware.gov", cell.find("a").get("href")])
        row_data.append(link)
        row_dict = dict(zip(headers, row_data))
        data.append(row_dict)
    return data


def write_to_csv(cases, field_names):
    with open("cases.csv", "w", newline="") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=field_names)
        writer.writeheader()
        writer.writerows(cases)


def main(url):
    page_numbers = get_pages(url)
    data = []
    headers = ["Parties/Caption", "Date", "File Number", "Court", "Type", "Judicial Officer", "Description", "Link"]
    request_headers = {
        "ctlOpinions1selagencies": "Court+of+Chancery",
        "ctlOpinions1selperiods": "2023",
        "ctlOpinions1txtsearchtext": "",
        "ctlOpinions1selresults": "25",
        "ctlOpinions1hdnagency": "Court+of+Chancery",
        "ctlOpinions1hdncasetype": "",
        "ctlOpinions1hdndivision": "",
        "ctlOpinions1hdnsortby": "",
        "ctlOpinions1hdnsortorder": "0",
        "ctlOpinions1hdnsortbynew": "",
        "ctlOpinions1hdnpageno": "",
    }
    for page_number in page_numbers:
        request_headers["ctlOpinions1hdnpageno"] = str(page_number)
        response = requests.get(url, json=request_headers)
        data.extend(crawl_response(response, headers))
    write_to_csv(data, headers)


if __name__ == '__main__':
    main("https://courts.delaware.gov/opinions/list.aspx?ag=court+of+chancery")
