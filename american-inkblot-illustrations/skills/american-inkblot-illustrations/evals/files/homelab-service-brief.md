# Homelab notes service

A browser reaches `notes.example.test` over HTTPS. Caddy terminates TLS and
forwards HTTP requests over loopback to a notes app on port 4310. The notes app
reads and writes a SQLite database at `/srv/notes/notes.db` and stores uploaded
files under `/srv/notes/uploads/`.

launchd starts Caddy and the notes app at login and restarts the app when it
exits. A health checker requests `/health` every five minutes and writes a local
failure log. A nightly job copies the database and uploads directory to an
encrypted backup destination. The backup job is configured, but the supplied
brief contains no recent successful backup result.

Do not expose the private hostname, absolute data paths, or port number in the
generated image. They may appear in local companion notes when needed.
