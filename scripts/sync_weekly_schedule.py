import datetime
import json
import os
import re
import sys
import urllib.request
import urllib.error


def iso_week_string(d: datetime.date) -> str:
    year, week, _ = d.isocalendar()
    return f"{year}-W{week:02d}"


def parse_date(value: str) -> datetime.date | None:
    v = (value or "").strip()
    if not v:
        return None
    for fmt in ("%Y-%m-%d", "%Y/%m/%d", "%Y.%m.%d"):
        try:
            return datetime.datetime.strptime(v, fmt).date()
        except Exception:
            pass
    return None


def get_first(fields: dict, names: list[str]) -> object | None:
    for n in names:
        if n in fields and fields[n] not in (None, ""):
            return fields[n]
    return None


def http_post_json(url: str, payload: dict, token: str) -> dict:
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(url, data=data, method="POST")
    req.add_header("Content-Type", "application/json")
    req.add_header("Accept", "application/json")
    req.add_header("User-Agent", "ai-course-sync-script")
    if token:
        req.add_header("Authorization", f"Bearer {token}")
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            body = resp.read().decode("utf-8")
        return json.loads(body)
    except urllib.error.HTTPError as e:
        err_body = ""
        try:
            err_body = e.read().decode("utf-8")
        except Exception:
            err_body = ""

        hint = ""
        if e.code == 401:
            hint = (
                "\nHint: 401 Unauthorized 通常表示 token 无效/过期/粘贴错误。"
                "\n- 确认仓库 Secrets 里 `PROJECTS_TOKEN` 已设置且没有多余空格/换行"
                "\n- 建议使用 classic PAT，并勾选 `read:project` 权限（fine-grained PAT 有时会踩权限边界）"
            )
        elif e.code == 403:
            hint = (
                "\nHint: 403 Forbidden 通常表示权限不足或被限流。"
                "\n- 确认 token 至少有 `read:project`"
                "\n- 若是 rate limit，请稍后重试或改用 PAT（不要只用 GITHUB_TOKEN）"
            )

        raise RuntimeError(
            f"HTTP Error {e.code}: {e.reason}\nResponse: {err_body}{hint}"
        ) from e


def gh_graphql(query: str, variables: dict, token: str) -> dict:
    res = http_post_json(
        "https://api.github.com/graphql",
        {"query": query, "variables": variables},
        token,
    )
    if "errors" in res and res["errors"]:
        msg = json.dumps(res["errors"], ensure_ascii=False, indent=2)
        raise RuntimeError(f"GitHub GraphQL errors: {msg}")
    return res["data"]


def extract_field_map(item: dict) -> dict:
    field_values = item.get("fieldValues", {}).get("nodes", []) or []
    out: dict[str, object] = {}

    for node in field_values:
        if not node:
            continue

        field = node.get("field") or {}
        field_name = field.get("name")
        if not field_name:
            continue

        typename = node.get("__typename")

        if typename == "ProjectV2ItemFieldTextValue":
            out[field_name] = node.get("text")
        elif typename == "ProjectV2ItemFieldDateValue":
            out[field_name] = node.get("date")
        elif typename == "ProjectV2ItemFieldNumberValue":
            out[field_name] = node.get("number")
        elif typename == "ProjectV2ItemFieldSingleSelectValue":
            out[field_name] = node.get("name")

    return out


def status_icon(status: str | None) -> str:
    if not status:
        return "⬜ 未开始"
    s = status.strip().lower()
    if s in {"todo", "backlog", "to do"}:
        return "⬜ 未开始"
    if s in {"preparing", "in progress", "doing"}:
        return "🟨 备课中"
    if s in {"ready", "review", "blocked"}:
        return "🟦 可上课"
    if s in {"done", "completed"}:
        return "🟩 已完成"
    return status


def safe(s: object) -> str:
    if s is None:
        return ""
    return str(s).strip()


def build_table_rows(items: list[dict], week_value: str) -> list[list[str]]:
    rows: list[tuple[str, float, list[str]]] = []

    for item in items:
        fields = extract_field_map(item)

        # 兼容字段名：英文 + 中文
        week = safe(get_first(fields, ["Week", "周次"]))
        date_raw = safe(get_first(fields, ["Date", "授课时间", "授课日期", "日期"]))
        topic = safe(get_first(fields, ["Topic", "主题"]))
        lesson_no = get_first(fields, ["LessonNo", "课次", "第几次", "序号"]) 
        materials = safe(get_first(fields, ["Materials", "课件/代码", "资料链接", "腾讯会议链接"]))

        # 周次筛选：优先使用 Week 字段；否则用授课日期推算 ISO 周
        if week:
            if week != week_value:
                continue
        else:
            d = parse_date(date_raw)
            if not d:
                continue
            week = iso_week_string(d)
            if week != week_value:
                continue

        date = date_raw
        try:
            lesson_no_num = float(lesson_no) if lesson_no is not None else float("inf")
        except Exception:
            lesson_no_num = float("inf")

        status = safe(get_first(fields, ["Status", "状态"]))

        if not topic:
            content = item.get("content") or {}
            topic = safe(content.get("title"))

        row = [
            week,
            date,
            str(int(lesson_no_num)) if lesson_no is not None and lesson_no_num != float("inf") else safe(lesson_no),
            topic,
            status_icon(status),
            materials if materials else "（待补）",
        ]

        sort_key_date = date if date else "9999-99-99"
        rows.append((sort_key_date, lesson_no_num, row))

    rows.sort(key=lambda x: (x[0], x[1]))
    return [r[2] for r in rows]


def render_markdown_table(rows: list[list[str]]) -> str:
    header = "| 周次 | 日期 | 课次 | 主题 | 备课状态 | 课件/代码 |"
    sep = "| --- | --- | ---: | --- | --- | --- |"
    lines = [header, sep]
    for r in rows:
        week, date, lesson_no, topic, status, materials = r
        lines.append(f"| {week} | {date} | {lesson_no} | {topic} | {status} | {materials} |")
    if len(rows) == 0:
        lines.append("| （本周暂无条目） |  |  |  |  |  |")
    return "\n".join(lines) + "\n"


def replace_block(text: str, start_marker: str, end_marker: str, new_block: str) -> str:
    pattern = re.compile(
        re.escape(start_marker) + r".*?" + re.escape(end_marker),
        flags=re.DOTALL,
    )
    replacement = start_marker + "\n" + new_block + end_marker
    if not pattern.search(text):
        raise RuntimeError("Could not find markers in README. Make sure markers exist.")
    return pattern.sub(replacement, text)


def main() -> int:
    owner = os.getenv("PROJECT_OWNER", "").strip()
    number = os.getenv("PROJECT_NUMBER", "").strip()
    readme_path = os.getenv("README_PATH", "README.md")

    if not owner or not number:
        project_url = os.getenv("COURSE_PROJECT_URL", "").strip()
        if project_url:
            m = re.search(r"github\.com/(?:users|orgs)/([^/]+)/projects/(\d+)", project_url)
            if m:
                owner = owner or m.group(1)
                number = number or m.group(2)

    owner = owner or "HuangShengZeBlueSky"
    number = number or "1"

    try:
        project_number = int(number)
    except Exception:
        print("PROJECT_NUMBER must be int", file=sys.stderr)
        return 2

    token_source = ""
    token = os.getenv("PROJECTS_TOKEN", "").strip()
    if token:
        token_source = "PROJECTS_TOKEN"
    else:
        token = os.getenv("GH_TOKEN", "").strip()
        if token:
            token_source = "GH_TOKEN"
        else:
            token = os.getenv("GITHUB_TOKEN", "").strip()
            if token:
                token_source = "GITHUB_TOKEN"

    if not token:
        print(
            "Missing token. Set repository secret PROJECTS_TOKEN (recommended) or rely on GITHUB_TOKEN.",
            file=sys.stderr,
        )
        return 2

    week_value = os.getenv("WEEK", "").strip() or iso_week_string(datetime.date.today())

    query = """
    query($login: String!, $number: Int!) {
      user(login: $login) {
        projectV2(number: $number) {
          title
          items(first: 100) {
            nodes {
              content {
                __typename
                ... on DraftIssue { title }
                ... on Issue { title url }
                ... on PullRequest { title url }
              }
              fieldValues(first: 50) {
                nodes {
                  __typename
                  ... on ProjectV2ItemFieldTextValue { text field { ... on ProjectV2FieldCommon { name } } }
                  ... on ProjectV2ItemFieldDateValue { date field { ... on ProjectV2FieldCommon { name } } }
                  ... on ProjectV2ItemFieldNumberValue { number field { ... on ProjectV2FieldCommon { name } } }
                  ... on ProjectV2ItemFieldSingleSelectValue { name field { ... on ProjectV2SingleSelectField { name } } }
                }
              }
            }
          }
        }
      }
    }
    """

    print(f"Using token source: {token_source}")
    data = gh_graphql(query, {"login": owner, "number": project_number}, token)
    project = (data.get("user") or {}).get("projectV2")
    if not project:
        raise RuntimeError(
            "Cannot access Project. If this is a user Project, you may need a PAT in secret PROJECTS_TOKEN with read:project."
        )

    items = project.get("items", {}).get("nodes", []) or []
    rows = build_table_rows(items, week_value)
    table_md = render_markdown_table(rows)

    with open(readme_path, "r", encoding="utf-8") as f:
        readme = f.read()

    start_marker = "<!-- WEEKLY_SCHEDULE_START -->"
    end_marker = "<!-- WEEKLY_SCHEDULE_END -->"

    new_block = (
        "> 本表由 GitHub Actions 从 Projects 自动生成；请在看板里维护（字段：Week/Date/LessonNo/Topic/Status/Materials）。\n\n"
        + table_md
    )

    updated = replace_block(readme, start_marker, end_marker, new_block)

    if updated != readme:
        with open(readme_path, "w", encoding="utf-8") as f:
            f.write(updated)
        print(f"Updated {readme_path} for week {week_value}")
    else:
        print("No changes")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
