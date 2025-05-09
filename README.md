# Karlsunruh-Importer

A Python-based tool designed to automate the import of event data into [karlsunruh.org](https://karlsunruh.org).

Various event sources can be integrated by implementing a shared interface.
To add a new source, implement the `EventSource` interface in the `src/sources` directory.
Imports are executed regularly via cron-scheduled GitHub Actions.
