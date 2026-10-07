// SPDX-FileCopyrightText: 2026 The LineageOS Project
// SPDX-License-Identifier: Apache-2.0
//
// Awinic calibration retry for the Lenovo libar-pal.so (vendor/lib64,
// sha1 fc9703f60480d102a046c99bf2183e0565188bf5), applied by the
// LIBAR_PAL_MONITOR_THREAD fixup in extract-files.py. To rebuild it:
//
//   clang --target=aarch64-linux-android -c awinic_cali.S -o cali.o
//   ld.lld -Ttext=0x3a8040 -e _start cali.o -o cali.elf
//       --defsym=pthread_mutex_unlock=0x3b5210 --defsym=usleep=0x3adb60
//       --defsym=aw_audioreach_get_re_from_file=0x3b0878
//       --defsym=aw_audioreach_dsp_set_re=0x3b0890
//       --defsym=virt_got=0x3be970 --defsym=hw_got=0x3be978
//       --defsym=relock=0x3a8004 --defsym=tail=0x3a8160
//   llvm-objcopy -O binary --only-section=.text cali.elf cali.bin
//
// and pad it with nops to 0x3a8160.
//
// Replaces the per-device monitor loop of the Awinic monitor thread
// (libar-pal.so 0x3a8040..0x3a815f). Entered with the monitor mutex (x20)
// held, x19 = monitor context, state at [x19, #0x1c].
    .text
    .global _start
_start:
    ldr     w8, [x19, #0x1c]
    cmp     w8, #3                  // started?
    b.ne    out
    mov     w8, #4                  // consume the start
    str     w8, [x19, #0x1c]
    mov     x0, x20
    bl      pthread_mutex_unlock
    mov     w26, #3                 // tries, 0.5 s apart
try:
    mov     w0, #0xa120
    movk    w0, #0x7, lsl #16       // 500000 us
    bl      usleep
    sub     sp, sp, #0x40
    add     x0, sp, #0x10           // int re[6]
    mov     w1, #6
    bl      aw_audioreach_get_re_from_file
    tbnz    w0, #31, fail
    adrp    x8, virt_got
    ldr     x8, [x8, :lo12:virt_got]
    ldr     x8, [x8]
    str     x8, [sp, #0x30]         // SpeakerProtection::virtMixer
    adrp    x8, hw_got
    ldr     x8, [x8, :lo12:hw_got]
    ldr     x8, [x8]
    str     x8, [sp, #0x38]         // SpeakerProtection::hwMixer
    add     x0, sp, #0x30
    add     x1, sp, #0x10
    mov     w2, #6
    bl      aw_audioreach_dsp_set_re
fail:
    add     sp, sp, #0x40
    subs    w26, w26, #1
    b.ne    try
    b       relock                  // lock again; waits for the next start
out:
    b       tail                    // unlock, usleep, loop (original path)
