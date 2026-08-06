import re
import unicodedata
from typing import Dict, List, Pattern, Tuple

import pandas as pd


JOB_TITLE_RULES: Dict[str, List[str]] = {
    "Business Analyst": [
        r"\bbusiness analyst\b",
        r"\bbusiness analysis\b",
        r"\bphan tich nghiep vu\b",
        r"\bit ba\b",
    ],
    "Data Engineer": [
        r"\bdata engineer\b",
        r"\bbig data engineer\b",
        r"\betl developer\b",
        r"\bdata pipeline\b",
    ],
    "Data Analyst": [
        r"\bdata analyst\b",
        r"\bbusiness intelligence analyst\b",
        r"\bbi analyst\b",
        r"\bphan tich du lieu\b",
    ],
    "Data Scientist / AI": [
        r"\bdata scientist\b",
        r"\bmachine learning\b",
        r"\bml engineer\b",
        r"\bai engineer\b",
        r"\bartificial intelligence\b",
        r"\bcomputer vision\b",
        r"\bnlp engineer\b",
    ],
    "DevOps / Cloud / SRE": [
        r"\bdevops\b",
        r"\bsite reliability engineer\b",
        r"\bsre\b",
        r"\bcloud engineer\b",
        r"\bcloud architect\b",
        r"\bplatform engineer\b",
    ],
    "Cybersecurity": [
        r"\bcyber ?security\b",
        r"\binformation security\b",
        r"\bsecurity engineer\b",
        r"\bsecurity analyst\b",
        r"\bpentest(?:er)?\b",
        r"\bsoc analyst\b",
        r"\ban toan thong tin\b",
    ],
    "Database Administrator": [
        r"\bdatabase administrator\b",
        r"\bdatabase admin\b",
        r"\bdba\b",
        r"\bquan tri co so du lieu\b",
    ],
    "System / Network Engineer": [
        r"\bsystem administrator\b",
        r"\bsystem engineer\b",
        r"\bnetwork administrator\b",
        r"\bnetwork engineer\b",
        r"\bit infrastructure\b",
        r"\bit infra\b",
        r"\bquan tri he thong\b",
        r"\bquan tri mang\b",
    ],
    "IT Support / Helpdesk": [
        r"\bit support\b",
        r"\bapplication support\b",
        r"\btechnical support\b",
        r"\bhelp ?desk\b",
        r"\bdesktop support\b",
        r"\bho tro cong nghe thong tin\b",
        r"\bho tro ky thuat\b",
    ],
    "QA / Tester": [
        r"\bquality assurance\b",
        r"\bqa engineer\b",
        r"\bqa tester\b",
        r"\bqc engineer\b",
        r"\bautomation test(?:er|ing)?\b",
        r"\bmanual test(?:er|ing)?\b",
        r"\bsoftware test(?:er|ing)?\b",
        r"\btester\b",
        r"\bkiem thu\b",
    ],
    "Project Manager": [
        r"\bproject manager\b",
        r"\bproject management\b",
        r"\bproject coordinator\b",
        r"\bquan ly du an\b",
    ],
    "Product Manager / Owner": [
        r"\bproduct manager\b",
        r"\bproduct owner\b",
        r"\bproduct management\b",
    ],
    "UI / UX Designer": [
        r"\bui\s*/?\s*ux\b",
        r"\bux\s*/?\s*ui\b",
        r"\bui designer\b",
        r"\bux designer\b",
        r"\bweb designer\b",
        r"\bgraphic designer\b",
        r"\bthiet ke giao dien\b",
    ],
    "ERP / SAP": [
        r"\bsap\b",
        r"\berp\b",
        r"\boracle ebs\b",
        r"\bdynamics 365\b",
    ],
    "Embedded / IoT Engineer": [
        r"\bembedded\b",
        r"\bfirmware\b",
        r"\biot\b",
        r"\bhardware engineer\b",
    ],
    "Game Developer": [
        r"\bgame developer\b",
        r"\bunity developer\b",
        r"\bunreal developer\b",
        r"\bgame programmer\b",
        r"\blap trinh game\b",
    ],
    "Mobile Developer": [
        r"\bmobile developer\b",
        r"\bmobile engineer\b",
        r"\bandroid developer\b",
        r"\bandroid engineer\b",
        r"\bios developer\b",
        r"\bios engineer\b",
        r"\bflutter\b",
        r"\breact native\b",
        r"\blap trinh mobile\b",
        r"\blap trinh android\b",
        r"\blap trinh ios\b",
    ],
    "Full-stack Developer": [
        r"\bfull[ -]?stack\b",
        r"\bfullstack\b",
    ],
    "Frontend Developer": [
    r"\bfront[ -]?end\b",
    r"\bfrontend\b",
    r"\breact(?:js|\.js)?\b",
    r"\bangular(?:js)?\b",
    r"\bvue(?:js|\.js)?\b",
    r"\bweb frontend\b",
    ],
    "Backend Developer": [
        r"\bback[ -]?end\b",
        r"\bbackend\b",
        r"\bjava developer\b",
        r"\b\.net developer\b",
        r"\bdotnet developer\b",
        r"\bphp developer\b",
        r"\bpython developer\b",
        r"\bnode(?:js|\.js)? developer\b",
        r"\bgolang developer\b",
        r"\bruby developer\b",
        r"\bserver side developer\b",
    ],
    "Software Developer": [
        r"\bsoftware engineer\b",
        r"\bsoftware developer\b",
        r"\bapplication developer\b",
        r"\bweb developer\b",
        r"\bdeveloper\b",
        r"\bprogrammer\b",
        r"\blap trinh vien\b",
        r"\blap trinh phan mem\b",
        r"\bky su phan mem\b",
    ],
}


COMPILED_RULES: List[Tuple[str, List[Pattern[str]]]] = [
    (
        category,
        [re.compile(pattern, flags=re.IGNORECASE) for pattern in patterns],
    )
    for category, patterns in JOB_TITLE_RULES.items()
]


NOISE_PATTERNS: List[Pattern[str]] = [
    re.compile(r"\b(?:senior|junior|fresher|intern(?:ship)?)\b"),
    re.compile(r"\b(?:thuc tap sinh|thuc tap|nhan vien|chuyen vien|cong tac vien)\b"),
    re.compile(r"\b(?:urgent|hot job|attractive salary|apply now)\b"),
    re.compile(r"\b(?:salary|luong|thu nhap)\b.*$"),
    re.compile(r"\bup\s*to\b.*$"),
    re.compile(r"\btu\s+\d+(?:[.,]\d+)?\s*(?:nam|thang)\b.*$"),
    re.compile(r"\b\d+(?:[.,]\d+)?\s*(?:nam|year|years)\s*(?:kinh nghiem|experience)?\b"),
    re.compile(r"\b(?:kinh nghiem|experience)\b"),
    re.compile(r"\$\s*\d[\d.,]*"),
    re.compile(r"\b\d+[\d.,]*\s*(?:usd|trieu|million|m)\b"),
]


def remove_accents(text: str) -> str:
    normalized = unicodedata.normalize("NFD", text)

    return "".join(
        character
        for character in normalized
        if unicodedata.category(character) != "Mn"
    ).replace("đ", "d").replace("Đ", "D")


def clean_job_title(job_title: str) -> str:
    if pd.isna(job_title) or not str(job_title).strip():
        return ""

    title = unicodedata.normalize("NFKC", str(job_title))
    title = remove_accents(title).lower().strip()

    title = title.replace("&", " and ")
    title = re.sub(r"[_|]+", " ", title)
    title = re.sub(r"[\[\]{}()]", " ", title)
    title = re.sub(r"\s*[-–—]+\s*", " ", title)

    for pattern in NOISE_PATTERNS:
        title = pattern.sub(" ", title)

    title = re.sub(r"[^a-z0-9+#./\s-]", " ", title)
    title = re.sub(r"\s+", " ", title)

    return title.strip(" -/.")


def classify_job_title(job_title: str) -> str:
    cleaned_title = clean_job_title(job_title)

    if not cleaned_title:
        return "Unknown"

    if re.search(r"\bbusiness development\b", cleaned_title):
        return "Other"

    for category, patterns in COMPILED_RULES:
        if any(pattern.search(cleaned_title) for pattern in patterns):
            return category

    return "Other"


def job_title_normalize(df: pd.DataFrame) -> pd.DataFrame:
    if "job_title" not in df.columns:
        raise KeyError("Missing required column: 'job_title'")

    df_clean = df.copy()

    df_clean["clean_job_title"] = df_clean["job_title"].apply(clean_job_title)
    df_clean["normalized_job_title"] = df_clean["job_title"].apply(classify_job_title)

    return df_clean