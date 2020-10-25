from github import Github
import re
from classroom_automation_tokens import GITHUB_TOKEN
from tqdm import tqdm


class Group(object):
    def __init__(self, name, name_login_dict={}):
        self.name = name
        self.nl = name_login_dict
        self.ln = {v: k for k, v in self.nl.items()}
        self.merged = []
        self.not_merged = []

    def process_repo(self, repo):
        dz, login = re.match(".*-no(\d)-(.*)", repo.name).groups()
        if login not in self.ln.keys():
            return False

        commit = repo.get_commits()[0]
        try:
            if commit.get_statuses()[0].state == "success":
                
                pull = list(filter(lambda x: x.title=="Feedback", repo.get_pulls(state="all")))[0]
            
                if pull.is_merged():
                    self.merged.append(repo)
                else:
                    self.not_merged.append(repo)
        except:
            pass

        return True
    
    def format_repo(self, repo, grades=False):
        
        dz, login = re.match(".*-no(\d)-(.*)", repo.name).groups()
        name = self.ln[login]
        variant = list(self.ln.keys()).index(login) + 1
        if(grades):
            if("loponavt" in repo.name):
                pass
            pull = list(filter(lambda x: x.title=="Feedback", repo.get_pulls(state="all")))[0]
            
            grade = 0
            for comment in pull.get_issue_comments():
                if "Оценка" in comment.body:
                    grade = comment.body.split(" ")[-1]
                    break
            return f"\n {variant} {name} \n" + f"\t https://github.com/MIEE-ACS/{repo.name}/pull/1\n\tОценка: {grade}\n"
        else:
            return f"\n {variant} {name} \n" + f"\t https://github.com/MIEE-ACS/{repo.name}/pull/1"

    def get_dz(repo):
        return re.match(".*-no(\d)-.*", repo.name).groups()[0]


    def get_repos_to_check(self, dz="*"):
        return [self.format_repo(repo) for repo in self.not_merged if dz=="*" or dz==get_dz(repo)]

    def get_graded_repo(self, dz="*"):
        return [self.format_repo(repo, grades=True) 
                for repo in tqdm(self.merged, desc="Fetching grades") 
                    if dz=="*" or dz==get_dz(repo)]


uts21_nl = {
    "Антоновский": "AntonovskiyIvan",
    "Богатый": "AnatoliiBogatyi",
    "Колосов": "KolosovSergey24",
    "Комалов": "Unlinked user",
    "Кузьмин": "WurrenG",
    "Молчанов": "Mihail325",
    "Олейник": "vladimir1o",
    "Платонов": "loponavt",
    "Рыбаков": "Nofims",
    "Снегирев": "dimjan131",
    "Тарасов": "tarasqua",
    "Тришкин": "AmthyCorn",
    "Фазлутдинова": "Albinaf",
    "Черопко": "SolarMeIster",
    "Шишкин": "k4let0"
}

uts22_nl = {
    "Белик": "BadFatRat",
    "Буй": "Bd0ptimus",
    "Волоченко": "Unlinked user",
    "Гаврилова": "gavrilova-spk",
    "Гугучкин": "CelestialShepherd",
    "Добродеев": "Aleksandr32reg",
    "Ерепилов": "Ejik656RUS",
    "Королев": "Akorolev1-d",
    "Лавриненко": "1XDeNX1",
    "Мухаметгалина": "dianamukhametgalina",
    "Припотнев": "MSPripotnev",
    "Рожков": "MrRivan",
    "Рожкова": "JuliaRoUTC22",
    "Федорович": "Furry4",
    "Хо": "htpdanh",
    "Хоанг": "viettung267",
    "Чугаев": "ChugaevMark"
}

ivt_nl = {
    "Амеличев": "Unlinked user",
    "Бадаев": "Unlinked user",
    "Быков": "Unlinked user",
    "Бычков": "Unlinked user",
    "Васякин": "Unlinked user",
    "Гричушкина": "Unlinked user",
    "Зубков": "Unlinked user",
    "Идаев": "Unlinked user",
    "Идаев": "Unlinked user",
    "Когустов": "Unlinked user",
    "Краснюк": "Unlinked user",
    "Оганесян": "Unlinked user",
    "Пирожихин": "Unlinked user",
    "Серебряков": "GeloTorange",
    "Спиридонов": "Unlinked user",
    "Фахриева": "Unlinked user",
}

g = Github(GITHUB_TOKEN)

groups = [
    Group("UTS-21", uts21_nl),
    Group("UTS-22", uts22_nl),
    Group("IVT", ivt_nl),
]

repos = g.get_user().get_repos()
progress = tqdm(repos, total=repos.totalCount, desc="Processing repositories")
i = 0
for repo in progress:

    progress.set_description(f"Processing: {repo.name:>50}")
    if repo.name.startswith("domashnee-zadanie-no3"):
        if repo.private:
            continue      
        for group in groups:
            if group.process_repo(repo):
                break

for group in groups:
    print(f"\n{group.name}")
    print("\n".join(group.get_repos_to_check()))

for group in groups:
    print(f"\n{group.name}")
    print("\n".join(group.get_graded_repo()))
