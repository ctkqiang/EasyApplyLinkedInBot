import time
from app import EasyApplyLinkedinJobBot as bot

if __name__ == '__main__':
    try:
        linkedinBot: object = bot(
            account='johnmelodyme',
            jobs=['flutter'],
            location='United Kingdom'
        )
        beginningTime: object = time.time()
        linkedinBot.main()
    except Exception as e:
        raise Exception(e)
    finally:
        print(
            "Job application Took=> " +
            str(round((time.time() - beginningTime)/60)) +
            " minute(s)."
        )
