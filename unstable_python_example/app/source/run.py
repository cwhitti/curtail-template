from server import server_loop

try:
    server_loop()

except Exception as e:
    raise e
    quit()
