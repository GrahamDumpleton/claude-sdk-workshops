# Guided JupyterLab workshops for the Claude Agent SDK. Run `just` to list targets.

repo := "https://github.com/GrahamDumpleton/claude-sdk-workshops"

# The catalog names every collection in this repository, so one URL
# offers them all; each collection has an index of its own under
# collections/<name>/, with an id that never changes.
catalog_title := "Claude Agent SDK workshops"
catalog_description := "Guided JupyterLab workshops for the Claude Agent SDK for Python: what an agent is and how to run one, how to extend it, and how to build a chat application on it."

foundations_id := "grahamdumpleton.me/claude-agent-sdk/foundations"
foundations_title := "Agent foundations with the Claude Agent SDK"
foundations_description := "Guided JupyterLab workshops on what an AI agent is and how to run one with the Claude Agent SDK for Python: the agent loop, tools and their results, what a run costs, instructions, models, permissions, conversations, sessions, streaming and structured output."

# The foundations collection, in the order to take it. OUTLINE.md is the
# design this list follows; `just index` writes the index in this order,
# skipping any not written yet, so the order lives here and nowhere else.
foundations := "your-first-agent watching-the-agent-loop reading-the-result giving-the-agent-instructions choosing-a-model deciding-what-it-can-do holding-a-conversation picking-up-where-you-left-off streaming-the-reply getting-data-back"

extending_id := "grahamdumpleton.me/claude-agent-sdk/extending"
extending_title := "Extending an agent with the Claude Agent SDK"
extending_description := "Guided JupyterLab workshops on giving an agent built with the Claude Agent SDK for Python more to work with: your own tools, MCP servers, your own data, project instructions, skills, approvals, hooks, subagents and long sessions."

# The extending collection, in the order to take it.
extending := "giving-the-agent-a-tool connecting-an-mcp-server answering-from-your-own-data instructions-that-persist packaging-know-how-as-a-skill asking-before-acting guardrails-in-code handing-work-to-subagents keeping-a-long-session-small"

chat_app_id := "grahamdumpleton.me/claude-agent-sdk/chat-app"
chat_app_title := "Building a chat app with the Claude Agent SDK"
chat_app_description := "Guided JupyterLab workshops that build a web chat application on the Claude Agent SDK for Python, a step at a time: a first reply, streaming, a conversation per visitor, showing the agent's work, approvals, tools, history and usage."

# The chat app collection, in the order to take it.
chat_app := "the-smallest-chat-app streaming-to-the-browser one-conversation-per-visitor showing-the-agent-at-work approving-from-the-browser plugging-in-your-tools coming-back-to-a-conversation showing-usage-and-limits"

# List available targets.
default:
    @just --list

# Set up the environment: sync uv, fetch the reference checkouts, download the self-test browser, link the authoring skill.
install:
    uv sync
    git submodule update --init
    uv run playwright install chromium
    just skill

# The skill ships inside the jupyterlab-workshop package. Linking it into
# .claude/skills lets Claude Code load it without a copy in this repository,
# and it tracks the pinned release; rerun after bumping the version.
# Link the authoring skill from the installed package into .claude/skills.
skill:
    #!/usr/bin/env bash
    set -euo pipefail
    target=$(uv run python -c 'import jupyterlab_workshop, pathlib; print(pathlib.Path(jupyterlab_workshop.__file__).parent / "skills" / "jupyterlab-workshop-authoring")')
    mkdir -p .claude/skills
    ln -sfn "$target" .claude/skills/jupyterlab-workshop-authoring
    echo "Linked .claude/skills/jupyterlab-workshop-authoring -> $target"

# JupyterLab must run from this directory: the extension lists workshops/
# as installed, and the MCP live tools open workshops by paths relative
# to this root, such as workshops/<name>. The workshops call the model
# with the Claude login of whoever starts JupyterLab, so start it from a
# shell where `claude` is logged in and ANTHROPIC_API_KEY is not set.
# Start JupyterLab from the checkout, listing the workshops in each collection's order.
lab *ARGS:
    uv run jupyter lab --config=jupyter_lab_config.py {{ARGS}}

# Scaffold a new workshop under workshops/; extra args go to `jupyter workshop init`.
new NAME *ARGS:
    uv run jupyter workshop init workshops/{{NAME}} {{ARGS}}

# Lint the catalog, every collection index and every workshop, or only the workshops named.
lint *NAMES:
    #!/usr/bin/env bash
    set -euo pipefail
    shopt -s nullglob
    names=({{NAMES}})
    if [ ${#names[@]} -eq 0 ]; then
        if [ -f catalog.json ]; then
            uv run jupyter workshop lint catalog.json
        fi
        for index in collections/*/collection.json; do
            uv run jupyter workshop lint "$index"
        done
        dirs=(workshops/*/)
    else
        dirs=("${names[@]/#/workshops/}")
    fi
    if [ ${#dirs[@]} -eq 0 ]; then
        echo "No workshops under workshops/ yet"
        exit 0
    fi
    for dir in "${dirs[@]}"; do
        echo "== $dir"
        uv run jupyter workshop lint "$dir"
    done

# Render one workshop as HTML to check what a page looks like; extra args go to `jupyter workshop render`.
render NAME *ARGS:
    uv run jupyter workshop render workshops/{{NAME}} {{ARGS}}

# The self-test runs the workshop's actions and checks for real, as you,
# on this machine; only the workshop directory is protected, by a
# temporary copy. Here that means every cell that calls the agent calls
# the model, under your Claude login, and counts against its usage
# limits. Read the workshop first.
# Self-test one workshop in a JupyterLab of its own; extra args go to `jupyter workshop test`.
test NAME *ARGS:
    uv run jupyter workshop test workshops/{{NAME}} {{ARGS}}

# Every workshop calls the model, so this spends usage in proportion to
# the number of workshops. Run it before a release, not after each edit.
# Self-test every workshop, writing a JUnit report for each.
test-all:
    #!/usr/bin/env bash
    set -euo pipefail
    shopt -s nullglob
    for dir in workshops/*/; do
        name=$(basename "$dir")
        echo "== $dir"
        uv run jupyter workshop test "$dir" --junit "results-$name.xml"
    done

# Write or refresh every collection index and the catalog.
index: index-foundations index-extending index-chat-app catalog

# The workshop directories are named one by one, in the collection's
# order, which is how `jupyter workshop index` is told the order to
# write; naming only the directories that exist lets the index be
# refreshed while the collection is still being written. The repository
# URL is given explicitly so the index does not depend on a git remote
# being configured in the checkout.
# Write or refresh collections/foundations/collection.json in the collection's order.
index-foundations:
    #!/usr/bin/env bash
    set -euo pipefail
    dirs=()
    for name in {{foundations}}; do
        if [ -d "workshops/$name" ]; then
            dirs+=("workshops/$name")
        fi
    done
    if [ ${#dirs[@]} -eq 0 ]; then
        echo "No foundations workshops under workshops/ yet; collections/foundations/collection.json is left as it is"
        exit 0
    fi
    uv run jupyter workshop index "${dirs[@]}" --root . --out collections/foundations/collection.json --repo "{{repo}}" --id "{{foundations_id}}" --title "{{foundations_title}}" --description "{{foundations_description}}" --homepage "{{repo}}" --tag python --tag claude --tag agents --tag foundations --ordered

# Write or refresh collections/extending/collection.json in the collection's order.
index-extending:
    #!/usr/bin/env bash
    set -euo pipefail
    dirs=()
    for name in {{extending}}; do
        if [ -d "workshops/$name" ]; then
            dirs+=("workshops/$name")
        fi
    done
    if [ ${#dirs[@]} -eq 0 ]; then
        echo "No extending workshops under workshops/ yet; collections/extending/collection.json is left as it is"
        exit 0
    fi
    mkdir -p collections/extending
    uv run jupyter workshop index "${dirs[@]}" --root . --out collections/extending/collection.json --repo "{{repo}}" --id "{{extending_id}}" --title "{{extending_title}}" --description "{{extending_description}}" --homepage "{{repo}}" --tag python --tag claude --tag agents --tag tools --ordered

# Write or refresh collections/chat-app/collection.json in the collection's order.
index-chat-app:
    #!/usr/bin/env bash
    set -euo pipefail
    dirs=()
    for name in {{chat_app}}; do
        if [ -d "workshops/$name" ]; then
            dirs+=("workshops/$name")
        fi
    done
    if [ ${#dirs[@]} -eq 0 ]; then
        echo "No chat app workshops under workshops/ yet; collections/chat-app/collection.json is left as it is"
        exit 0
    fi
    mkdir -p collections/chat-app
    uv run jupyter workshop index "${dirs[@]}" --root . --out collections/chat-app/collection.json --repo "{{repo}}" --id "{{chat_app_id}}" --title "{{chat_app_title}}" --description "{{chat_app_description}}" --homepage "{{repo}}" --tag python --tag claude --tag agents --tag web --ordered

# Write or refresh catalog.json from the collection indexes, recorded by relative path.
catalog:
    uv run jupyter workshop catalog catalog.json collections/foundations/collection.json collections/extending/collection.json collections/chat-app/collection.json --relative --title "{{catalog_title}}" --description "{{catalog_description}}" --homepage "{{repo}}"

# The extension's reference checkout is what agents read for the workshop
# format beyond the skill (docs/, examples/ and the source), so it is
# kept at the tag of the pinned release and moves with the pin.
# Pin a new jupyterlab-workshop release, relock, relink the skill and move the reference checkout.
bump VERSION:
    uv add "jupyterlab-workshop=={{VERSION}}"
    just skill
    git -C reference/jupyterlab-workshop fetch --tags
    git -C reference/jupyterlab-workshop checkout "{{VERSION}}"
    git add reference/jupyterlab-workshop

# The SDK is pinned in pyproject.toml, since every workshop runs on this
# environment's kernel, and the reference checkout is what agents read
# for its source, examples and changelog, so the two move together. The
# SDK's tags carry a `v` prefix. The README names the same release in
# the uvx, uv tool and pip commands a learner copies, so it is rewritten
# here rather than left to be remembered.
# Pin a new claude-agent-sdk release, relock, move the reference checkout and update the README, e.g. `just bump-sdk 0.2.163`.
bump-sdk VERSION:
    #!/usr/bin/env bash
    set -euo pipefail
    uv add "claude-agent-sdk=={{VERSION}}"
    git -C reference/claude-agent-sdk-python fetch --tags
    git -C reference/claude-agent-sdk-python checkout "v{{VERSION}}"
    git add reference/claude-agent-sdk-python
    uv run python -c 'import pathlib, re, sys; p = pathlib.Path("README.md"); p.write_text(re.sub(r"claude-agent-sdk==[0-9][0-9A-Za-z.]*", "claude-agent-sdk==" + sys.argv[1], p.read_text()))' "{{VERSION}}"
    echo "claude-agent-sdk is at {{VERSION}}; reread the changelog and retest the workshops, since each one calls the release it is pinned to"

# No workshop here builds an environment of its own, so the prune is a
# no-op unless one is added later; it is kept so that a kernelspec left
# pointing at a removed environment never lingers in the launcher.
# Remove what opening, running and publishing the workshops leaves behind.
clean:
    rm -rf workshops/*/_workshop workshops/*/work workshops/*/dist workshops/*/scratch
    rm -f results-*.xml
    find . -type d -name .ipynb_checkpoints -not -path "./.venv/*" -exec rm -rf {} +
    find . -type d -name __pycache__ -not -path "./.venv/*" -not -path "./scratch/*" -not -path "./reference/*" -exec rm -rf {} +
    uv run jupyter workshop kernels --prune

# Also remove the environment and the skill link; run `just install` afterwards.
distclean: clean
    rm -rf .venv .claude/skills/jupyterlab-workshop-authoring
    git submodule deinit -f reference/jupyterlab-workshop reference/claude-agent-sdk-python
