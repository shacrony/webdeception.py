
import requests
from rich.console import Console
from rich.progress import Progress, BarColumn, TimeRemainingColumn, TextColumn
from urllib.parse import urljoin
from concurrent.futures import ThreadPoolExecutor
import time
from datetime import datetime

console = Console()

# Lista ampliada
delimitadores = [";", ".", "%00", "!", '"', "#", "&", "=", ":", ",", "'", "(", ")", "+", "~", "*"]
sufixos = [".css", ".js", ".ico", ".exe", ".jpg", ".png", ".txt", ".svg", ".woff", ".ttf"]

def is_cached(headers):
    cache_control = headers.get("Cache-Control", "").lower()
    x_cache = headers.get("X-Cache", "").lower()
    age = headers.get("Age")

    if any(tag in cache_control for tag in ["no-cache", "no-store", "private"]):
        return False
    if "hit" in x_cache or (age and age.isdigit() and int(age) > 0):
        return True
    if "public" in cache_control or "max-age" in cache_control:
        return True
    return False

def tamanho_similar(base, test, tolerancia=0.05):
    return base * (1 - tolerancia) <= test <= base * (1 + tolerancia)

def testar_url(delim, sufix, url, base_status, base_len, output_lines):
    url_test = url + delim + "aaa" + sufix
    try:
        r = requests.get(url_test)
        if (
            r.status_code == base_status and
            tamanho_similar(base_len, len(r.content)) and
            is_cached(r.headers)
        ):
            result = f"[!] VULNERÁVEL: {url_test} | Cache-Control: {r.headers.get('Cache-Control', 'N/A')}"
            console.print(f"[bold red]{result}[/bold red]")
            output_lines.append(result)
    except:
        pass

def testar_endpoint(url, output_file=None, modo_rapido=False):
    console.print(f"[bold cyan][+] Testando endpoint base:[/] {url}")
    try:
        r_base = requests.get(url)
        base_status = r_base.status_code
        base_len = len(r_base.content)
        console.print(f"[+] Resposta base: {base_status} | {base_len} bytes")
        console.print(f"    Header Cache-Control: {r_base.headers.get('Cache-Control', 'N/A')}")
    except Exception as e:
        console.print(f"[red]Erro ao testar endpoint base: {e}[/red]")
        return

    output_lines = []
    total_testes = len(delimitadores) * (len(sufixos) if not modo_rapido else 1)

    with Progress(
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        "[progress.percentage]{task.percentage:>3.0f}%",
        TimeRemainingColumn(),
    ) as progress:
        task = progress.add_task("Executando testes...", total=total_testes)

        with ThreadPoolExecutor(max_workers=20) as executor:
            futures = []
            for delim in delimitadores:
                if not modo_rapido:
                    for sufix in sufixos:
                        futures.append(executor.submit(testar_url, delim, sufix, url, base_status, base_len, output_lines))
                else:
                    futures.append(executor.submit(testar_url, delim, ".exe", url, base_status, base_len, output_lines))

                progress.advance(task)

            for f in futures:
                f.result()

    if output_file:
        with open(output_file, "w", encoding="utf-8") as f:
            for line in output_lines:
                f.write(line + "\n")
        console.print(f"[green]Resultados salvos em {output_file}[/green]")

if __name__ == "__main__":
    url = input("Digite a URL do endpoint alvo (ex: https://site.com/profile)\nURL: ").strip()
    output_file = input("Deseja salvar os resultados em um arquivo? (pressione Enter para ignorar)\nNome do arquivo (ex: resultados.txt): ").strip()
    output_file = output_file if output_file else None
    modo = input("Deseja usar o modo rápido (menos testes, mais desempenho)? (s/n)\nModo rápido: ").strip().lower() == "s"
    testar_endpoint(url, output_file=output_file, modo_rapido=modo)
