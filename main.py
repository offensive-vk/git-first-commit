import os
import subprocess
import datetime
import time
import random
import string


def log(message, success=True):
    """Logs a message with timestamp and success/failure status."""
    timestamp = datetime.datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")
    checkmark = "\033[92m[✔]\033[0m" if success else "\033[91m[✘]\033[0m"
    print(f"{timestamp} {checkmark} {message}")


def run_command(command):
    """Runs a shell command and returns its stdout and stderr."""
    log(f"Executing: {command}")
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    if result.returncode != 0:
        log(f"Error executing: {command}\n{result.stderr}", success=False)
    return result.stdout.strip(), result.stderr.strip()


def generate_random_directory():
    """Generates a unique random directory name with 'first-*' prefix."""
    while True:
        random_suffix = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
        dir_name = f"first-{random_suffix}"
        if not os.path.exists(dir_name):
            return dir_name


def banner():
    """Displays the script banner."""
    print("""
    ========================================================
    🔥 Git First Commit Modifier 🔥
    Modify, Delete, or Inspect the First Commit of any git repository.
    Author: Vedansh
    Source: Custom Script
    ========================================================
    """)


def clone_repository():
    """Prompts the user for a repository URL, clones it, and changes into the directory."""
    repo_url = input("Enter the Git repository URL to clone: ").strip()
    if not repo_url:
        log("No repository URL provided!", success=False)
        exit(1)
    
    repo_name = repo_url.rstrip('/').split('/')[-1] if '/' in repo_url else None
    clone_dir = repo_name if repo_name and not os.path.exists(repo_name) else generate_random_directory()
    
    stdout, stderr = run_command(f"git clone {repo_url} {clone_dir}")
    if stderr:
        log("Failed to clone repository! Ensure the URL is correct and you have access.", success=False)
        exit(1)
    
    log(f"Repository cloned successfully into {clone_dir}. Changing directory...")
    time.sleep(2)
    os.chdir(clone_dir)


def get_first_commit():
    """Returns the hash of the first commit in the repository."""
    commit_hash, stderr = run_command("git rev-list --max-parents=0 HEAD")
    if stderr:
        log("Failed to retrieve first commit.", success=False)
        return None
    return commit_hash


def view_commit_details(commit_hash):
    """Displays the details of the first commit."""
    stdout, stderr = run_command(f"git show {commit_hash} --stat")
    if stderr:
        log("Failed to retrieve commit details.", success=False)
    else:
        print(stdout)
    time.sleep(2)


def create_branch_from_first_commit(commit_hash):
    """Creates a new branch from the first commit."""
    branch_name = input("Enter new branch name: ").strip()
    if not branch_name:
        log("Branch name cannot be empty!", success=False)
        return
    
    run_command(f"git branch {branch_name} {commit_hash}")
    log(f"Branch '{branch_name}' created from the first commit.")
    time.sleep(2)


def edit_commit_message(commit_hash):
    """Allows the user to modify the first commit message."""
    new_message = input("Enter new commit message: ").strip()
    if not new_message:
        log("Commit message cannot be empty!", success=False)
        return
    
    run_command(f'GIT_COMMITTER_DATE="$(git show -s --format=%ci {commit_hash})" git commit --amend -m "{new_message}"')
    log("Commit message updated successfully.")
    time.sleep(2)


def edit_commit_date(commit_hash):
    """Allows the user to modify the commit date."""
    new_date = input("Enter new date (YYYY-MM-DD HH:MM:SS): ").strip()
    
    if not new_date:
        log("Invalid date format!", success=False)
        return
    
    run_command(f'GIT_COMMITTER_DATE="{new_date}" git commit --amend --date "{new_date}"')
    log("Commit date updated successfully.")
    time.sleep(2)


def modify_commit_content():
    """Allows the user to modify files before amending the first commit."""
    log("Modify the files as needed, then press Enter to continue...")
    input()
    run_command("git commit --amend --no-edit")
    log("Commit content updated successfully.")
    time.sleep(2)


def delete_first_commit(commit_hash):
    """Deletes the first commit and rebases the repository."""
    run_command(f"git rebase --onto {commit_hash}^ {commit_hash}")
    log("First commit deleted successfully.")
    time.sleep(2)


def main():
    """Main function that orchestrates user choices."""
    banner()
    clone_repository()
    
    if not os.path.exists(".git"):
        log("Not a valid Git repository!", success=False)
        return
    
    commit_hash = get_first_commit()
    if not commit_hash:
        log("No commits found in the repository!", success=False)
        return
    
    log(f"First commit found: {commit_hash}")
    
    while True:
        print("\nChoose an option:")
        print("1. View commit details")
        print("2. Edit commit message")
        print("3. Edit commit date and time")
        print("4. Modify commit content")
        print("5. Delete first commit")
        print("6. Create branch from first commit")
        print("7. Exit")
        
        choice = input("Enter choice: ").strip()
        
        if choice == "1":
            view_commit_details(commit_hash)
        elif choice == "2":
            edit_commit_message(commit_hash)
        elif choice == "3":
            edit_commit_date(commit_hash)
        elif choice == "4":
            modify_commit_content()
        elif choice == "5":
            delete_first_commit(commit_hash)
            break
        elif choice == "6":
            create_branch_from_first_commit(commit_hash)
        elif choice == "7":
            break
        else:
            log("Invalid choice! Please try again.", success=False)
    
    log("Done. If changes were made, you may need to force push: git push --force")
    time.sleep(2)


if __name__ == "__main__":
    main()
