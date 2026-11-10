# OTAS Development Environment Setup

## Prerequisites

### Windows (WSL 2)
1. Install WSL 2 (Ubuntu 22.04):
   ```powershell
   wsl --install -d Ubuntu-22.04
   ```
2. Install [Docker Desktop](https://www.docker.com/products/docker-desktop/) and enable **WSL 2 Integration** in *Settings > Resources*.
3. Open WSL and run the Quick Start command.

### macOS
1. Install [Docker Desktop for Mac](https://www.docker.com/products/docker-desktop/).
2. Install XQuartz for GUI support:
   ```bash
   brew install --cask xquartz
   ```
3. Open XQuartz, enable **"Allow connections from network clients"** in *Preferences > Security*, then run:
   ```bash
   xhost +localhost
   ```
4. Launch the container:
   ```bash
   DISPLAY=host.docker.internal:0 docker compose run --rm dev-environment
   ```

---


## Quick Start
Run this command in your terminal to launch the environment:

```bash
docker compose run --rm dev-environment
```

---

## Verification
Inside the container, run this command to verify all dependencies:

```bash
ros2 node list && gz sim --version && flake8 --version && pytest --version && cpplint --version
```
