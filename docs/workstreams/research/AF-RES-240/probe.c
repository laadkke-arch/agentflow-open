/* Raw public ICU4C 76.1 calls for names, plus a separate time-zone comparison. */
#include <inttypes.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unicode/icudataver.h>
#include <unicode/putil.h>
#include <unicode/uchar.h>
#include <unicode/ucal.h>
#include <unicode/ulocdata.h>
#include <unicode/ustring.h>
#include <unicode/utypes.h>
#include <unicode/uversion.h>

#define CAPACITY 256

static const UCharNameChoice choices[] = {
    U_UNICODE_CHAR_NAME, U_CHAR_NAME_ALIAS, U_EXTENDED_CHAR_NAME
};
static const char *const choice_names[] = {
    "U_UNICODE_CHAR_NAME", "U_CHAR_NAME_ALIAS", "U_EXTENDED_CHAR_NAME"
};

static void print_version(const char *name, const UVersionInfo version) {
    char text[U_MAX_VERSION_STRING_LENGTH];
    u_versionToString(version, text);
    printf("# %s=%s (%u,%u,%u,%u)\n", name, text,
           version[0], version[1], version[2], version[3]);
}

static int validate_versions(void) {
    UVersionInfo library, unicode, data = {0};
    UErrorCode status = U_ZERO_ERROR;
    u_getVersion(library);
    u_getUnicodeVersion(unicode);
    u_getDataVersion(data, &status);
    printf("# compile_header=%s\n# u_getDataDirectory=%s\n",
           U_ICU_VERSION, u_getDataDirectory());
    print_version("u_getVersion", library);
    print_version("u_getUnicodeVersion", unicode);
    print_version("u_getDataVersion", data);
    printf("# u_getDataVersion_status=%d:%s\n", (int)status, u_errorName(status));
    if (strcmp(U_ICU_VERSION, "76.1") != 0 ||
        library[0] != 76 || library[1] != 1 || library[2] != 0 || library[3] != 0 ||
        unicode[0] != 16 || unicode[1] != 0 || unicode[2] != 0 || unicode[3] != 0 ||
        data[0] != 76 || data[1] != 1 || data[2] != 0 || data[3] != 0 ||
        U_FAILURE(status)) {
        fputs("Wrong header, runtime or data version\n", stderr);
        return 1;
    }
    return 0;
}

static void print_hex(const char *bytes, size_t length) {
    for (size_t index = 0; index < length; index++) {
        printf("%02x", (unsigned int)(unsigned char)bytes[index]);
    }
}

static int probe_name(const char *repeat, char *line) {
    char *fields[4] = {line};
    for (size_t index = 1; index < 4; index++) {
        char *tab = strchr(fields[index - 1], '\t');
        if (tab == NULL) {
            return 1;
        }
        *tab = '\0';
        fields[index] = tab + 1;
    }
    const char *id = fields[0];
    char *end;
    long number = strtol(fields[1], &end, 16);
    if (end == fields[1] || *end || number < 0 || number > 0x10ffff) {
        return 1;
    }
    UChar32 cp = (UChar32)number;
    const char *operation = fields[2];
    const char *input = fields[3];
    int lookup = strcmp(operation, "lookup") == 0;
    int32_t capacity = CAPACITY;
    if (strcmp(operation, "name-cap1") == 0) {
        capacity = 1;
    } else if (strcmp(operation, "name-capexact") == 0) {
        capacity = (int32_t)sizeof("LATIN CAPITAL LETTER OI") - 1;
    } else if (!lookup && strcmp(operation, "name") != 0) {
        return 1;
    }
    for (size_t index = 0; index < sizeof(choices) / sizeof(choices[0]); index++) {
        UErrorCode status = U_ZERO_ERROR;
        char buffer[CAPACITY];
        memset(buffer, 0x7e, sizeof(buffer));
        int32_t result = lookup ? u_charFromName(choices[index], input, &status)
                                : u_charName(cp, choices[index], buffer, capacity, &status);
        printf("%s\t%s\t%04" PRIX32 "\t%s\t%s\t%d\t%s\t", repeat, id, (uint32_t)cp,
               operation, choice_names[index], choices[index], input);
        print_hex(input, strlen(input));
        printf("\t%" PRId32 "\t", result);
        if (lookup) {
            printf("%04" PRIX32, (uint32_t)result);
        }
        printf("\t%d\t%s\t%d\t%d\t0\t", (int)status, u_errorName(status),
               U_SUCCESS(status), U_FAILURE(status));
        if (lookup) {
            printf("\t\t\t\n");
            continue;
        }
        const char *nul = memchr(buffer, '\0', (size_t)capacity);
        int length = nul ? (int)(nul - buffer) : capacity;
        printf("%" PRId32 "\t%d\t%.*s\t", capacity, nul ? length : -1, length, buffer);
        print_hex(buffer, (size_t)(length + (nul != NULL)));
        putchar('\n');
    }
    return 0;
}

static int probe_names(const char *repeat) {
    char line[512];
    puts("repeat\tinput_id\tcode_point\toperation\tchoice\tchoice_num\tinput\tinput_ascii_hex\treturn"
         "\treturn_hex\tstatus\tstatus_name\tu_success\tu_failure\tpre_status\tbuffer_capacity"
         "\tnul_index\tbuffer_text\tbuffer_hex");
    while (fgets(line, sizeof(line), stdin)) {
        line[strcspn(line, "\r\n")] = '\0';
        if (probe_name(repeat, line)) {
            fputs("Invalid probe input row\n", stderr);
            return 1;
        }
    }
    return ferror(stdin) != 0;
}

static void probe_zones(void) {
    const char *const keys[] = {"US/Eastern", "America/New_York",
                                "Asia/Calcutta", "Asia/Kolkata", "Invalid/AF_RES_240"};
    UVersionInfo cldr = {0};
    UErrorCode status = U_ZERO_ERROR;
    const char *tz_version = ucal_getTZDataVersion(&status);
    printf("# tzdata=%s status=%s\n", tz_version ? tz_version : "", u_errorName(status));
    status = U_ZERO_ERROR;
    ulocdata_getCLDRVersion(cldr, &status);
    print_version("cldr", cldr);
    printf("# cldr_status=%s\n", u_errorName(status));
    puts("input\tcanonical\tcanonical_length\tis_system_id\tcanonical_status"
         "\tiana\tiana_status\topen_status\treturned_id\tid_length\tid_status");
    for (size_t index = 0; index < sizeof(keys) / sizeof(keys[0]); index++) {
        UChar key[CAPACITY], out[CAPACITY] = {0};
        char canonical[CAPACITY] = {0}, id[CAPACITY] = {0};
        UBool is_system_id = 0;
        u_uastrcpy(key, keys[index]);

        status = U_ZERO_ERROR;
        int32_t n = ucal_getCanonicalTimeZoneID(key, -1, out, CAPACITY, &is_system_id, &status);
        if (U_SUCCESS(status) && n >= 0 && n < CAPACITY) {
            u_austrcpy(canonical, out);
        }
        printf("%s\t%s\t%" PRId32 "\t%d\t%s\t", keys[index], canonical, n, is_system_id,
               u_errorName(status));

        status = U_ZERO_ERROR;
        memset(out, 0, sizeof(out));
        n = ucal_getIanaTimeZoneID(key, -1, out, CAPACITY, &status);
        if (U_SUCCESS(status) && n >= 0 && n < CAPACITY) {
            u_austrcpy(id, out);
        }
        printf("%s\t%s\t", id, u_errorName(status));
        id[0] = '\0';

        status = U_ZERO_ERROR;
        UCalendar *calendar = ucal_open(key, -1, "en_US", UCAL_GREGORIAN, &status);
        printf("%s\t", u_errorName(status));
        if (calendar == NULL || U_FAILURE(status)) {
            puts("\t\t");
        } else {
            status = U_ZERO_ERROR;
            memset(out, 0, sizeof(out));
            n = ucal_getTimeZoneID(calendar, out, CAPACITY, &status);
            if (U_SUCCESS(status) && n >= 0 && n < CAPACITY) {
                u_austrcpy(id, out);
            }
            printf("%s\t%" PRId32 "\t%s\n", id, n, u_errorName(status));
        }
        if (calendar != NULL) {
            ucal_close(calendar);
        }
    }
}

int main(int argc, char **argv) {
    if (argc != 2 || (strcmp(argv[1], "1") && strcmp(argv[1], "2") && strcmp(argv[1], "tz"))) {
        fprintf(stderr, "Usage: %s 1|2|tz (name cases as TSV on stdin)\n", argv[0]);
        return 64;
    }
    if (validate_versions()) {
        return 2;
    }
    if (strcmp(argv[1], "tz") == 0) {
        probe_zones();
        return 0;
    }
    return probe_names(argv[1]);
}
