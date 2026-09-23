# Keep this runtime aligned with both web images. The Debian/glibc variant avoids
# the Alpine musl pwritev2 path rejected by older container hosts.
FROM nginx:1.31.6-trixie
