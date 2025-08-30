import asyncio
from logging import FileHandler, StreamHandler, INFO, basicConfig, error as log_error, info as log_info
from os import path as ospath, environ
from subprocess import run as srun
from dotenv import load_dotenv, dotenv_values
from pymongo import AsyncMongoClient  # pymongo >= 5

# Setup logging
basicConfig(
    format="[%(asctime)s] [%(levelname)s] - %(message)s",
    datefmt="%d-%b-%y %I:%M:%S %p",
    handlers=[FileHandler('log.txt'), StreamHandler()],
    level=INFO
)

# Load environment variables
load_dotenv('config.env', override=True)

BOT_TOKEN = environ.get('BOT_TOKEN', '')
if not BOT_TOKEN:
    log_error("BOT_TOKEN variable is missing! Exiting now")
    exit(1)

bot_id = BOT_TOKEN.split(':', 1)[0]

DATABASE_URL = environ.get('DATABASE_URL')
UPSTREAM_REPO = None
UPSTREAM_BRANCH = ""


async def init_db():
    """Fetch configs from MongoDB if DATABASE_URL exists."""
    global UPSTREAM_REPO, UPSTREAM_BRANCH

    if not DATABASE_URL:
        return

    conn = AsyncMongoClient(DATABASE_URL)
    db = conn.bypass

    old_config = await db.settings.deployConfig.find_one({'_id': bot_id})
    config_dict = await db.settings.config.find_one({'_id': bot_id})

    if old_config is not None:
        old_config.pop('_id', None)

    if ((old_config is not None and old_config == dict(dotenv_values('config.env')))
            or old_config is None) and config_dict is not None:
        environ['UPSTREAM_REPO'] = config_dict.get('UPSTREAM_REPO', '')
        environ['UPSTREAM_BRANCH'] = config_dict.get('UPSTREAM_BRANCH', '')

    await conn.close()

    UPSTREAM_REPO = environ.get('UPSTREAM_REPO', '') or None
    UPSTREAM_BRANCH = environ.get('UPSTREAM_BRANCH', '')


async def update_repo():
    """Update repo from UPSTREAM_REPO if provided (no commit needed)."""
    if not UPSTREAM_REPO:
        return

    if ospath.exists('.git'):
        srun(["rm", "-rf", ".git"], check=True)

    update = srun(
        f"""
        git init -q &&
        git remote add origin {UPSTREAM_REPO} &&
        git fetch origin {UPSTREAM_BRANCH} -q &&
        git reset --hard origin/{UPSTREAM_BRANCH} -q
        """,
        shell=True
    )

    if update.returncode == 0:
        log_info('Successfully updated with latest commit from UPSTREAM_REPO')
    else:
        log_error('Something went wrong while updating, check UPSTREAM_REPO if valid or not!')

async def main():
    await init_db()
    await update_repo()


if __name__ == "__main__":
    asyncio.run(main())
