from anime_parser.anime_methods import anime_stats, anime_description, episode_counter, final_episode_release_date
from anime_parser.ongoing_anime import anime_ongoing_list
import time


def ongoing_to_storage():
    result = []
    temporary_list = []

    for key, value in anime_ongoing_list().items():
        temporary_list.append(key)
        time.sleep(2)
        temporary_list.append(anime_description(value))
        time.sleep(2)
        temporary_list.append(value)
        time.sleep(2)
        temporary_list.append(anime_stats(value)[0])
        time.sleep(2)
        temporary_list.append(final_episode_release_date(anime_stats(value)))
        time.sleep(2)
        result.append(tuple(temporary_list))
        temporary_list.clear()
    return result





