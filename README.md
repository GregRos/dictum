# Dictum

Runs commands on the containers of a pod with a specific user (root by default).

## Usage

```bash
$ dictum run -s "[app=nginx]" -u root -C /bin/bash
```
