from github import Github
from classroom_automation_tokens import GITHUB_TOKEN


uts21_nl = {
    "Антоновский": "Unlinked user",
    "Богатый": "AnatoliiBogatyi",
    "Колосов": "KolosovSergey24",
    "Комалов": "Unlinked user",
    "Кузьмин": "Unlinked user",
    "Молчанов": "Mihail325",
    "Олейник": "vladimir1o",
    "Платонов": "loponavt",
    "Рыбаков": "Nofims",
    "Снегирев": "dimjan131",
    "Тарасов": "tarasqua",
    "Тришкин": "AmthyCorn",
    "Фазлутдинова": "Albinaf",
    "Черопко": "SolarMeIster",
    "Шишкин": "Unlinked user"
}
uts21_ln = {v: k for k, v in uts21_nl.items()}

uts22_nl = {
    "Белик": "BadFatRat",
    "Буй": "Bd0ptimus",
    "Волоченко": "Unlinked user",
    "Гаврилова": "gavrilova-spk",
    "Гугучкин": "CelestialShepherd",
    "Добродеев": "Aleksandr32reg",
    "Ерепилов": "Unlinked user",
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

uts22_ln = {v: k for k, v in uts22_nl.items()}

g = Github(GITHUB_TOKEN)

merged = []

not_merged = []

for repo in g.get_user().get_repos():
    if repo.name.startswith("domashnee-zadanie"):
        if repo.private:
            continue

        commit = repo.get_commits()[0]
        try:
            if commit.get_statuses()[0].state == "success":

                if repo.get_pulls(state="all")[0].is_merged():
                    merged.append(repo)
                else:
                    not_merged.append(repo)
        except:
            pass


report_22 = ""
report_21 = ""

for repo in not_merged:
    login = repo.name.split("-no1-")[-1]
    group = 0
    variant = 0
    try:
        name = uts21_ln[login]
        variant = list(uts21_nl.keys()).index(name) + 1
        group = 21
    except:
        try:
            name = uts22_ln[login]
            variant = list(uts22_nl.keys()).index(name) + 1
            group = 22
        except:
            name = "Unknown"
    
    if group == 21:
        report_21 = report_21 + f"\n {variant} {name} \n" + f"\t https://github.com/MIEE-ACS/{repo.name}"
    elif group == 22:
        report_22 = report_22 + f"\n {variant} {name} \n" + f"\t https://github.com/MIEE-ACS/{repo.name}"

print("УТС-21\n------\n")
print(report_21)

print("УТС-22\n------\n")
print(report_22)


