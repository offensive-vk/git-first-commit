import os
import subprocess
import datetime
import time
import random
import string
import re
import sys

def log(message, success=True):
    timestamp = datetime.datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")
    checkmark = "\033[92m[✔]\033[0m" if success else "\033[91m[✘]\033[0m"
    print(f"{timestamp} {checkmark} {message}")

def run_command(command):
    log(f"Executing: {command}")
    result = subprocess.run(command, shell=True, capture_output=True, text=True, check=False)
    if result.returncode != 0:
        log(f"Command failed with exit code {result.returncode}.", success=False)
        if result.stdout:
            log(f"--- STDOUT ---\n{result.stdout.strip()}", success=False)
        if result.stderr:
            log(f"--- STDERR ---\n{result.stderr.strip()}", success=False)
    else:
        log("Command executed successfully.", success=True)
    return result.stdout.strip(), result.stderr.strip(), result.returncode

def banner():
    print("""
==========================================================
🔥 Git Commit Manipulator 🔥
Author: @offensive-vk (modified)
Source: https://github.com/offensive-vk/git-first-commit
==========================================================
    """)

def generate_random_dir():
    while True:
        random_suffix = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
        dir_name = f"first-commit-{random_suffix}"
        if not os.path.exists(dir_name):
            return dir_name

def extract_repo_name(repo_url):
    match = re.search(r'/([^/]+?)(\.git)?$', repo_url)
    if match:
        return match.group(1)
    return generate_random_dir()

def select_or_clone_repository():
    repo_input = input("Enter Git repository path (local) or URL (remote), or '.' for current directory: ").strip()
    if not repo_input:
        log("No input provided!", success=False)
        sys.exit(1)
    if repo_input == '.':
        if os.path.exists(".git"):
            log("Using current directory as the repository.")
            return
        else:
            log("Current directory is not a Git repository.", success=False)
            sys.exit(1)
    elif os.path.isdir(repo_input):
        repo_path = os.path.abspath(repo_input)
        if os.path.exists(os.path.join(repo_path, ".git")):
            log(f"Using local repository at: {repo_path}")
            os.chdir(repo_path)
            return
        else:
            log(f"The path '{repo_input}' is not a Git repository.", success=False)
            sys.exit(1)
    else:
        repo_url = repo_input
        log(f"Attempting to clone remote repository: {repo_url}")
        repo_name = extract_repo_name(repo_url)
        stdout, stderr, returncode = run_command(f"git clone {repo_url} {repo_name}")
        if returncode != 0:
            log(f"Failed to clone repository '{repo_url}'.", success=False)
            sys.exit(1)
        if os.path.exists(repo_name):
            log(f"Repository cloned successfully into '{repo_name}'. Changing directory...")
            os.chdir(repo_name)
            time.sleep(1)
            return
        else:
            log(f"Cloning succeeded but directory '{repo_name}' not found.", success=False)
            sys.exit(1)

def get_first_commit():
    command = "git rev-list --max-parents=0 HEAD"
    commit_hash_output, stderr, returncode = run_command(command)
    if re.fullmatch(r'[0-9a-fA-F]{40}', commit_hash_output):
        return commit_hash_output
    else:
        log(f"Failed to retrieve a valid first commit hash. Output: '{commit_hash_output}'", success=False)
        return None

def list_and_choose_commit():
    stdout, stderr, returncode = run_command("git log --oneline --reverse")
    if returncode != 0:
        log("Failed to retrieve commit list.", success=False)
        return None
    commits = stdout.strip().split('\n')
    if not commits:
        log("No commits found.", success=False)
        return None
    print("\nAvailable commits:")
    for idx, commit in enumerate(commits):
        print(f"{idx + 1}. {commit}")
    choice = input("Enter the number of the commit you want to select: ").strip()
    if not choice.isdigit() or not (1 <= int(choice) <= len(commits)):
        log("Invalid choice!", success=False)
        return None
    selected_line = commits[int(choice) - 1]
    selected_hash = selected_line.split()[0]
    return selected_hash

def view_commit_details(commit_hash):
    stdout, stderr, returncode = run_command(f"git show {commit_hash} --stat")
    if returncode == 0:
        print(stdout)
    else:
        log("Failed to retrieve commit details.", success=False)
    time.sleep(2)

def create_branch_from_commit(commit_hash):
    branch_name = input("Enter new branch name: ").strip()
    if not branch_name:
        log("Branch name cannot be empty!", success=False)
        return
    stdout, stderr, returncode = run_command(f"git branch {branch_name} {commit_hash}")
    if returncode == 0:
        log(f"Branch '{branch_name}' created from commit.")
    time.sleep(2)

def edit_commit_message(commit_hash):
    new_message = input("Enter new commit message: ").strip()
    if not new_message:
        log("Commit message cannot be empty!", success=False)
        return
    run_command(f"git rebase -i --root")
    time.sleep(2)

def edit_commit_date(commit_hash):
    log("Enter new date (YYYY-MM-DD HH:MM:SS):")
    new_date_str = input("New date and time: ").strip()
    try:
        datetime.datetime.strptime(new_date_str, "%Y-%m-%d %H:%M:%S")
    except ValueError:
        log("Invalid date format!", success=False)
        return
    stdout, stderr, returncode_author = run_command(f'git show -s --format="%aN <%aE>" {commit_hash}')
    if returncode_author != 0:
        log("Failed to get author info.", success=False)
        return
    author_ident = stdout.strip()
    amend_command = f'GIT_AUTHOR_DATE="{new_date_str}" GIT_COMMITTER_DATE="{new_date_str}" GIT_AUTHOR_IDENT="{author_ident}" GIT_COMMITTER_IDENT="{author_ident}" git commit --amend --no-edit --date "{new_date_str}"'
    stdout, stderr, returncode = run_command(amend_command)
    if returncode == 0:
        log("Commit date updated successfully.")
    time.sleep(2)

def modify_commit_content():
    log("Modify files, stage changes, then press Enter...")
    input("Press Enter when ready to amend: ")
    stdout, stderr, returncode = run_command("git commit --amend --no-edit")
    if returncode == 0:
        log("Commit content updated successfully.")
    time.sleep(2)

def delete_commit():
    log("Starting interactive rebase to delete a commit.")
    log("An editor will open. Delete the commit you want to remove.")
    try:
        subprocess.call("git rebase -i --root", shell=True)
        log("Interactive rebase finished.")
    except Exception as e:
        log(f"Error during rebase: {e}", success=False)
    time.sleep(2)

def main():
    banner()
    select_or_clone_repository()
    if not os.path.exists(".git"):
        log("Not a Git repository.", success=False)
        sys.exit(1)

    commit_hash = list_and_choose_commit()
    if not commit_hash:
        log("Exiting.", success=False)
        sys.exit(0)

    log(f"Selected commit: {commit_hash}")

    while True:
        print("\nChoose an option:")
        print("1. View commit details")
        print("2. Edit commit message")
        print("3. Edit commit date and time")
        print("4. Modify commit content (amend)")
        print("5. Delete a commit (interactive rebase)")
        print("6. Create branch from selected commit")
        print("7. Select another commit")
        print("8. Exit")

        choice = input("Enter choice: ").strip()

        if choice == '1':
            view_commit_details(commit_hash)
        elif choice == '2':
            edit_commit_message(commit_hash)
        elif choice == '3':
            edit_commit_date(commit_hash)
        elif choice == '4':
            modify_commit_content()
        elif choice == '5':
            delete_commit()
            break
        elif choice == '6':
            create_branch_from_commit(commit_hash)
        elif choice == '7':
            commit_hash = list_and_choose_commit()
            if not commit_hash:
                log("No commit selected. Exiting.", success=False)
                break
            log(f"Selected commit: {commit_hash}")
        elif choice == '8':
            log("Exiting application.")
            break
        else:
            log("Invalid choice!", success=False)

if __name__ == "__main__":
    main()
