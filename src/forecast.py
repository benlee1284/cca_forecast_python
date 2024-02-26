from datetime import datetime, date
from collections import defaultdict
from typing import Any


class WeatherEntry:
    def __init__(
        self,
        date_time: datetime,
        average_temperature: float,
        probability_of_rain: float,
    ) -> None:
        self.date_time = date_time
        self.average_temperature = average_temperature
        self.probability_of_rain = probability_of_rain

    def is_morning(self) -> bool:
        return 6 <= self.date_time.hour < 12

    def is_afternoon(self) -> bool:
        return 12 <= self.date_time.hour < 18

    def get(self, name: str) -> Any:
        return getattr(self, name)


class DailyWeatherSummary:
    def __init__(self) -> None: ...

    def to_dict(self) -> dict: ...


def summarize_forecast(data):
    summaries = {}

    weather_entries = parse_weather_entries(data)

    entries_grouped_by_day = group_entries_by_day(weather_entries)

    # Process each day
    for day, entries in entries_grouped_by_day.items():
        summary = create_summary(entries)

        # format reader-friendly date
        day_name = day.strftime("%A %B %d").replace(" 0", " ")

        summaries[day_name] = summary

    return summaries


def create_summary(entries: list[WeatherEntry]) -> dict:
    morning_temperature = []
    morning_rain_probability = []
    afternoon_temperature = []
    afternoon_rain_probability = []

    all_t = [entry.average_temperature for entry in entries]

    for entry in entries:
        # collect morning period entries
        if entry.is_morning():
            morning_temperature.append(entry.average_temperature)
            morning_rain_probability.append(entry.probability_of_rain)
        # collection afternoon period entries
        elif entry.is_afternoon():
            afternoon_temperature.append(entry.average_temperature)
            afternoon_rain_probability.append(entry.probability_of_rain)

    return {
        # if no morning data, report insufficient data
        "morning_average_temperature": (
            "Insufficient forecast data"
            if not morning_temperature
            else round(sum(morning_temperature) / len(morning_temperature))
        ),
        "morning_chance_of_rain": (
            "Insufficient forecast data"
            if not morning_rain_probability
            else round(sum(morning_rain_probability) / len(morning_rain_probability), 2)
        ),
        # if no afternoon data, report insufficient data
        "afternoon_average_temperature": (
            "Insufficient forecast data"
            if not afternoon_temperature
            else round(sum(afternoon_temperature) / len(afternoon_temperature))
        ),
        "afternoon_chance_of_rain": (
            "Insufficient forecast data"
            if not afternoon_rain_probability
            else round(
                sum(afternoon_rain_probability) / len(afternoon_rain_probability), 2
            )
        ),
        "high_temperature": max(all_t),
        "low_temperature": min(all_t),
    }


def parse_weather_entries(raw_data: list[dict]) -> list[WeatherEntry]:
    return [
        WeatherEntry(
            date_time=get_datetime(raw_entry),
            average_temperature=raw_entry["average_temperature"],
            probability_of_rain=raw_entry["probability_of_rain"],
        )
        for raw_entry in raw_data
    ]


def get_datetime(entry):
    return datetime.fromisoformat(entry.get("date_time").replace("Z", "+00:00"))


def group_entries_by_day(
    weather_entries: list[WeatherEntry],
) -> dict[date, list[WeatherEntry]]:
    entries_grouped_by_day = defaultdict(list)
    for entry in weather_entries:
        entry_datetime = entry.date_time
        entry_date = entry_datetime.date()
        entries_grouped_by_day[entry_date].append(entry)

    return entries_grouped_by_day
