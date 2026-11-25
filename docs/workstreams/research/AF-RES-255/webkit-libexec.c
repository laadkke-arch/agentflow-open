/* Resolve Debian WebKitGTK's auxiliary programs and bundle in the unpacked package. */
#include <dlfcn.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct _GSubprocess GSubprocess;
typedef struct _GSubprocessLauncher GSubprocessLauncher;
typedef struct _GError GError;
typedef struct _GModule GModule;
typedef GSubprocess *(*spawn_fn)(GSubprocessLauncher *, const char *const *, GError **);
typedef GModule *(*module_open_fn)(const char *, int);

GSubprocess *g_subprocess_launcher_spawnv(GSubprocessLauncher *launcher,
                                          const char *const *argv, GError **error)
{
    spawn_fn original = (spawn_fn)dlsym(RTLD_NEXT, "g_subprocess_launcher_spawnv");
    if (!original) abort();

    const char compiled_dir[] = "/usr/lib/x86_64-linux-gnu/webkit2gtk-4.1/";
    const char *unpacked_dir = getenv("AF255_WEBKIT_LIBEXEC");
    if (!argv || !argv[0] || !unpacked_dir || strncmp(argv[0], compiled_dir, sizeof(compiled_dir) - 1))
        return original(launcher, argv, error);

    const char *name = argv[0] + sizeof(compiled_dir) - 1;
    if (strcmp(name, "WebKitWebProcess") && strcmp(name, "WebKitNetworkProcess") && strcmp(name, "WebKitGPUProcess"))
        return original(launcher, argv, error);

    size_t count = 0;
    while (argv[count]) count++;
    const char *rewritten[count + 1];
    char path[strlen(unpacked_dir) + strlen(name) + 2];
    snprintf(path, sizeof(path), "%s/%s", unpacked_dir, name);
    memcpy(rewritten, argv, (count + 1) * sizeof(*argv));
    rewritten[0] = path;
    fprintf(stderr, "AF-RES-255 WebKit libexec %s\n", path);
    return original(launcher, rewritten, error);
}

GModule *g_module_open(const char *filename, int flags)
{
    module_open_fn original = (module_open_fn)dlsym(RTLD_NEXT, "g_module_open");
    if (!original) abort();
    const char compiled_bundle[] = "/usr/lib/x86_64-linux-gnu/webkit2gtk-4.1/injected-bundle/libwebkit2gtkinjectedbundle.so";
    const char suffix[] = "/injected-bundle/libwebkit2gtkinjectedbundle.so";
    const char *unpacked_dir = getenv("AF255_WEBKIT_LIBEXEC");
    if (!filename || !unpacked_dir || strcmp(filename, compiled_bundle))
        return original(filename, flags);

    char path[strlen(unpacked_dir) + sizeof(suffix)];
    snprintf(path, sizeof(path), "%s%s", unpacked_dir, suffix);
    fprintf(stderr, "AF-RES-255 WebKit bundle %s\n", path);
    return original(path, flags);
}
