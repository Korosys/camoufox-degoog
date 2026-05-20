[![Build & Publish Docker Image](https://github.com/Korosys/camoufox-degoog/actions/workflows/docker-publish.yml/badge.svg)](https://github.com/Korosys/camoufox-degoog/actions/workflows/docker-publish.yml)
# camoufox-degoog

A minimal Docker container that runs a [Camoufox](https://github.com/daijro/camoufox) server for use as a transport with the [degoog](https://github.com/degoog-org/degoog) self-hosted search aggregator.

This follows the setup described in the [degoog official extensions store](https://degoog-org.github.io/community-extensions/#repo=https%3A%2F%2Fgithub.com%2Fdegoog-org%2Fofficial-extensions&ext=transports%2Fcamoufox) with fixes applied to resolve errors encountered.

The camoufox server listens on port 3000.

The image is automatically rebuilt and published to the GitHub Container Registry whenever a new version of `camoufox` is released on PyPI.

---

## Quick start

### Docker Compose

Add the camoufox service to your existing degoog `compose.yml`:

```yaml
services:
  degoog:
    image: ghcr.io/degoog-org/degoog:latest
    volumes:
      - ./data:/app/data
    ports:
      - "4444:4444"
    restart: unless-stopped

  camoufox:
    image: ghcr.io/Korosys/camoufox-degoog:latest
    ports:
      - "3000:3000"
    restart: unless-stopped
```

Then point the camoufox transport in degoog's settings at `http://camoufox:3000`.

### Docker only

```bash
docker run -d \
  --name camoufox \
  -p 3000:3000 \
  --restart unless-stopped \
  ghcr.io/Korosys/camoufox-degoog:latest
```

---

## Connecting to degoog

1. Open your degoog instance and go to **Settings → Store**
2. Make sure the official extensions repo is added (`https://github.com/degoog-org/official-extensions`)
3. Install the **`transports/camoufox`** extension
4. Go to **Settings → Engines**, pick an engine, and set its **Outgoing HTTP client** to `camoufox`
5. In the transport settings, set the server URL to `http://camoufox:3000` (or `http://localhost:3000` if not using Compose networking)

---

## Image tags

| Tag | Description |
|-----|-------------|
| `latest` | Most recent build |
| `camoufox-x.y.z` | Pinned to a specific camoufox PyPI version |
| `sha-xxxxxxx` | Pinned to a specific git commit |

---

## Building locally

```bash
git clone https://github.com/Korosys/camoufox-degoog.git
cd camoufox-docker
docker build -t camoufox .
docker run -d -p 3000:3000 camoufox
```

---

## What was fixed
The following line was added to the Dockerfile to fix errors I was getting 

```bash
RUN apt-get update && apt-get install -y libasound2 && rm -rf /var/lib/apt/lists/*
```

---

## Links

- [Degoog](https://github.com/degoog-org/degoog)
- [Degoog official extensions](https://github.com/degoog-org/official-extensions)
- [Camoufox](https://github.com/daijro/camoufox)
- [degoog documentation](https://degoog-org.github.io/degoog/)
