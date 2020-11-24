# Gaze-and-Expertise

Find out the correlation between gaze pattern and domain expertise of the reader

**Version:** 0.0.0

## Getting up and running

Minimum requirements: **pip, python3.7 & [PostgreSQL 11][install-postgres]**, setup is tested on Mac OSX only.

```
brew install postgres python3
```

[install-postgres]: http://www.gotealeaf.com/blog/how-to-install-postgresql-on-a-mac

In your terminal, type or copy-paste the following:

    git clone git@github.com:Astruj/Gaze-and-Expertise.git; cd Gaze-and-Expertise/website; make install

Go grab a cup of coffee, we bake your hot development machine.

Useful commands:

- `make install` - Install and setup project dependencies
- `make djrun` - start [django server](http://localhost:8000/)
- `make djmigrate` - Run Django migrations
- `make djmm` - Create Django migrations
- `make help` - Display help commandss

**NOTE:** Checkout `Makefile` for all the options available and how they do it.

## Contributing

Golden Rule:

> Anything in **master** is always **deployable**.

Avoid working on `master` branch, create a new branch with meaningful name, send pull request asap. Be vocal!
