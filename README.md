# branch  backup
Serve para guardar o código original de como funcionava dentro da plataforma Choreo. Portanto, caso dê algum erro irritante, é possível ter o código inicial como parâmetro.

# 🎬 watchhive-backend

API backend do TCC para um site de avaliação e recomendação de filmes e séries.

---

## 📦 Gerenciamento de Pacotes

Este projeto utiliza o [uv](https://github.com/astral-sh/uv) para facilitar o gerenciamento de dependências.

### Instalação do uv

Execute o comando abaixo no **Git Bash**:

```sh
curl -LsSf https://astral.sh/uv/install.sh | sh
```

---

## 📚 Como adicionar dependências

Sempre que precisar de uma nova biblioteca, utilize:

```sh
uv add [nome-da-biblioteca]
```

**Exemplo:**

```sh
uv add fastapi
```

A dependência será instalada e registrada automaticamente no ambiente virtual do projeto.

---

## 💡 Observações

- O uso do `uv` facilita a instalação e o controle das dependências.
- Lembre-se de rodar os comandos sempre dentro do diretório do projeto.

---

## 🧹 Checagem e Formatação de Código com Ruff

Para verificar problemas de estilo e organizar os imports, utilize:

```sh
uvx ruff check
```

Para formatar automaticamente o código e corrigir os imports, utilize:

```sh
uvx ruff format
```

---
