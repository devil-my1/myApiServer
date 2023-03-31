import asyncio
import platform
import nats
import random


if platform.system() == "Windows":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


async def main():
    try:
        # Connect to NATS!
        nc = await nats.connect(
            servers=["nats://185.51.246.205:2222"],
            user="local",
            password="WC00cIJqoBNMje8jHb2pDCrdhPF28IeI",
        )

        js = nc.jetstream()

        # Publish a message
        ack = await js.publish(
            "develop.ncm.subject",
            f"Random (1-100): {random.randint(1,100)}".encode("utf-8"),
        )
        print("Published message to [{}] with seq: {}".format(ack.stream, ack.seq))
    except Exception as err:
        print(f"Error: {err.with_traceback(err.__traceback__)}")
    finally:
        ...
        # Close NATS connection
        await nc.close()


if __name__ == "__main__":
    asyncio.run(main())
