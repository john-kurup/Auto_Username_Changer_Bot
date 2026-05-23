import asyncio
    "rotator",
    api_id=API_ID,
    api_hash=API_HASH,
    session_string=SESSION_STRING
)

with open("usernames.txt", "r") as f:
    USERNAMES = [x.strip() for x in f.readlines() if x.strip()]

current_index = 0


async def rotate_username():
    global current_index

    await asyncio.sleep(random.randint(60, RANDOM_DELAY_MINUTES * 60))

    username = USERNAMES[current_index]

    try:
        channel = await app.resolve_peer(CHANNEL_ID)

        await app.invoke(
            UpdateUsername(
                channel=channel,
                username=username
            )
        )

        print(f"Changed username to: {username}")

        current_index += 1

        if current_index >= len(USERNAMES):
            current_index = 0

    except FloodWait as e:
        print(f"FloodWait: Sleeping {e.value} seconds")
        await asyncio.sleep(e.value)

    except UsernameOccupied:
        print(f"Username occupied: {username}")

    except UsernameInvalid:
        print(f"Invalid username: {username}")

    except Exception as e:
        print(f"Error: {e}")


async def main():
    await app.start()

    print("Bot Started")

    scheduler = AsyncIOScheduler()

    scheduler.add_job(
        rotate_username,
        "interval",
        minutes=CHANGE_INTERVAL_MINUTES
    )

    scheduler.start()

    while True:
        await asyncio.sleep(999999)


app.run(main())
