
# WebDeception

 ferramenta simples, rápida e altamente eficaz para detectar **Web Cache Deception**, explorando variações de caminhos e extensões em endpoints de aplicações web.

Essa técnica pode ser usada para tentar enganar mecanismos de cache a armazenar conteúdo sensível, como páginas privadas ou dados autenticados, de forma indevida.

## Funcionalidades

- Testes automáticos com delimitadores comuns (como `;`, `#`, `%00`, etc)
- Extensões populares de arquivos (`.css`, `.js`, `.exe`, etc)
- Validação por similaridade de tamanho de resposta
- Verificação de cabeçalhos de cache (`Cache-Control`, `X-Cache`, `Age`)
- Execução paralela para alto desempenho
- Barra de progresso e tempo estimado de finalização
- Salvamento opcional dos resultados
- Modo rápido para pentests mais ágeis

## Uso

```bash
python3 webdeception.py
```

Você será guiado interativamente a inserir:
- URL alvo
- Nome do arquivo de saída (opcional)
- Ativação do modo rápido

## Exemplo

```
Digite a URL do endpoint alvo (ex: https://site.com/profile)
URL: https://site.com/profile
Deseja salvar os resultados em um arquivo? (pressione Enter para ignorar)
Nome do arquivo (ex: resultados.txt): resultado.txt
Deseja usar o modo rápido (menos testes, mais desempenho)? (s/n)
Modo rápido: s
```

## Requisitos

Crie um ambiente virtual e instale as dependências:

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### requirements.txt

```
rich
requests
```

## Aviso Legal

Esta ferramenta foi criada com fins educacionais e de testes controlados em ambientes autorizados. **Nunca utilize contra sistemas sem permissão explícita.**
