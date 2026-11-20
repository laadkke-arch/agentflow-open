"""Exact concept matching under the pre-run exclusion rule."""
import unicodedata


def normalize_target(value):
    return " ".join(unicodedata.normalize("NFKC", value).casefold().split())


NEEDS = {
    "서버와 클라이언트 공개 소스": ("server_open_source", "client_open_source"),
    "공개 소스": ("open_source",),
    "오픈소스": ("open_source",),
    "자체 호스팅 가능": ("self_host",),
    "자가 호스팅": ("self_host",),
    "오프라인 한 컴퓨터": ("offline",),
    "로컬 오프라인": ("offline",),
    "오프라인 GUI": ("offline",),
    "무료": ("free",),
    "PostgreSQL 유지": ("postgresql",),
    "OpenAPI 가져오기": ("openapi_import",),
    "요청 그룹 파일·CLI": ("request_group_files", "cli"),
    "구형 .ppt 읽기": ("legacy_ppt",),
    "가능한 EXIF 보존": ("exif_preservation",),
    "Boost 비의존·그래프 조작·공개 소스": ("graph_edit", "open_source"),
    "용어집 재사용": ("reusable_glossary",),
    "VS Code·다중 파일": ("vscode", "multi_file"),
    "SD카드 직접 저장": ("sdcard_write",),
    "PDF 읽기, OCR·생성·편집 불필요": ("pdf_read",),
    ".NET8·상업적 사용·무료": ("dotnet8", "commercial_use", "free"),
    "영어 문장형 C# 테스트": ("csharp_bdd",),
    "30초–1시간 작업": ("runtime_60m",),
    "활발히 유지되는 라이브러리": ("maintained",),
    "활발한 유지보수": ("maintained",),
    "회로에서 라벨 대신 직접 선 연결": ("direct_schematic_wires",),
    "PCB 배선 생성": ("pcb_routing",),
    "컨테이너에서 IMAP 메일 수신": ("imap_receive",),
    "한국어 화자 구분": ("ko_speaker_diarization",),
    "자막 처리": ("subtitle_management",),
    "seedbox 연동": ("seedbox",),
}
BANS = {
    "중개 서버 없는 저장소": ("relay_server",),
    "Boost 비의존·그래프 조작·공개 소스": ("boost",),
    "큰 메모리 AI": ("high_memory_ai",),
    "온라인 방식이면 최종 사용자의 계정 생성 불필요": ("end_user_account",),
    "별도 서버 예산 없음": ("separate_server",),
    "ZooKeeper": ("zookeeper",),
}
POLARITIES = {"positive", "negative"}
RULES = {
    normalize_target(label): (
        frozenset(NEEDS.get(label, ())), frozenset(BANS.get(label, ())),
    )
    for label in NEEDS.keys() | BANS.keys()
}


def query_concepts(must):
    needs, bans = set(), set()
    mapped = 0
    for item in must:
        rule = RULES.get(normalize_target(item["target"]))
        if rule is None:
            continue
        must_have, must_avoid = rule
        # Compound Boost explicitly contains both directions in the fixed map.
        expected = "positive" if must_have else "negative"
        if item["polarity"] != expected:
            continue
        needs.update(must_have)
        bans.update(must_avoid)
        mapped += 1
    return needs, bans, mapped


def conflicts(exclusions, needs, bans):
    return frozenset(row["target"] for row in exclusions
                     if (row["polarity"] == "unsupported" and row["target"] in needs)
                     or (row["polarity"] == "required" and row["target"] in bans))


def postprocess(order, matches, strategy):
    if strategy == "filter":
        return [doc for doc in order if doc not in matches]
    if strategy == "penalty":
        priority = {doc: rank for rank, doc in enumerate(order, 1)}
        return sorted(order, key=lambda doc: (
            priority[doc] + 10 * len(matches.get(doc, ())), priority[doc],
        ))
    return order
