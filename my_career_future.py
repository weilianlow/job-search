from requests import post
import json


class Job:
    def __init__(self, theader, outfile):
        self.theader = theader
        self.f = open(outfile, "w")
        self.f.write("<html>\n\t<head>\n\t</head>\n\t<body>\n\t\t<table border='1'>\n\t\t\t<thead>\n\t\t\t\t<tr>")
        self.f.write(''.join([f"\n\t\t\t\t\t<th>{v}</th>" for v in self.theader]))
        self.f.write("\n\t\t\t\t</tr>\n\t\t\t</thead>\n\t\t\t<tbody>")
        self.results = dict()
        self.results_lst = list()

    def sort(self, **kwargs):
        self.results_lst = list(self.results.values())
        self.results_lst.sort(**kwargs)

    def close(self):
        tmp = ["\n\t\t\t\t<tr>" + ''.join([f"\n\t\t\t\t\t<td>{v}\n\t\t\t\t\t</td>" for v in r]) + "\n\t\t\t\t</tr>" for
               r in
               self.results_lst]
        self.f.write(''.join(tmp))

        # close html
        self.f.write("\n\t\t\t</tbody>\n\t\t</table>\n\t</body>\n</html>")
        self.f.close()


if __name__ == '__main__':
    def req(keyword, final_dct, url, data):
        response = post(url=url, data=data)
        for result in response.json()["results"]:
            status = result["status"]["jobStatus"]
            company = result["postedCompany"]["name"].replace(",", ";")
            title = result["title"].replace(",", ";")
            link = result["metadata"]["jobDetailsUrl"]
            key = f'{company},{title}'
            if key not in final_dct:
                final_dct[key] = [keyword,
                                  result["metadata"]["newPostingDate"],
                                  str(result["metadata"]["totalNumberJobApplication"]),
                                  # "jobDetailsUrl": result["metadata"]["jobDetailsUrl"],
                                  f"<a href='{link}' target='_blank'>{title}</a>",
                                  status,
                                  company,
                                  str(result["salary"]["minimum"]),
                                  str(result["salary"]["maximum"]),
                                  ]
        return final_dct


    j = Job(theader=["search", "newPostingDate", "totalNumberJobApplication", "title", "status", "name", "min-salary",
                     "max-salary"],
            outfile="my_career_future.html")
    a = ["test", "automation", "QA"]
    b = ["engineer", "analyst", "consultant", "specialist", "lead"]
    jobs = ','.join([','.join([second + " " + first for second in a]) for first in b]).split(',')
    jobs.extend(["sdet", "set", "software development engineer in test", "software engineer in test"])
    for keyword in jobs:
        req(keyword,
            j.results,
            "https://api.mycareersfuture.gov.sg/v2/search?limit=100&page=0", json.dumps({
                "search": keyword,
                "salary": 10000,
                "postingCompany": ["Direct"],
                "sortBy": [
                    "new_posting_date"
                ]
            }))
    j.sort(key=lambda x: x[5])
    j.close()
