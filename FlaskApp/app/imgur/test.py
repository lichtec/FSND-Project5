from imgurpython import ImgurClient

client_id = '95123b1565c2a83'
client_secret = '1e0a0fe1040481cca186309b83508b9f9cf3c3a0'

client = ImgurClient(client_id, client_secret)

# Example request
album = client.get_Album('TlFpu')
for images in album:
    print(images[link])
