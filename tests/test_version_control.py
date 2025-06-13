import os
import pytest
import subprocess
from pathlib import Path

def run_git_command(command):
    """Выполняет git команду и возвращает результат."""
    try:
        result = subprocess.run(
            ["git"] + command,
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        pytest.fail(f"Git команда завершилась с ошибкой: {e.stderr}")

def test_git_repository_exists():
    """Проверяет, что мы находимся в git репозитории."""
    assert Path(".git").exists(), "Директория .git не найдена"

def test_git_ignore_file():
    """Проверяет наличие и содержимое .gitignore."""
    gitignore_path = Path(".gitignore")
    assert gitignore_path.exists(), "Файл .gitignore не найден"
    
    # Проверяем наличие важных паттернов в .gitignore
    required_patterns = [
        "__pycache__",
        "*.pyc",
        ".env",
        ".venv",
        "venv",
        "*.log",
        ".idea",
        ".vscode"
    ]
    
    gitignore_content = gitignore_path.read_text()
    for pattern in required_patterns:
        assert pattern in gitignore_content, f"Паттерн {pattern} отсутствует в .gitignore"

def test_git_branch_naming():
    """Проверяет соответствие имен веток соглашениям."""
    current_branch = run_git_command(["branch", "--show-current"])
    
    # Проверяем, что имя ветки соответствует соглашениям
    valid_prefixes = ["feature/", "bugfix/", "hotfix/", "release/", "main", "master", "develop"]
    assert any(current_branch.startswith(prefix) for prefix in valid_prefixes), \
        f"Имя ветки {current_branch} не соответствует соглашениям"

def test_git_commit_messages():
    """Проверяет формат сообщений коммитов."""
    # Получаем последние 10 коммитов
    commits = run_git_command(["log", "-n", "10", "--pretty=format:%s"]).split("\n")
    
    for commit in commits:
        # Проверяем, что сообщение не пустое
        assert commit.strip(), "Найден коммит с пустым сообщением"
        
        # Проверяем, что сообщение начинается с заглавной буквы
        assert commit[0].isupper(), f"Сообщение коммита должно начинаться с заглавной буквы: {commit}"
        
        # Проверяем длину сообщения
        assert len(commit) <= 72, f"Сообщение коммита слишком длинное: {commit}"

def test_git_no_detached_head():
    """Проверяет, что мы не находимся в состоянии detached HEAD."""
    head_ref = run_git_command(["symbolic-ref", "HEAD"])
    assert head_ref, "HEAD не указывает на ветку (detached HEAD state)"

def test_git_no_uncommitted_changes():
    """Проверяет отсутствие незакоммиченных изменений."""
    status = run_git_command(["status", "--porcelain"])
    assert not status, "Найдены незакоммиченные изменения:\n" + status

def test_git_remote_exists():
    """Проверяет наличие удаленного репозитория."""
    remotes = run_git_command(["remote"]).split("\n")
    assert remotes, "Не найдены удаленные репозитории"

def test_git_branch_protection():
    """Проверяет защиту основных веток."""
    protected_branches = ["main", "master", "develop"]
    current_branch = run_git_command(["branch", "--show-current"])
    
    if current_branch in protected_branches:
        # Проверяем, что мы не можем напрямую пушить в защищенные ветки
        try:
            run_git_command(["push", "origin", current_branch, "--force"])
            pytest.fail(f"Успешный push в защищенную ветку {current_branch}")
        except subprocess.CalledProcessError:
            pass  # Ожидаемое поведение

def test_git_lfs_installed():
    """Проверяет, что Git LFS установлен и настроен."""
    try:
        run_git_command(["lfs", "version"])
    except subprocess.CalledProcessError:
        pytest.skip("Git LFS не установлен")

def test_git_hooks():
    """Проверяет наличие и работоспособность git hooks."""
    hooks_dir = Path(".git/hooks")
    assert hooks_dir.exists(), "Директория git hooks не найдена"
    
    # Проверяем наличие основных hooks
    required_hooks = ["pre-commit", "pre-push"]
    for hook in required_hooks:
        hook_path = hooks_dir / hook
        assert hook_path.exists(), f"Git hook {hook} не найден"
        assert os.access(hook_path, os.X_OK), f"Git hook {hook} не исполняемый"

def test_git_submodules():
    """Проверяет состояние git submodules."""
    try:
        submodules = run_git_command(["submodule", "status"]).split("\n")
        for submodule in submodules:
            if submodule:
                # Проверяем, что submodule инициализирован и обновлен
                assert not submodule.startswith("-"), f"Submodule не инициализирован: {submodule}"
                assert not submodule.startswith("+"), f"Submodule не обновлен: {submodule}"
    except subprocess.CalledProcessError:
        # Если submodules не используются, тест проходит
        pass 