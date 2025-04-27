# Atualizações Recomendadas: UV e Ruff

## Status Atual

Atualmente, o projeto Python Project Starter utiliza:
- UV versão 0.1.18 para gerenciamento de ambiente e pacotes
- Ruff versão 0.3.0 para linting e formatação de código
- Configuração já existente para formatação integrada do Ruff
- GitHub Actions para CI/CD com etapas de lint, type-check, test e build

## Atualizações Específicas Recomendadas

### UV (Universal Virtualenv)

- **Versão atual no projeto**: 0.1.18
- **Versão atual no mercado**: 0.2.24
- **Atualizações necessárias**:
  ```toml
  [project.optional-dependencies]
  dev = [
      "uv >= 0.2.0", # Atualizar para a versão mais recente
      # outras dependências...
  ]
  ```

#### Comandos UV a Atualizar no Código:

As atualizações específicas são necessárias em `src/project_starter/main.py`, linha ~290:

```python
# Atual
uv_venv_success, _ = _run_command(["uv", "venv"], cwd=root_path, console=console)
# ...
uv_sync_success, _ = _run_command(
    ["uv", "sync", "--dev"], cwd=root_path, console=console
)

# Recomendado (sintaxe atualizada UV 0.2+)
uv_venv_success, _ = _run_command(["uv", "venv"], cwd=root_path, console=console)
# ...
uv_sync_success, _ = _run_command(
    ["uv", "pip", "install", "-e", ".[dev]"], cwd=root_path, console=console
)
```

E nas mensagens de erro associadas linhas ~293 e ~305:

```python
# Atual
"[yellow]Warning:[/yellow] Failed to create virtual environment with uv. Please run 'uv venv' manually."
# ...
"[yellow]Warning:[/yellow] Failed to install dev dependencies with uv. Please run 'uv sync --dev' manually after activating the environment."

# Recomendado
"[yellow]Warning:[/yellow] Failed to create virtual environment with uv. Please run 'uv venv' manually."
# ...
"[yellow]Warning:[/yellow] Failed to install dev dependencies with uv. Please run 'uv pip install -e \".[dev]\"' manually after activating the environment."
```

### Ruff

- **Versão atual no projeto**: 0.3.0
- **Atualizações recomendadas**:
  ```toml
  [project.optional-dependencies]
  dev = [
      # outras dependências...
      "ruff >= 0.6.0",
      # outras dependências...
  ]
  ```

#### Melhorias na Configuração do Ruff:

A configuração atual já é boa, mas poderia ser expandida com:

```toml
[tool.ruff]
line-length = 88
target-version = "py310"
# Habilitar modo preview para usar os recursos mais recentes
preview = true

[tool.ruff.lint]
# Adicionando mais regras úteis aos já bem configurados
select = [
    "E",  # pycodestyle errors
    "F",  # Pyflakes
    "W",  # pycodestyle warnings
    "I",  # isort
    "N",  # pep8-naming
    "UP", # pyupgrade
    "B",  # flake8-bugbear
    "A",  # flake8-builtins
    "C4", # flake8-comprehensions
    "SIM",# flake8-simplify
    "PT", # flake8-pytest-style
    "PTH",# flake8-use-pathlib
    "RET",# flake8-return
    "SLF",# flake8-self
    "ARG",# flake8-unused-arguments
    "ERA",# eradicate (comentários comentados)
]
```

## Atualização do Template

O arquivo `src/project_starter/templates/_pyproject.toml.template` precisa ser atualizado de:

```toml
dev = [
    "uv >= 0.1.18",
    "ruff >= 0.3.0",
    # ...
]
```

Para:

```toml
dev = [
    "uv >= 0.2.0",
    "ruff >= 0.6.0",
    # ...
]
```

E adicionar a seção de preview na configuração do Ruff:

```toml
[tool.ruff]
line-length = 88
target-version = "py310"
preview = true  # Ativar recursos experimentais
```

## Atualizações no Fluxo CI/CD

O arquivo `.github/workflows/python-ci.yml` já está bem estruturado, mas poderia ser atualizado com:

```yaml
- name: Install dependencies
  run: |
    python -m pip install --upgrade pip
    pip install uv>=0.2.0 ruff>=0.6.0

# Na etapa de lint, alterar para utilizar preview
- name: Run ruff lint check
  run: |
    uv run ruff check --preview .
```

## Atualizações na Documentação

O arquivo `README.md` e outros precisam ser atualizados com os novos comandos:

- Substituir ocorrências de `uv sync --dev` por `uv pip install -e ".[dev]"` quando apropriado
- Atualizar versões recomendadas de ferramentas

## Resumo das Modificações Necessárias

1. **pyproject.toml**: Atualizar versões de UV e Ruff, adicionar modo preview
2. **main.py**: Atualizar comando de instalação e mensagens de erro
3. **_pyproject.toml.template**: Atualizar para novas versões e configurações
4. **python-ci.yml**: Modificar para usar novas versões e opção --preview
5. **Documentação**: Atualizar comandos e recomendações

## Próximos Passos Práticos

1. Implementar as atualizações no pyproject.toml e testar localmente
2. Atualizar templates e documentação
3. Modificar CI/CD para usar as novas versões
4. Verificar compatibilidade com projetos existentes (possíveis breaking changes)
5. Documentar qualquer mudança de comportamento na documentação do usuário
