from datetime import date, datetime
from collections import defaultdict


class WeatherEntry:
    def __init__(
        self, date_: date, average_temperature: float, probability_of_rain: float
    ) -> None:
        self.date_ = date_
        self.average_temperature = average_temperature
        self.probability_of_rain = probability_of_rain


def summarize_forecast(data):
    summaries = {}

    # Group entries by day
    entries_grouped_by_day = defaultdict(list)
    for entry in data:
        entry_datetime = datetime.fromisoformat(entry["date_time"])
        entry_date = entry_datetime.date()
        entries_grouped_by_day[entry_date].append(entry)

    # Process each day
    for day, entries in entries_grouped_by_day.items():
        morning_temperature = []
        morning_rain_probability = []
        afternoon_temperature = []
        afternoon_rain_probability = []

        all_t = [entry["average_temperature"] for entry in entries]

        for entry in entries:
            entry_time = datetime.fromisoformat(entry["date_time"])
            # collect morning period entries
            if 6 <= entry_time.hour < 12:
                morning_temperature.append(entry["average_temperature"])
                morning_rain_probability.append(entry["probability_of_rain"])
            # collection afternoon period entries
            elif 12 <= entry_time.hour < 18:
                afternoon_temperature.append(entry["average_temperature"])
                afternoon_rain_probability.append(entry["probability_of_rain"])

        summary = {
            # if no morning data, report insufficient data
            "morning_average_temperature": (
                "Insufficient forecast data"
                if not morning_temperature
                else round(sum(morning_temperature) / len(morning_temperature))
            ),
            "morning_chance_of_rain": (
                "Insufficient forecast data"
                if not morning_rain_probability
                else round(
                    sum(morning_rain_probability) / len(morning_rain_probability), 2
                )
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

        # format reader-friendly date
        day_name = day.strftime("%A %B %d").replace(" 0", " ")

        summaries[day_name] = summary

    return summaries
