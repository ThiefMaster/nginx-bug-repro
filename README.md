# nginx bug?

I'm using nginx and x-accel-redirect in what's probably a slightly creative way to proxy file downloads from S3 in order to not show the very ugly and temporary S3 URL to my users. This works fine, but I noticed that in a few very rare cases the requests fail (usually due to an invalid S3 signature).

In any case, I managed to reproduce it without S3 and it seem to happen because depending on whether the URL the user accesses contains url-encoded charaters or not, the URL encoding behavior in the internal request changes.

This is a problem of course, because it means I cannot reliable know whether I need to URL-encode the path included in my x-accel-redirect header or not unless I use a horrible workaround of checking whether the current request url contains a `%` character.

I believe this behavior is so strange that it can only be a bug, but if there are any workarounds to get consistent behavior (so I can either always url-encode the path in my x-accel-redirect header or never do so) please let me know.

This is a minimal test case to reproduce this. The nginx version used originally was the one that's stable on my Gentoo system, but I'm also including a Dockerfile which can be used to test against the `nginx:latest` image on Docker hub:

```
docker build . -t nginx-bug-repro && docker run -p 8000:8000 nginx-bug-repro
```
