import time
from app import EasyApplyLinkedinJobBot as bot
from getpass import getpass


if __name__ == "__main__":
    positions = ["python"]  # 修改为你想要申请的职位关键词
    country: str = input("🌏 在哪个国家找工作呢？ ")
    account: str = input("📧 LinkedIn账号是啥呀～ ")
    password: str = getpass("🔐 悄悄输入密码吧～ ")

    try:
        linkedinBot: object = bot(
            account=account,
            password=password,
            jobs=positions,
            location=country,
        )
        beginningTime: object = time.time()
        linkedinBot.main()
    except Exception as e:
        raise Exception(e)
    finally:
        print(
            "⏰ 投递任务结束啦！总共花了 "
            + str(round((time.time() - beginningTime) / 60))
            + " 分钟呢～"
        )
