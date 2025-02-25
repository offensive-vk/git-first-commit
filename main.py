# still a wip, atleast for now.
# 
# 
import os
import subprocess
import datetime

def log(message, success=True):
    timestamp = datetime.datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")
    checkmark = "\033[92m[✔]\033[0m" if success else "\033[91m[✘]\033[0m"
    print(f"{timestamp} {checkmark} {message}")

def run_command(command):
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    if result.returncode != 0:
        log(f"Error executing: {command}\n{result.stderr}", success=False)
    return result.stdout.strip(), result.stderr.strip()

def banner():
    print("""
    ========================================================
    🔥 Git First Commit Modifier 🔥 - @community
    Modify or Delete the First Commit of any git repository.
    ========================================================
    """)

def clone_repository():
    repo_url = input("Enter the Git repository URL to clone: ")
    stdout, stderr = run_command(f"git clone {repo_url} repo")
    if stderr:
        log("Failed to clone repository!", success=False)
        exit(1)
    os.chdir("repo")
    log("Repository cloned and switched to directory.")

def get_first_commit():
    commit_hash, _ = run_command("git rev-list --max-parents=0 HEAD")
    return commit_hash

def edit_commit_message(commit_hash):
    new_message = input("Enter new commit message: ")
    run_command(f'GIT_COMMITTER_DATE="$(git show -s --format=%ci {commit_hash})" git commit --amend -m "{new_message}"')
    log("Commit message updated.")

def edit_commit_date(commit_hash):
    new_date = input("Enter new date (YYYY-MM-DD HH:MM:SS): ")
    run_command(f'GIT_COMMITTER_DATE="{new_date}" git commit --amend --date "{new_date}"')
    log("Commit date updated.")

def modify_commit_content(commit_hash):
    log("Modify the files as needed, then press Enter to continue...")
    input()
    run_command("git commit --amend --no-edit")
    log("Commit content updated.")

def delete_first_commit(commit_hash):
    run_command(f"git rebase --onto {commit_hash}^ {commit_hash}")
    log("First commit deleted.")

def main():
    banner()
    clone_repository()

    if not os.path.exists(".git"):
        log("Not a Git repository!", success=False)
        return

    commit_hash = get_first_commit()
    if not commit_hash:
        log("No commits found!", success=False)
        return

    log(f"First commit found: {commit_hash}")

    while True:
        print("\nChoose an option:")
        print("1. Edit commit message")
        print("2. Edit commit date and time")
        print("3. Modify commit content")
        print("4. Delete first commit")
        print("5. Exit")

        choice = input("Enter choice: ")

        if choice == "1":
            edit_commit_message(commit_hash)
        elif choice == "2":
            edit_commit_date(commit_hash)
        elif choice == "3":
            modify_commit_content(commit_hash)
        elif choice == "4":
            delete_first_commit(commit_hash)
            break
        elif choice == "5":
            break
        else:
            log("Invalid choice!", success=False)

    log("Done. If changes were made, force push may be required: git push --force")

if __name__ == "__main__":
    main()


# Documentation is not finished yet, publishing it to github with docs and ci soon.
