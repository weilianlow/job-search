from requests import post
import json


class Job:
    def __init__(self, theader, outfile):
        # init
        self.theader = theader
        self.f = open(outfile, "w")
        # write
        self.f.write("<html>\n\t<head>\n\t</head>\n\t<body>\n\t\t<table border='1'>\n\t\t\t<thead>\n\t\t\t\t<tr>")
        self.f.write(''.join([f"\n\t\t\t\t\t<th>{v}</th>" for v in self.theader]))
        self.f.write("\n\t\t\t\t</tr>\n\t\t\t</thead>\n\t\t\t<tbody>")
        self.result = list()

    def append_report(self, result):
        self.result.extend(result)

    def sort(self, **kwargs):
        self.result.sort(**kwargs)

    def close(self):
        tmp = ["\n\t\t\t\t<tr>" + ''.join([f"\n\t\t\t\t\t<td>{v}\n\t\t\t\t\t</td>" for v in r]) + "\n\t\t\t\t</tr>" for
               r in
               self.result]
        self.f.write(''.join(tmp))

        # close html
        self.f.write("\n\t\t\t</tbody>\n\t\t</table>\n\t</body>\n</html>")
        self.f.close()


if __name__ == '__main__':
    def req(keyword, url, data):
        final_lst = list()
        response = post(url=url, data=data)
        for result in response.json()["results"]:
            status = result["status"]["jobStatus"]
            company = result["postedCompany"]["name"].replace(",", ";")
            title = result["title"].replace(",", ";")
            link = result["metadata"]["jobDetailsUrl"]

            lst = [keyword,
                   result["metadata"]["newPostingDate"],
                   str(result["metadata"]["totalNumberJobApplication"]),
                   # "jobDetailsUrl": result["metadata"]["jobDetailsUrl"],
                   f"<a href='{link}' target='_blank'>{title}</a>",
                   status,
                   company,
                   str(result["salary"]["minimum"]),
                   str(result["salary"]["maximum"]),
                   ]
            final_lst.append(lst)
        return final_lst


    j = Job(theader=["search", "newPostingDate", "totalNumberJobApplication", "title", "status", "name", "min-salary",
                     "max-salary"],
            outfile="my_career_future.html")
    for keyword in ["qa engineer", "automation engineer", "test engineer",
                    "qa analyst", "automation analyst", "test analyst",
                    "qa tester", "automation tester", "quality assurance"]:
        j.append_report(
            req(keyword, "https://api.mycareersfuture.gov.sg/v2/search?limit=100&page=0", json.dumps({
                "search": keyword,
                "salary": 11000,
                "postingCompany": ["Direct"],
                "sortBy": [
                    "new_posting_date"
                ]
            }))
        )
    j.sort(key=lambda x: x[5])
    j.close()
