# Setup Media IP and Hantro

Media IP is a new hardware feature firstly introduced on GNR-D. Hantro is the User Mode Driver. In GNR-D SKUs that contain multiple QAT 2.2 devices, they can be configured to provide either CPM (Content Processing Module) services or Media services.

## System Setup

> To be updated with newer BKC [Release Notes Intel® GNR-D Media 1.1 Alpha][Release Notes Intel® GNR-D Media 1.1 Alpha] and Media IP release driver package [BKC 2024ww16][BKC 2024ww16].

- Platform: GNR-D
- BKC version: 2023ww18
- BKC release note: [BKC realease note][BKC realease note]
- Operating System: CentOS Stream 8
- Kernel: Linux 5.19.0-gnr.po.bkc.7.2.21.x86_64
- Media driver version: GNR-D_Development_12

Download the Media driver from [Artifactory GNR-D_Development_12][Artifactory GNR-D_Development_12] and the install script from [Artifactory Install Script][Artifactory Install Script], then copy them to the worker node.

```bash
$ tar xzvf GNR-D_Development_12.tgz && cd GNR-D_Development_12
# Copy the install script into the package
$ cp ../install_mediaip_dev_12.sh . && chmod a+x install_mediaip_dev_12.sh && ls
ffmpeg  GStreamer  haps  install_mediaip_dev_12.sh  install.sh  metadata  metal  setenv.sh  simics  src  usr
$ source setenv.sh
# Install on baremetal with aux driver in WQM mode
$ sudo ./install_mediaip_dev_12.sh metal aux wqm
...
+ /home/media/GNR-D_Development_12/usr/local/bin/vainfo --display drm --device /dev/dri/renderD128
Trying display: drm
libva info: VA-API version 1.20.0
libva info: User environment variable requested driver 'hantro'
libva info: Trying to open /home/media/GNR-D_Development_12/metal/drv/hantro_drv_video.so
libva info: Found init function __vaDriverInit_1_0
[0x7f1c15171000: check_global_env]:---Getting global env---
[0x7f1c15171000: check_global_env]:  Output log level, VA_UMD_LOG_LEVEL = 4
[0x7f1c15171000: check_global_env]:  Dump cmdbuf, VA_DUMP_CMDBUF = 0
[0x7f1c15171000: check_global_env]:  Shared Virtual Memory, VA_USE_SVM = 0, SVM disabled
[0x7f1c15171000: check_global_env]:  UQ/WQ selection, VA_USE_WQM = 1, Using WQM
[0x7f1c15171000: check_global_env]:  UMD version is ea5d85f
[0x7f1c15171000: check_global_env]:------------------------
[0x7f1c15171000: init_cmdbuf]:Create global command buffer...
[0x7f1c15171000: create_cmdbuf]:cmdbuf 0xf6600000/0x7f1c14e2e000, status cmdbuf 0xf6400000/0x7f1c13800000
[0x7f1c15171000: drm_hantro_bufmgr_open]:Creating cmdbuf wait thread 139758562965248
libva info: va_openDriver() returns 0
vainfo: VA-API version: 1.20 (libva 2.20.0.pre1)
vainfo: Driver version: Intel VID driver for GNR  - 1.0.0
vainfo: Supported profile and entrypoints
      VAProfileH264ConstrainedBaseline: VAEntrypointVLD
      VAProfileH264ConstrainedBaseline: VAEntrypointEncSlice
      VAProfileH264ConstrainedBaseline: VAEntrypointEncSliceLP
      VAProfileH264Main               : VAEntrypointVLD
      VAProfileH264Main               : VAEntrypointEncSlice
      VAProfileH264Main               : VAEntrypointEncSliceLP
      VAProfileH264High               : VAEntrypointVLD
      VAProfileH264High               : VAEntrypointEncSlice
      VAProfileH264High               : VAEntrypointEncSliceLP
      VAProfileH264High10             : VAEntrypointVLD
      VAProfileH264High10             : VAEntrypointEncSlice
      VAProfileH264High10             : VAEntrypointEncSliceLP
      VAProfileNone                   : VAEntrypointVideoProc
      VAProfileJPEGBaseline           : VAEntrypointVLD
      VAProfileJPEGBaseline           : VAEntrypointEncPicture
      VAProfileHEVCMain               : VAEntrypointVLD
      VAProfileHEVCMain               : VAEntrypointEncSlice
      VAProfileHEVCMain               : VAEntrypointEncSliceLP
      VAProfileHEVCMain10             : VAEntrypointVLD
      VAProfileHEVCMain10             : VAEntrypointEncSlice
      VAProfileHEVCMain10             : VAEntrypointEncSliceLP
      VAProfileAV1Profile0            : VAEntrypointEncSlice
[0x7f1c15171000: drm_hantro_bufmgr_destroy]:Shutdown thread 139758562965248
[0x7f1c15171000: deinit_cmdbuf]:Destroy global command buffer...
[0x7f1c15171000: hantro_Terminate]:hantro 0x409ac0, surface created/destroyed 0/0

+ '[' 0 -eq 0 ']'
+ echo 'vainfo test pass with wqm.'
vainfo test pass with wqm.
```

Then check the device with:

```bash
$ ls /dev/dri/
by-path  card0  renderD128

$ lspci |grep 4946
01:00.0 Co-processor: Intel Corporation Device 4946
05:00.0 Co-processor: Intel Corporation Device 4946
```

## Node Labels

Add the following node label on the worker node:

- `HAS-SETUP-VSI-HANTRO`: yes

## See Also

How to build & use AUX driver: [MediaIP driver guide][MediaIP driver guide]

[Artifactory GNR-D_Development_12]: https://af01p-igk.devtools.intel.com/artifactory/platform_hero-igk-local/Media/FFmpeg/GNR-D_Development_12.tgz
[Artifactory Install Script]: https://af01p-igk.devtools.intel.com/artifactory/platform_hero-igk-local/Media/FFmpeg/install_mediaip_dev_12.sh
[BKC realease note]: https://wiki.ith.intel.com/display/linuxstack/Release+Notes+2023+WW18+GNR
[MediaIP driver guide]: https://wiki.ith.intel.com/pages/viewpage.action?pageId=3074538405
[Release Notes Intel® GNR-D Media 1.1 Alpha]: https://wiki.ith.intel.com/pages/viewpage.action?pageId=3429693460
[BKC 2024ww16]: https://wiki.ith.intel.com/display/linuxstack/Release+Notes+2024+WW16+GNR