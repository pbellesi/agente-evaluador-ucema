"""
Módulo de inspección y descarga de repositorios públicos de GitHub.

La aplicación no realiza llamadas a APIs generativas ni requiere API keys del usuario.
Sí requiere acceso de red a GitHub para obtener los repositorios públicos evaluados.
"""

import os
import re
import io
import zipfile
import requests
from typing import Dict, List, Tuple


# Extensiones excluidas por ser binarias o no relevantes para evaluación textual
EXCLUDED_EXTENSIONS = {
    ".png", ".jpg", ".jpeg", ".gif", ".ico", ".svg", ".pdf", ".zip", ".tar",
    ".gz", ".7z", ".exe", ".dll", ".so", ".dylib", ".pyc", ".pyo", ".db",
    ".sqlite", ".sqlite3", ".mp4", ".mp3", ".wav", ".avi", ".mov", ".woff",
    ".woff2", ".ttf", ".eot", ".bin", ".dat"
}

# Directorios a ignorar
EXCLUDED_DIRECTORIES = {
    ".git", "node_modules", "venv", ".venv", "env", "__pycache__",
    "dist", "build", ".idea", ".vscode", ".pytest_cache"
}

# Prefijos/carpetas prioritarias para la rúbrica UCEMA
PRIORITY_PATHS = [
    "readme", "decisiones", "prompts/", "corridas/", "src/", "docs/", "tests/", "casos/"
]

MAX_FILE_SIZE_BYTES = 100 * 1024  # 100 KB por archivo individual
MAX_TOTAL_BYTES = 500 * 1024       # 500 KB total de contenido leido


def parse_github_url(url: str) -> Tuple[str, str, str, str]:
    """
    Parsea una URL de GitHub para obtener (owner, repo, branch, subpath).
    Ejemplos:
    - https://github.com/owner/repo -> ('owner', 'repo', 'main', '')
    - https://github.com/owner/repo/tree/dev -> ('owner', 'repo', 'dev', '')
    - https://github.com/owner/repo/tree/main/casos/excelente -> ('owner', 'repo', 'main', 'casos/excelente')
    """
    cleaned = url.strip().rstrip("/")
    # Eliminar extensión .git si existe
    if cleaned.endswith(".git"):
        cleaned = cleaned[:-4]

    pattern = r"github\.com/([^/]+)/([^/]+)(?:/tree/([^/]+)(?:/(.+))?)?"
    match = re.search(pattern, cleaned)
    if not match:
        raise ValueError(f"URL de GitHub no válida: {url}")

    owner = match.group(1)
    repo = match.group(2)
    branch = match.group(3) or "main"
    subpath = (match.group(4) or "").strip("/")
    return owner, repo, branch, subpath


def _is_text_file(filename: str) -> bool:
    ext = os.path.splitext(filename)[1].lower()
    return ext not in EXCLUDED_EXTENSIONS


def _is_excluded_path(path: str) -> bool:
    parts = path.split("/")
    for part in parts:
        if part in EXCLUDED_DIRECTORIES:
            return True
    return False


def _get_path_priority(path: str) -> int:
    path_lower = path.lower()
    for idx, prio in enumerate(PRIORITY_PATHS):
        if prio in path_lower:
            return idx
    return 999


def fetch_repository_data(github_url: str) -> dict:
    """
    Descarga e inspecciona un repositorio público de GitHub (o subcarpeta).
    Retorna un diccionario con:
    - repository: owner/repo (o owner/repo/subpath)
    - branch: rama evaluada
    - subpath: subcarpeta evaluada o ""
    - tree_inventory: inventario en árbol completo del área evaluada
    - file_contents: dict de path -> contenido
    - formatted_context: bloque de texto formateado listo para inyectar como UNTRUSTED DATA.
    """
    owner, repo, branch, subpath = parse_github_url(github_url)
    
    # Intentar descargar ZIP para la rama indicada (con fallback a master si falla main)
    branches_to_try = [branch]
    if branch == "main":
        branches_to_try.append("master")

    zip_content = None
    successful_branch = branch

    for b in branches_to_try:
        zip_url = f"https://github.com/{owner}/{repo}/archive/refs/heads/{b}.zip"
        resp = requests.get(zip_url, timeout=20)
        if resp.status_code == 200:
            zip_content = resp.content
            successful_branch = b
            break

    if not zip_content:
        raise RuntimeError(
            f"No se pudo acceder al repositorio https://github.com/{owner}/{repo} en la rama '{branch}'. "
            "Verifica que el repositorio sea público y que la rama exista."
        )

    # Procesar archivo ZIP en memoria
    # all_files contiene tuplas (target_path, zip_member_rel_path, size)
    all_files: List[Tuple[str, str, int]] = []
    text_files: Dict[str, str] = {}

    with zipfile.ZipFile(io.BytesIO(zip_content)) as z:
        namelist = z.namelist()
        if not namelist:
            raise RuntimeError("El repositorio está vacío.")
        
        # El nombre del directorio raíz en el ZIP suele ser owner-repo-commit/ o repo-branch/
        root_prefix = namelist[0].split("/")[0] + "/"

        for member in z.infolist():
            if member.is_dir():
                continue
            rel_path = member.filename
            if rel_path.startswith(root_prefix):
                rel_path = rel_path[len(root_prefix):]

            if not rel_path or _is_excluded_path(rel_path):
                continue

            # Filtrar subcarpeta si se especificó
            if subpath:
                if not (rel_path.startswith(subpath + "/") or rel_path == subpath):
                    continue
                target_path = rel_path[len(subpath):].lstrip("/")
            else:
                target_path = rel_path

            if not target_path:
                continue

            all_files.append((target_path, rel_path, member.file_size))

        if not all_files:
            raise RuntimeError(
                f"No se encontraron archivos en la subcarpeta '{subpath}' del repositorio https://github.com/{owner}/{repo}."
            )

        # Construir el inventario completo en árbol (ordenado alfabéticamente por target_path)
        all_files.sort(key=lambda x: x[0])
        tree_inventory_lines = [f"{path} ({size} bytes)" for path, _, size in all_files]
        tree_inventory_str = "\n".join(tree_inventory_lines)

        # Ordenar archivos para lectura según prioridad
        readable_files = [f for f in all_files if _is_text_file(f[0])]
        readable_files.sort(key=lambda x: (_get_path_priority(x[0]), x[0]))

        total_bytes_read = 0
        for target_path, zip_rel_path, file_size in readable_files:
            if total_bytes_read >= MAX_TOTAL_BYTES:
                break

            # Buscar la clave interna completa en el ZIP
            zip_member_name = root_prefix + zip_rel_path
            try:
                raw_bytes = z.read(zip_member_name)
                if len(raw_bytes) > MAX_FILE_SIZE_BYTES:
                    raw_bytes = raw_bytes[:MAX_FILE_SIZE_BYTES] + b"\n... [TRUNCADO POR TAMANO]"

                # Intentar decodificar UTF-8 (con fallback a latin-1)
                try:
                    content_text = raw_bytes.decode("utf-8")
                except UnicodeDecodeError:
                    content_text = raw_bytes.decode("latin-1", errors="replace")

                text_files[target_path] = content_text
                total_bytes_read += len(raw_bytes)
            except Exception as e:
                text_files[target_path] = f"[Error al leer archivo: {str(e)}]"

    # Intentar obtener el commit SHA exacto desde la API de GitHub
    commit_sha = "unknown"
    try:
        commit_api_url = f"https://api.github.com/repos/{owner}/{repo}/commits/{successful_branch}"
        commit_resp = requests.get(commit_api_url, timeout=5)
        if commit_resp.status_code == 200:
            commit_sha = commit_resp.json().get("sha", "unknown")
    except Exception:
        pass

    evaluated_revision = f"{successful_branch}@{commit_sha[:10]}" if commit_sha != "unknown" else successful_branch

    # Generar bloque formateado de datos no confiables (UNTRUSTED REPOSITORY DATA)
    canonical_repo_id = f"{owner}/{repo}::{subpath}" if subpath else f"{owner}/{repo}"
    target_display_name = os.path.basename(subpath) if subpath else f"{owner}/{repo}"

    formatted_parts = [
        f"=== TRABAJO EVALUADO: {target_display_name} ===",
        tree_inventory_str,
        "\n=== CONTENIDO DE ARCHIVOS INSPECCIONADOS ==="
    ]

    for path, content in text_files.items():
        formatted_parts.append(f"\n--- ARCHIVO: {path} ---")
        formatted_parts.append(content)

    formatted_context = "\n".join(formatted_parts)

    return {
        "repository": canonical_repo_id,
        "display_name": target_display_name,
        "branch": successful_branch,
        "commit_sha": commit_sha,
        "evaluated_revision": evaluated_revision,
        "subpath": subpath,
        "tree_inventory": tree_inventory_str,
        "file_contents": text_files,
        "formatted_context": formatted_context
    }
