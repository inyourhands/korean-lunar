from datetime import date, timedelta
from korean_lunar_calendar import KoreanLunarCalendar


START_YEAR = 2026
END_YEAR = 2050

OUTPUT_FILE = "korean-lunar.ics"


def escape_ics(text):
    return (
        str(text)
        .replace("\\", "\\\\")
        .replace(";", "\\;")
        .replace(",", "\\,")
        .replace("\n", "\\n")
    )


def get_lunar_date(d):
    calendar = KoreanLunarCalendar()

    if not calendar.setSolarDate(d.year, d.month, d.day):
        return None

    return (
        calendar.lunarYear,
        calendar.lunarMonth,
        calendar.lunarDay,
        calendar.isIntercalation,
    )


def main():
    start = date(START_YEAR, 1, 1)
    end = date(END_YEAR, 12, 31)

    lines = [
        "BEGIN:VCALENDAR",
        "VERSION:2.0",
        "PRODID:-//Korean Lunar Calendar//KO",
        "CALSCALE:GREGORIAN",
        "METHOD:PUBLISH",
        "X-WR-CALNAME:한국 음력",
        "X-WR-CALDESC:한국천문연구원 기준 한국 음력",
        "X-WR-TIMEZONE:Asia/Seoul",
    ]

    current = start

    while current <= end:
        lunar = get_lunar_date(current)

        if lunar:
            lunar_year, lunar_month, lunar_day, is_leap = lunar

            leap_text = "윤" if is_leap else ""

            summary = (
                f"음력 {lunar_year}년 "
                f"{leap_text}{lunar_month}월 "
                f"{lunar_day}일"
            )

            date_string = current.strftime("%Y%m%d")

            lines.extend([
                "BEGIN:VEVENT",
                f"UID:korean-lunar-{date_string}@github.com",
                f"DTSTART;VALUE=DATE:{date_string}",
                f"DTEND;VALUE=DATE:{(current + timedelta(days=1)).strftime('%Y%m%d')}",
                f"SUMMARY:{escape_ics(summary)}",
                "TRANSP:TRANSPARENT",
                "STATUS:CONFIRMED",
                "END:VEVENT",
            ])

        current += timedelta(days=1)

    lines.append("END:VCALENDAR")

    with open(OUTPUT_FILE, "w", encoding="utf-8", newline="\r\n") as f:
        f.write("\r\n".join(lines) + "\r\n")

    print(f"생성 완료: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
