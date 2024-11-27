# ReportEAO

Plataforma para reportar problemáticas en la Escuela de Artes y Oficios

## Instalación

ReportEAO requiere Python >=3.11. Se puede instalar de dos maneras.

### Poetry

Instale [Poetry](https://python-poetry.org), y corra el siguiente comando para instalar las dependencias.

```
$ poetry install
```

Copie el archivo de configuración, y edítelo en un editor de texto.

```
$ cp config.example.toml config.toml
$ nano config.toml
```

Finalmente, ejecute el servidor web y la cola con los siguientes comandos.

```
$ poetry run flask --app reporteao run &
$ poetry run huey_consumer.py reporteao.email.cola
```

### Nix

Instale [Nix](https://nixos.org) en su servidor, y entre a la consola de desarrollo.

```
$ nix develop
```

Copie el archivo de configuración, y edítelo en un editor de texto.

```
$ cp config.example.toml config.toml
$ nano config.toml
```

Finalmente, ejecute el servidor web y la cola con los siguientes comandos.

```
$ flask --app reporteao run &
$ huey_consumer.py reporteao.email.cola
```
