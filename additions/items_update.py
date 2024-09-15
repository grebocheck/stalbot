import os
import asyncio
import time

from config import repo_url, repo_dir


async def run_command(command, cwd=None):
    process = await asyncio.create_subprocess_exec(
        *command,
        cwd=cwd,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )
    
    stdout, stderr = await process.communicate()
    
    if process.returncode == 0:
        print(stdout.decode().strip())
    else:
        print(f'Error: {stderr.decode().strip()}')

async def update_stalcraft_database_items():
    # update stalcraft database items
    
    if os.path.exists(repo_dir):
        await run_command(['git', 'pull'], cwd=repo_dir)
    else:
        os.makedirs(repo_dir, exist_ok=True)
        await run_command(['git', 'clone', repo_url, repo_dir])

async def update_stalcraft_database_items_loop():
    while True:
        try:
            await update_stalcraft_database_items()
            await asyncio.sleep(60*60*24)
        except Exception as e:
            print(e)
    