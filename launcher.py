import modis

DISCORD_TOKEN = process.env.DISCORD_TOKEN
CLIENT_ID = "380719766471442433"

modis.gui(
    discord_token=DISCORD_TOKEN,
    discord_client_id=CLIENT_ID
)
