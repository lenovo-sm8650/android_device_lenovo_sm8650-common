#!/usr/bin/env -S PYTHONPATH=../../../tools/extract-utils python3
#
# SPDX-FileCopyrightText: 2026 The LineageOS Project
# SPDX-License-Identifier: Apache-2.0
#

from extract_utils.fixups_blob import (
    blob_fixup,
    blob_fixups_user_type,
)
from extract_utils.fixups_lib import (
    lib_fixups,
    lib_fixups_user_type,
)
from extract_utils.main import (
    ExtractUtils,
    ExtractUtilsModule,
)

namespace_imports = [
    'device/lenovo/sm8650-common',
    'hardware/qcom-caf/sm8650',
    'hardware/qcom-caf/wlan',
    'vendor/qcom/opensource/commonsys/display',
    'vendor/qcom/opensource/commonsys-intf/display',
    'vendor/qcom/opensource/dataservices',
]


def lib_fixup_vendor_suffix(lib: str, partition: str, *args, **kwargs):
    return f'{lib}_{partition}' if partition == 'vendor' else None


lib_fixups: lib_fixups_user_type = {
    **lib_fixups,
    (
        'com.qualcomm.qti.dpm.api@1.0',
        'vendor.qti.diaghal@1.0',
        'vendor.qti.hardware.dpmaidlservice-V1-ndk',
        'vendor.qti.hardware.dpmservice@1.0',
        'vendor.qti.hardware.qccsyshal@1.0',
        'vendor.qti.hardware.qccsyshal@1.1',
        'vendor.qti.hardware.qccsyshal@1.2',
        'vendor.qti.hardware.wifidisplaysession@1.0',
        'vendor.qti.qccvndhal_aidl-V1-ndk',
    ): lib_fixup_vendor_suffix,
}


def clear_opencl_versions(fixup):
    # Lenovo camera algorithm libs reference OpenCL symbols with OPENCL_x.y
    # versions, but the Adreno libOpenCL exports them unversioned.
    for symbol in OPENCL_SYMBOLS:
        fixup = fixup.clear_symbol_version(symbol)
    return fixup


def clear_nativewindow_versions(fixup):
    # AHardwareBuffer symbols are referenced as @LIBNATIVEWINDOW, but the
    # vendor libnativewindow stub exports them unversioned.
    for symbol in NATIVEWINDOW_SYMBOLS:
        fixup = fixup.clear_symbol_version(symbol)
    return fixup


NATIVEWINDOW_SYMBOLS = (
    'AHardwareBuffer_allocate',
    'AHardwareBuffer_describe',
    'AHardwareBuffer_lock',
    'AHardwareBuffer_lockPlanes',
    'AHardwareBuffer_release',
    'AHardwareBuffer_unlock',
)


OPENCL_SYMBOLS = (
    'clBuildProgram',
    'clCreateBuffer',
    'clCreateCommandQueue',
    'clCreateCommandQueueWithProperties',
    'clCreateContext',
    'clCreateKernel',
    'clCreateProgramWithBinary',
    'clCreateProgramWithSource',
    'clEnqueueCopyBuffer',
    'clEnqueueFillBuffer',
    'clEnqueueMapBuffer',
    'clEnqueueNDRangeKernel',
    'clEnqueueReadBuffer',
    'clEnqueueUnmapMemObject',
    'clFinish',
    'clGetDeviceIDs',
    'clGetDeviceInfo',
    'clGetExtensionFunctionAddressForPlatform',
    'clGetPlatformIDs',
    'clGetPlatformInfo',
    'clGetProgramBuildInfo',
    'clGetProgramInfo',
    'clReleaseCommandQueue',
    'clReleaseContext',
    'clReleaseKernel',
    'clReleaseMemObject',
    'clReleaseProgram',
    'clSetKernelArg',
)

# libar-pal (Lenovo): the Awinic smart PA code writes the speaker calibration
# (Re) and voltage offsets to the ADSP when the speaker device starts, before
# its playback graph runs, so it never finds the speaker protection module
# and every write fails; its monitor thread, which could retry, is off
# (monitor time 0). Wake the monitor thread on every start and make it write
# the calibration again 0.5, 1 and 1.5 s later, once the graph runs. The
# code replaces the per-device monitor loop, unused with monitor time 0
# (see tools/awinic_cali.S).
LIBAR_PAL_MONITOR_START = (
    '08 01 00 d0 08 85 47 b9 88 01 00 34 00 e4 00 6f',  # cbz w8 (monitor time 0)
    '08 01 00 d0 08 85 47 b9 1f 20 03 d5 00 e4 00 6f',  # nop
)
LIBAR_PAL_MONITOR_THREAD = (
    '68 1a 40 b9 bf 43 1f b8 ff 13 00 b9 1f 05 00 71 8b 08 00 54 fa 03 1f aa 05 00 00 14 68 1a 80 b9',
    ''.join((
    '68 1e 40 b9 1f 0d 00 71 c1 03 00 54 88 00 80 52 '
    '68 1e 00 b9 e0 03 14 aa 6e 34 00 94 7a 00 80 52 '
    '00 24 94 52 e0 00 a0 72 be 16 00 94 ff 03 01 d1 '
    'e0 43 00 91 c1 00 80 52 00 22 00 94 a0 01 f8 37 '
    'a8 00 00 d0 08 b9 44 f9 08 01 40 f9 e8 1b 00 f9 '
    'a8 00 00 d0 08 bd 44 f9 08 01 40 f9 e8 1f 00 f9 '
    'e0 c3 00 91 e1 43 00 91 c2 00 80 52 f9 21 00 94 '
    'ff 03 01 91 5a 07 00 71 41 fd ff 54 d2 ff ff 17 '
    '28 00 00 14 1f 20 03 d5 1f 20 03 d5 1f 20 03 d5 '
    '1f 20 03 d5 1f 20 03 d5 1f 20 03 d5 1f 20 03 d5 '
    '1f 20 03 d5 1f 20 03 d5 1f 20 03 d5 1f 20 03 d5 '
    '1f 20 03 d5 1f 20 03 d5 1f 20 03 d5 1f 20 03 d5 '
    '1f 20 03 d5 1f 20 03 d5 1f 20 03 d5 1f 20 03 d5 '
    '1f 20 03 d5 1f 20 03 d5 1f 20 03 d5 1f 20 03 d5 '
    '1f 20 03 d5 1f 20 03 d5 1f 20 03 d5 1f 20 03 d5 '
    '1f 20 03 d5 1f 20 03 d5 1f 20 03 d5 1f 20 03 d5 '
    '1f 20 03 d5 1f 20 03 d5 1f 20 03 d5 1f 20 03 d5 '
    '1f 20 03 d5 1f 20 03 d5 1f 20 03 d5 1f 20 03 d5 '
    )).strip(),
)

blob_fixups: blob_fixups_user_type = {
    'vendor/lib64/libar-pal.so': blob_fixup()
        .sig_replace(*LIBAR_PAL_MONITOR_START)
        .sig_replace(*LIBAR_PAL_MONITOR_THREAD),
    'system_ext/lib64/vendor.qti.hardware.qccsyshal@1.2-halimpl.so': blob_fixup()
        .replace_needed('libprotobuf-cpp-full.so', 'libprotobuf-cpp-full-21.7.so'),
    (
        'vendor/bin/qcc-vendor',
        'vendor/lib64/libqcc_sdk.so',
    ): blob_fixup()
        .add_needed('libbinder_shim.so'),
    (
        'vendor/etc/media_codecs_cliffs_v0.xml',
        'vendor/etc/media_codecs_cliffs_v1.xml',
        'vendor/etc/media_codecs_pineapple.xml',
    ): blob_fixup()
        .regex_replace('.*media_codecs_(google_audio|google_c2|google_telephony|google_video|vendor_audio).*\n', ''),
    (
        'vendor/etc/seccomp_policy/qesdksec.policy',
        'vendor/etc/seccomp_policy/qsap_qapeservice.policy',
    ): blob_fixup()
        .add_line_if_missing('lseek: 1'),
    'vendor/lib64/libqcodec2_core.so': blob_fixup()
        .add_needed('libcodec2_shim.so'),
    (
        'vendor/bin/hw/vendor.qti.hardware.display.composer-service',
        'vendor/lib64/libaodoptfeature.so',
        'vendor/lib64/libapengine.so',
        'vendor/lib64/libdpps.so',
        'vendor/lib64/libgamepoweroptfeature.so',
        'vendor/lib64/liblearningmodule.so',
        'vendor/lib64/liboffscreenpoweroptfeature.so',
        'vendor/lib64/libpowercore.so',
        'vendor/lib64/libpsmoptfeature.so',
        'vendor/lib64/libsnapdragoncolor-manager.so',
        'vendor/lib64/libstandbyfeature.so',
        'vendor/lib64/libvideooptfeature.so',
    ): blob_fixup()
        .replace_needed('libtinyxml2.so', 'libtinyxml2-v34.so'),
    (
        'vendor/lib64/libVoiceSdk.so',
        'vendor/lib64/libcapiv2uvvendor.so',
        'vendor/lib64/liblistensoundmodel2vendor.so',
    ): blob_fixup()
        .replace_needed('libtensorflowlite_c.so', 'libtensorflowlite_c_vendor.so'),
}  # fmt: skip

module = ExtractUtilsModule(
    'sm8650-common',
    'lenovo',
    blob_fixups=blob_fixups,
    lib_fixups=lib_fixups,
    namespace_imports=namespace_imports,
)

if __name__ == '__main__':
    utils = ExtractUtils.device(module)
    utils.run()
