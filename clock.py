from time import sleep
from apscheduler.schedulers.blocking import BlockingScheduler
from twitch_notifier import TwitchNotifier

live = False


def is_live():
    global live
    bot = TwitchNotifier()
    if bot.is_he_live():
        if not live:
            if bot.notify_discord():
                live = True
                print("Successfully done!!!")
        else:
            print("Still stream is live!!!")
            sleep(1800)
    else:
        if live:
            print("Streamer gone offline!!!")
            live = False
        else:
            print("Stream is not live yet!!!")


if __name__ == '__main__':
    sched = BlockingScheduler()
    sched.add_job(is_live, 'interval', seconds=30)
    sched.start()
