# 🔥 Git First Commit

## 🛠️ Overview

`Git First Commit` is a powerful Python script that allows you to **modify, delete, or inspect the first commit** of any Git repository. Whether you want to edit the message, update the commit date, modify the content, or even remove the first commit entirely—this tool has you covered! 🚀

## 🎯 Features

- ✅ Clone any Git repository 🔗
- ✅ Retrieve & modify the **first commit** ✍️
- ✅ Edit the commit **message, date, author** 🕒
- ✅ Modify commit **content** before re-amending 📄
- ✅ **Delete** the first commit (Rebase) ❌
- ✅ Create a **branch** from the first commit 🌱
- ✅ View detailed **commit stats** 📊
- ✅ Handles directory naming dynamically 📂
- ✅ **User-friendly prompts & error handling** 💡

## 📌 Prerequisites

🔹 Ensure you have **Git** installed (`git --version`) ✅  
🔹 Ensure **Python 3** is installed (`python3 --version`) 🐍  
🔹 Internet connection for cloning repositories 🌐  

## 🚀 Installation & Usage

### 1️⃣ Clone this script
```sh
 git clone https://github.com/offensive-vk/git-first-commit.git
 cd git-first-commit
```

### 2️⃣ Run the script
```sh
 python3 git_modifier.py
```

## 📖 How It Works

### 🔹 Cloning the Repository
You will be prompted to enter the GitHub repository URL. The script automatically extracts the repository name and uses it as the cloning directory. If the name can't be determined, it assigns a **unique random directory** starting with `first-*`.

### 🔹 Choosing an Action
Once cloned, the script identifies the first commit and offers you several operations:

1️⃣ **View commit details** 📜  
2️⃣ **Edit commit message** ✏️  
3️⃣ **Edit commit date & time** ⏳  
4️⃣ **Modify commit content** 🛠️  
5️⃣ **Delete first commit** 🚨  
6️⃣ **Create branch from first commit** 🌿  
7️⃣ **Modify or erase the commit author** 👤  
8️⃣ **Exit** 🚪  

### 🔹 Handling Errors
🔴 If cloning fails, the script suggests fixes.  
🔴 If Git commands fail, it logs errors in **verbose mode** for troubleshooting.  

## ⚠️ Important Notes

⚠️ **Modifying history can break repository integrity!** Always test in a separate branch before force-pushing.  
⚠️ If you modify history, a force push (`git push --force`) may be required.  
⚠️ Back up your work before running destructive operations!  

## 🤝 Contributions

Contributions are welcome! Feel free to **fork** this repository, make improvements, and submit a **pull request**. 💡

## 📜 License

This script is open-source and distributed under the **MIT License**.
