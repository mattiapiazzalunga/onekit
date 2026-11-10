/* Copyright 2026 Mattia Piazzalunga
 * SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0
 * Freestanding Linux/i386 helper, used only inside the isolated browser VM.
 * Never execute on an authoring machine: changing its clock is not a build step.
 * argv[1] names a fresh /jobs/<id> directory for each invocation. Reusing paths
 * would permit stale guest page-cache reads after a host-side 9p replacement.
 * host-clock.bin: signed 64-bit Unix seconds, then signed 64-bit nanoseconds, LE.
 * seed.bin: 32 fresh bytes supplied by host WebCrypto before each restored job.
 */
static int syscall3(int number, int a, int b, int c) {
    int result;
    __asm__ volatile("int $0x80" : "=a"(result)
        : "a"(number), "b"(a), "c"(b), "d"(c) : "memory");
    return result;
}

static int read_exact(const char *name, void *bytes, int length) {
    int file = syscall3(5, (int)name, 0, 0);
    if (file < 0) return -1;
    int offset = 0;
    while (offset < length) {
        int count = syscall3(3, file, (int)bytes + offset, length - offset);
        if (count <= 0) break;
        offset += count;
    }
    syscall3(6, file, 0, 0);
    return offset == length ? 0 : -1;
}

void refresh_main(int *stack) {
    struct { long long seconds, nanos; } clock = {0, 0};
    struct { int entropy, length; unsigned char bytes[32]; } pool = {256, 32, {0}};
    int result = 1;
    char clock_path[128], seed_path[128];
    char *directory = stack[0] == 2 ? ((char **)(stack + 1))[1] : (char *)0;
    int length = 0, valid = directory != (char *)0;
    const char *prefix = "/jobs/";
    while (valid && directory[length]) {
        char value = directory[length];
        if (length >= 100 || (length < 6 ? value != prefix[length]
                : !((value >= 'a' && value <= 'z') || (value >= 'A' && value <= 'Z')
                    || (value >= '0' && value <= '9') || value == '_' || value == '-'))) {
            valid = 0; break;
        }
        clock_path[length] = seed_path[length] = value;
        length++;
    }
    const char *clock_name = "/host-clock.bin", *seed_name = "/seed.bin";
    for (int index = 0; index < 16; index++) clock_path[length + index] = clock_name[index];
    for (int index = 0; index < 10; index++) seed_path[length + index] = seed_name[index];
    if (valid && length > 6 && read_exact(clock_path, &clock, sizeof(clock)) == 0
            && clock.seconds >= 0 && clock.nanos >= 0 && clock.nanos < 1000000000
            && read_exact(seed_path, pool.bytes, 32) == 0
            && syscall3(404, 0, (int)&clock, 0) == 0) { /* clock_settime64(CLOCK_REALTIME) */
        int random = syscall3(5, (int)"/dev/random", 2, 0);
        if (random >= 0) {
            result = syscall3(54, random, 0x40085203, (int)&pool) == 0 ? 0 : 1;
            syscall3(6, random, 0, 0);
        }
    }
    syscall3(1, result, 0, 0);
    for (;;) {}
}

/* Preserve the initial argc/argv before the C function prologue changes ESP. */
__asm__(".global _start\n_start:\nmov %esp,%eax\nand $-16,%esp\nsub $12,%esp\n"
        "push %eax\ncall refresh_main\n1: jmp 1b\n");
