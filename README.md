
> ⚠️ This repository has moved! 
> It is now hosted on Codeberg:  
> **[https://codeberg.org/mitlinks-it/karlsunruh-importer](https://codeberg.org/mitlinks-it/karlsunruh-importer)**
> 
> All future development, issues, and pull requests will be handled on Codeberg.  
> This GitHub repository is archived and will no longer be maintained.
 

# Karlsunruh-Importer

A Python-based tool designed to automate the import of event data into [karlsunruh.org](https://karlsunruh.org).

Various event sources can be integrated by implementing a shared interface.
To add a new source, implement the `EventSource` interface in the `src/sources` directory.
Imports are executed regularly via cron-scheduled GitHub Actions.
