import threading
import time
from os.path import exists
from typing import Dict

from anti_plagiarism import Repository, AntiPlagiarism, comp_diff
import config
from config import MIN_DIFF, MAX_THREADS

result = {}


def repo_diff(repo: Repository, sources: Dict[str, str], ap: AntiPlagiarism):
    files = ap.get_repo_files(repo)
    if not files:
        print("[!] Files not found in", repo.path)
    for file in files:

        full_url = f"https://github.com/{repo.path}/blob/{repo.default_branch}/{file.path}".replace(" ", "%20")

        for url, source in sources.items():
            diff = comp_diff(source, file.content) * 100
            result[full_url + '///' + url] = diff


def main():
    urls = ("https://github.com/ShimmeryHirm/labs/blob/master/include/arrays.h",)

    if not exists("repos.txt"):
        open("repos.txt", "w").close()
        print("[-] Fill repositories in repos.txt")
        return

    ap = AntiPlagiarism(config.TOKEN)

    sources = dict(zip(urls, ap.get_raw(urls)))

    print("[*] Sources:", ", ".join(urls), "\n")
    print("[*] Preparing..")

    start = time.time()

    with open("repos.txt") as f:
        repos = f.readlines()

    in_repos = []

    for repo in repos:
        repo = repo.strip().split(".com/")[1].strip('/').split("?")[0].rstrip('.git')
        if repo.count('/') == 1:
            f = ap.get_repo
            action = in_repos.append
        else:
            f = ap.get_user_repos
            action = in_repos.extend

        if res := f(repo):
            action(res)

    print(f"[*] Found {len(in_repos)} repos for {(time.time() - start):.1f}s")
    print("\n[*] Scanning...")

    start = time.time()

    threads_count = MAX_THREADS
    threads = {}
    for repo in in_repos:
        thread = threading.Thread(target=repo_diff, args=(repo, sources, ap))
        threads[thread] = 0
    while threads:
        for i in threads.copy():
            if not threads[i] and threads_count:
                threads[i] = 1
                threads_count -= 1
                i.start()

        for thread in [thread for thread in threads if not thread.is_alive() and threads[thread]]:
            del threads[thread]
            threads_count += 1

    print(f"[*] Done for {(time.time() - start):.1f}s\n")
    print(f"[*] Results with >{MIN_DIFF}% similarity")

    sorted_result = dict(sorted(result.items(), key=lambda item: item[1], reverse=True))
    for res in sorted_result:
        if sorted_result[res] >= MIN_DIFF:
            add = '' if len(urls) == 1 else f"for {res.split('///')[1].split('/', maxsplit=7)[-1]}"
            print(f"[+] {sorted_result[res]:.1f}% {res.split('///')[0]} {add}")


if __name__ == '__main__':
    main()
