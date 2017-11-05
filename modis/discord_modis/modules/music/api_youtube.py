import logging

from modis import datatools

import googleapiclient.discovery

logger = logging.getLogger(__name__)

ytdiscoveryapi = None


def build_api():
    data = datatools.get_data()
    if "google_api_key" not in data["discord"]["keys"]:
        logger.critical("No API key found with name 'google_api_key'")
        logger.info("Please add your google API key with name 'google_api_key' int the control panel")
        return False

    logger.debug("Building YouTube discovery API")
    ytdevkey = data["discord"]["keys"]["google_api_key"]
    try:
        global ytdiscoveryapi
        ytdiscoveryapi = googleapiclient.discovery.build("youtube", "v3", developerKey=ytdevkey)
        logger.debug("Build successfull")
        return True
    except:
        logger.critical("HTTP error connecting to YouTube API, build failed")
        return False


def get_ytvideos(query, ilogger):
    """Gets either a list of videos from a playlist or a single video, from the first result of a YouTube search

    Args:
        query (str): The YouTube search query
        ilogger (logging.logger): The logger to log API calls to

    Returns:
        queue (list): The items obtained from the YouTube search
    """

    queue = []

    # Search YouTube
    search_result = ytdiscoveryapi.search().list(
        q=query,
        part="id,snippet",
        maxResults=1,
        type="video,playlist"
    ).execute()

    if not search_result["items"]:
        return []

    # Get video/playlist title
    title = search_result["items"][0]["snippet"]["title"]
    ilogger.debug("Queueing {}".format(title))

    # Queue video if video
    if search_result["items"][0]["id"]["kind"] == "youtube#video":
        # Get ID of video
        videoid = search_result["items"][0]["id"]["videoId"]

        # Append video to queue
        queue.append(["https://www.youtube.com/watch?v={}".format(videoid), title])

    # Queue playlist if playlist
    elif search_result["items"][0]["id"]["kind"] == "youtube#playlist":
        # Get ID of playlist
        playlistid = search_result["items"][0]["id"]["playlistId"]

        # Get items in playlist
        playlist = ytdiscoveryapi.playlistItems().list(
            playlistId=playlistid,
            part="snippet",
            maxResults=50
        ).execute()

        # Append videos to queue
        for entry in playlist["items"]:
            videoid = entry["snippet"]["resourceId"]["videoId"]
            songname = entry["snippet"]["title"]
            queue.append(["https://www.youtube.com/watch?v={}".format(videoid), songname])

        # For playlists with more than 50 entries
        if "nextPageToken" in playlist:
            counter = 2

            while "nextPageToken" in playlist:
                ilogger.debug("Queueing {} (page {})".format(title, str(counter)))

                counter += 1

                # Get items in next page of playlist
                playlist = ytdiscoveryapi.playlistItems().list(
                    playlistId=playlistid,
                    part="snippet",
                    maxResults=50,
                    pageToken=playlist["nextPageToken"]
                ).execute()

                # Append videos to queue
                for entry in playlist["items"]:
                    videoid = entry["snippet"]["resourceId"]["videoId"]
                    songname = entry["snippet"]["title"]
                    queue.append(["https://www.youtube.com/watch?v={}".format(videoid), songname])

    return queue


build_api()
