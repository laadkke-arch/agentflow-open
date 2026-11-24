/* Probe the app-style public API without loading application or GTK widgets. */
#include <libintl.h>
#include <locale.h>
#include <stdio.h>
#include <string.h>

/* GLib's stable C ABI. The runtime soname is available without SDK headers. */
extern const char *g_dpgettext2(const char *domain, const char *context, const char *msgid);

int main(int argc, char **argv)
{
    const char *result;

    if (argc != 6 || !setlocale(LC_ALL, "")) {
        fputs("expected LOCALE_ROOT DOMAIN MODE CONTEXT MSGID and an installed locale\n", stderr);
        return 2;
    }

    if (!bindtextdomain(argv[2], argv[1]) ||
        !bind_textdomain_codeset(argv[2], "UTF-8")) {
        return 3;
    }

    if (strcmp(argv[3], "ambient") == 0) {
        /* A fresh process has the standard default domain ("messages"). */
        result = gettext(argv[5]);
    } else if (!textdomain(argv[2])) {
        return 3;
    } else if (strcmp(argv[3], "plain") == 0) {
        result = gettext(argv[5]);
    } else {
        result = g_dpgettext2(NULL, argv[4], argv[5]);
    }

    if (!result || fputs(result, stdout) < 0) {
        return 4;
    }
    return 0;
}
