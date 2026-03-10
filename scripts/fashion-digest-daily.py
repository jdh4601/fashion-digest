#!/usr/bin/env python3
"""
Fashion Digest Daily Automation
================================
매일 09:00 KST에 macOS launchd에 의해 실행됨.

실행 흐름:
  1. Claude CLI로 fashion-digest 스킬 실행 (패션 기사 찾아줘)
  2. 생성된 이메일 HTML 파일 탐색
  3. Gmail SMTP로 자신의 계정에 발송

설정:
  scripts/.env 파일에 GMAIL_USER, GMAIL_APP_PASSWORD 필요
  Gmail 앱 비밀번호: Google 계정 → 보안 → 앱 비밀번호 (2단계 인증 필요)
"""

import glob
import logging
import os
import smtplib
import subprocess
import sys
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pathlib import Path

# 경로 설정
SCRIPT_DIR = Path(__file__).parent
PROJECT_DIR = SCRIPT_DIR.parent
FASHION_RESEARCH_DIR = PROJECT_DIR
LOG_FILE = PROJECT_DIR / "logs" / "fashion-digest.log"
ENV_FILE = SCRIPT_DIR / ".env"


def load_env() -> None:
    """scripts/.env 파일에서 환경 변수를 로드한다."""
    if not ENV_FILE.exists():
        raise FileNotFoundError(
            f".env 파일 없음: {ENV_FILE}\nscripts/.env.example을 참고하여 생성하세요."
        )
    with open(ENV_FILE) as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                key, _, value = line.partition("=")
                os.environ.setdefault(key.strip(), value.strip())


def run_claude_skill() -> bool:
    """claude CLI로 fashion-digest 스킬을 실행한다.

    Returns:
        True if 성공 (returncode == 0), False otherwise.
    """
    logging.info("Claude 스킬 실행 시작: 패션 기사 찾아줘")
    try:
        result = subprocess.run(
            ["claude", "-p", "패션 기사 찾아줘", "--dangerously-skip-permissions"],
            capture_output=True,
            text=True,
            cwd=str(PROJECT_DIR),
            timeout=600,  # 10분 타임아웃
        )
        if result.returncode != 0:
            logging.error(
                "Claude 종료 코드 %d\nstderr: %s",
                result.returncode,
                result.stderr[:500],
            )
            return False
        logging.info("Claude 스킬 완료")
        return True
    except subprocess.TimeoutExpired:
        logging.error("Claude 스킬 실행 타임아웃 (10분 초과)")
        return False
    except FileNotFoundError:
        logging.error("claude CLI를 찾을 수 없음. PATH 확인 필요.")
        return False


def get_today_email_html() -> str | None:
    """오늘 날짜의 이메일 HTML 파일 경로를 반환한다.

    Returns:
        파일 경로 문자열, 없으면 None.
    """
    today = datetime.now().strftime("%Y-%m-%d")
    pattern = str(
        FASHION_RESEARCH_DIR / "output_email" / f"{today}-fashion-digest-email.html"
    )
    files = glob.glob(pattern)
    if files:
        logging.info("이메일 HTML 발견: %s", files[0])
        return files[0]
    logging.error("이메일 HTML 없음: %s", pattern)
    return None


def send_email(html_content: str, gmail_user: str, app_password: str) -> None:
    """Gmail SMTP TLS로 이메일을 발송한다.

    Args:
        html_content: 발송할 HTML 본문.
        gmail_user: 발신/수신 Gmail 주소.
        app_password: Gmail 앱 비밀번호 (16자리).

    Raises:
        smtplib.SMTPException: 발송 실패 시.
    """
    today_ko = datetime.now().strftime("%Y년 %m월 %d일")
    today_en = datetime.now().strftime("%B %d, %Y")

    msg = MIMEMultipart("alternative")
    msg["Subject"] = f"👗 Fashion Digest — {today_ko} ({today_en})"
    msg["From"] = gmail_user
    msg["To"] = gmail_user
    msg.attach(MIMEText(html_content, "html", "utf-8"))

    logging.info("Gmail SMTP 연결 중: smtp.gmail.com:587")
    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.ehlo()
        server.starttls()
        server.login(gmail_user, app_password)
        server.send_message(msg)
    logging.info("이메일 발송 완료 → %s", gmail_user)


def main() -> None:
    # 로깅 설정
    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s  %(levelname)-8s  %(message)s",
        handlers=[
            logging.FileHandler(LOG_FILE, encoding="utf-8"),
            logging.StreamHandler(sys.stdout),
        ],
    )

    logging.info("=" * 60)
    logging.info("Fashion Digest 자동화 시작")

    # 환경 변수 로드
    try:
        load_env()
    except FileNotFoundError as e:
        logging.error(str(e))
        sys.exit(1)

    gmail_user = os.environ.get("GMAIL_USER", "")
    app_password = os.environ.get("GMAIL_APP_PASSWORD", "")
    if not gmail_user or not app_password:
        logging.error("GMAIL_USER 또는 GMAIL_APP_PASSWORD가 .env에 없음")
        sys.exit(1)

    # 스킬 실행
    if not run_claude_skill():
        logging.error("스킬 실행 실패 — 종료")
        sys.exit(1)

    # 이메일 HTML 탐색
    email_html_path = get_today_email_html()
    if not email_html_path:
        logging.error("이메일 HTML 없음 — 종료")
        sys.exit(1)

    # 발송
    html_content = Path(email_html_path).read_text(encoding="utf-8")
    try:
        send_email(html_content, gmail_user, app_password)
    except smtplib.SMTPException as e:
        logging.error("이메일 발송 실패: %s", e)
        sys.exit(1)

    logging.info("Fashion Digest 자동화 완료")
    logging.info("=" * 60)


if __name__ == "__main__":
    main()
