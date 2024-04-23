%global libfdt_version 1.6.0
%global libseccomp_version 2.4.0
%global libusbx_version 1.0.23
%global meson_version 0.58.2
%global usbredir_version 0.7.1
%global ipxe_version 20200823-5.git4bd064de

%ifarch x86_64
%global kvm_package   system-x86
%endif

%ifarch aarch64
%global kvm_package   system-aarch64
%endif

%ifarch riscv64
%global kvm_package   system-riscv
%endif

%global modprobe_kvm_conf %{_sourcedir}/kvm.conf
%ifarch x86_64
%global modprobe_kvm_conf %{_sourcedir}/kvm-x86.conf
%endif

%ifarch x86_64
%global have_pmem 1
%else
%global have_pmem 0
%endif

%bcond_without rbd
%bcond_with usb_redir
%bcond_with virtgl
%bcond_without opengl
%bcond_with nfs
%bcond_with extra_arch

%global _lto_cflags %{nil}

%global firmwaredirs "%{_datadir}/qemu-firmware:%{_datadir}/ipxe/qemu:%{_datadir}/seavgabios:%{_datadir}/seabios:%{_datadir}/sgabios"
%global qemudocdir %{_docdir}/%{name}
%define evr %{version}-%{release}
%define requires_block_curl Requires: %{name}-block-curl = %{evr}
%define requires_block_dmg Requires: %{name}-block-dmg = %{evr}
%define requires_block_iscsi Requires: %{name}-block-iscsi = %{evr}
%if %{with nfs}
%define requires_block_nfs Requires: %{name}-block-nfs = %{evr}
%define obsoletes_block_nfs %{nil}
%else
%define requires_block_nfs %{nil}
%define obsoletes_block_nfs Obsoletes: %{name}-block-nfs < %{evr}
%endif
%if %{with rbd}
%define requires_block_rbd Requires: %{name}-block-rbd = %{evr}
%define obsoletes_block_rbd %{nil}
%else
%define requires_block_rbd %{nil}
%define obsoletes_block_rbd Obsoletes: %{name}-block-rbd < %{evr}
%endif
%define requires_block_ssh Requires: %{name}-block-ssh = %{evr}
%define requires_audio_alsa Requires: %{name}-audio-alsa = %{evr}
%define requires_audio_oss Requires: %{name}-audio-oss = %{evr}
%define requires_audio_pa Requires: %{name}-audio-pa = %{evr}
%define requires_audio_sdl Requires: %{name}-audio-sdl = %{evr}
%define requires_device_usb_host Requires: %{name}-device-usb-host = %{evr}
%if %{with usb_redir}
%define requires_device_usb_redirect Requires: %{name}-device-usb-redirect = %{evr}
%else
%define requires_device_usb_redirect %{nil}
%endif
%define requires_device_usb_smartcard %{nil}
%define requires_ui_curses Requires: %{name}-ui-curses = %{evr}
%define requires_ui_gtk Requires: %{name}-ui-gtk = %{evr}
%define requires_ui_sdl Requires: %{name}-ui-sdl = %{evr}
%if %{with opengl}
%define requires_ui_egl_headless Requires: %{name}-ui-egl-headless = %{evr}
%define requires_ui_opengl Requires: %{name}-ui-opengl = %{evr}
%else
%define requires_ui_egl_headless %{nil}
%define requires_ui_opengl %{nil}
%endif
%define requires_device_display_virtio_gpu Requires: %{name}-device-display-virtio-gpu = %{evr}
%define requires_device_display_virtio_gpu_pci Requires: %{name}-device-display-virtio-gpu-pci = %{evr}
%define requires_device_display_virtio_gpu_ccw Requires: %{name}-device-display-virtio-gpu-ccw = %{evr}
%define requires_device_display_virtio_vga Requires: %{name}-device-display-virtio-vga = %{evr}
%define requires_device_display_virtio_vga_gl Requires: %{name}-device-display-virtio-vga-gl = %{evr}

%if %{with virtgl}
%define requires_device_display_vhost_user_gpu Requires: %{name}-device-display-vhost-user-gpu = %{evr}
%else
%define requires_device_display_vhost_user_gpu %{nil}
%endif

%define requires_audio_jack %{nil}
%define requires_ui_spice_app %{nil}
%define requires_ui_spice_core %{nil}
%define requires_device_display_qxl %{nil}
%define requires_audio_spice %{nil}
%define requires_char_spice %{nil}

%global requires_all_modules \
%{requires_block_curl} \
%{requires_block_dmg} \
%{requires_block_iscsi} \
%{requires_block_nfs} \
%{requires_block_rbd} \
%{requires_block_ssh} \
%{requires_audio_alsa} \
%{requires_audio_oss} \
%{requires_audio_pa} \
%{requires_audio_sdl} \
%{requires_audio_jack} \
%{requires_audio_spice} \
%{requires_ui_curses} \
%{requires_ui_gtk} \
%{requires_ui_sdl} \
%{requires_ui_egl_headless} \
%{requires_ui_opengl} \
%{requires_ui_spice_app} \
%{requires_ui_spice_core} \
%{requires_char_spice} \
%{requires_device_display_qxl} \
%{requires_device_display_vhost_user_gpu} \
%{requires_device_display_virtio_gpu} \
%{requires_device_display_virtio_gpu_pci} \
%{requires_device_display_virtio_vga} \
%{requires_device_display_virtio_vga_gl} \
%{requires_device_usb_host} \
%{requires_device_usb_redirect} \
%{requires_device_usb_smartcard} \

Summary: QEMU is a FAST! processor emulator
Name: qemu
Version: 8.2.2
Release: 1%{?dist}
License: GPLv2 and BSD and MIT and CC-BY
URL: http://www.qemu.org/
Source0: http://wiki.qemu-project.org/download/%{name}-%{version}.tar.xz

Source1: qemu-guest-agent.service
Source2: 99-qemu-guest-agent.rules
Source3: bridge.conf
Source4: qemu-ga.sysconfig
Source5: 95-kvm-memlock.conf
Source6: vhost.conf
Source7: kvm.conf
Source8: kvm-s390x.conf
Source9: kvm-x86.conf

Patch0007: 0007-fix-CVE-2023-3180.patch
Patch0008: CVE-2023-5088.patch
# CVE-2023-3301
# https://github.com/qemu/qemu/commit/a0d7215e339b61c7d7a7b3fcf754954d80d93eb8
Patch0009: 0008-newfeature-support-vpsp.patch

BuildRequires: meson >= %{meson_version}
BuildRequires: zlib-devel
BuildRequires: glib2-devel
BuildRequires: gnutls-devel
BuildRequires: libselinux-devel
BuildRequires: cyrus-sasl-devel
BuildRequires: libaio-devel
BuildRequires: python3-devel
BuildRequires: libiscsi-devel
BuildRequires: libattr-devel
BuildRequires: libusbx-devel >= %{libusbx_version}
%if %{with usb_redir}
BuildRequires: usbredir-devel >= %{usbredir_version}
%endif
BuildRequires: texinfo
BuildRequires: python3-sphinx
BuildRequires: python3-sphinx_rtd_theme
BuildRequires: libseccomp-devel >= %{libseccomp_version}
BuildRequires: libcurl-devel
BuildRequires: libssh-devel
%if %{with rbd}
BuildRequires: librbd-devel
%endif
BuildRequires: systemtap
BuildRequires: systemtap-sdt-devel
BuildRequires: libpng-devel
BuildRequires: libcap-ng-devel
BuildRequires: pixman-devel
BuildRequires: rdma-core-devel
BuildRequires: libfdt-devel >= %{libfdt_version}
BuildRequires: lzo-devel snappy-devel
BuildRequires: numactl-devel
BuildRequires: device-mapper-multipath-devel
BuildRequires: systemd-devel
%if %{have_pmem}
BuildRequires: libpmem-devel
%endif
BuildRequires: pkgconfig(xkbcommon)
%if %{with opengl}
BuildRequires: pkgconfig(epoxy)
BuildRequires: pkgconfig(libdrm)
BuildRequires: pkgconfig(gbm)
%endif
BuildRequires: perl-Test-Harness
BuildRequires: libbpf-devel


%if "%{toolchain}" == "clang"
BuildRequires: clang
%else
BuildRequires: gcc
%endif
BuildRequires: make
BuildRequires: SDL2-devel
BuildRequires: pulseaudio-libs-devel
BuildRequires: alsa-lib-devel
%if %{with nfs}
BuildRequires: libnfs-devel
%endif
BuildRequires: ncurses-devel
BuildRequires: libjpeg-devel
BuildRequires: gtk3-devel
BuildRequires: vte291-devel
BuildRequires: gettext
BuildRequires: bzip2-devel
BuildRequires: libtasn1-devel
%if %{with virgl}
BuildRequires: virglrenderer-devel
%endif
BuildRequires: libudev-devel
BuildRequires: pam-devel
BuildRequires: liburing-devel
BuildRequires: libzstd-devel
BuildRequires: hostname
BuildRequires: daxctl-devel
BuildRequires: fuse-devel
BuildRequires: fuse3-devel
BuildRequires: flex bison

BuildRequires: glibc-static pcre2-static glib2-static zlib-static

%ifarch aarch64
Requires: %{name}-system-aarch64 = %{version}-%{release}
%endif
%ifarch ppc64le
Requires: %{name}-system-ppc = %{version}-%{release}
%endif
%ifarch x86_64
Requires: %{name}-system-x86 = %{version}-%{release}
%endif
%ifarch riscv
Requires: %{name}-system-riscv = %{version}-%{release}
%endif
Requires: %{name}-user = %{version}-%{release}
Requires: %{name}-img = %{version}-%{release}
Requires: %{name}-tools = %{version}-%{release}
Requires: virtiofsd
Requires: qemu-pr-helper = %{version}-%{release}
Requires: vhostuser-backend(fs)


%description
%{name} is an open source virtualizer that provides hardware
emulation for the KVM hypervisor. %{name} acts as a virtual
machine monitor together with the KVM kernel modules, and emulates the
hardware for a full system such as a PC and its associated peripherals.

%package common
Summary: QEMU common files needed by all QEMU targets
Requires(post): /usr/bin/getent
Requires(post): /usr/sbin/groupadd
Requires(post): /usr/sbin/useradd
Requires(post): systemd-units
Requires(preun): systemd-units
Requires(postun): systemd-units
%ifnarch aarch64
Requires: ipxe-roms-qemu >= %{ipxe_version}
%endif
Obsoletes: %{name}-device-display-virtio-gpu-gl <= %{version}
Obsoletes: %{name}-device-display-virtio-gpu-pci-gl <= %{version}
Obsoletes: %{name}-virtiofsd <= %{version}


%description common
This package provides documentation and auxiliary programs used with %{name}.


%package docs
Summary: %{name} documentation

%description docs
%{name}-docs provides documentation files regarding %{name}.


%package -n qemu-img
Summary: QEMU command line tool for manipulating disk images

%description -n qemu-img
This package provides a command line tool for manipulating disk images.


%package -n qemu-guest-agent
Summary: QEMU guest agent
Requires(post): systemd-units
Requires(preun): systemd-units
Requires(postun): systemd-units

%description -n qemu-guest-agent
This package provides an agent to run inside guests, which communicates
with the host over a virtio-serial channel named "org.qemu.guest_agent.0"

%package tools
Summary: %{name} support tools

%description tools
%{name}-tools provides various tools related to %{name} usage.


%package -n qemu-pr-helper
Summary: qemu-pr-helper utility for %{name}

%description -n qemu-pr-helper
This package provides the qemu-pr-helper utility that is required for certain
SCSI features.

%package tests
Summary: tests for the %{name} package
Requires: %{name} = %{version}-%{release}

%define testsdir %{_libdir}/%{name}/tests-src

%description tests
The %{name}-tests rpm contains tests that can be used to verify
the functionality of the installed %{name} package


%package  block-curl
Summary: QEMU CURL block driver
Requires: %{name}-common = %{version}-%{release}

%description block-curl
This package provides the additional CURL block driver for QEMU.

Install this package if you want to access remote disks over
http, https, ftp and other transports provided by the CURL library.


%package  block-iscsi
Summary: QEMU iSCSI block driver
Requires: %{name}-common = %{version}-%{release}

%description block-iscsi
This package provides the additional iSCSI block driver for QEMU.

Install this package if you want to access iSCSI volumes.

%if %{with rbd}
%package  block-rbd
Summary: QEMU Ceph/RBD block driver
Requires: %{name}-common = %{version}-%{release}

%description block-rbd
This package provides the additional Ceph/RBD block driver for QEMU.

Install this package if you want to access remote Ceph volumes
using the rbd protocol.
%endif


%package  block-ssh
Summary: QEMU SSH block driver
Requires: %{name}-common = %{version}-%{release}

%description block-ssh
This package provides the additional SSH block driver for QEMU.

Install this package if you want to access remote disks using
the Secure Shell (SSH) protocol.


%if %{with opengl}
%package  ui-opengl
Summary: QEMU opengl support
Requires: %{name}-common = %{version}-%{release}
Requires: mesa-libGL
Requires: mesa-libEGL
Requires: mesa-dri-drivers

%description ui-opengl
This package provides opengl support.
%endif

%package  block-dmg
Summary: QEMU block driver for DMG disk images
Requires: %{name}-common = %{version}-%{release}

%description block-dmg
This package provides the additional DMG block driver for QEMU.

Install this package if you want to open '.dmg' files.

%if %{with nfs}
%package  block-nfs
Summary: QEMU NFS block driver
Requires: %{name}-common = %{version}-%{release}

%description block-nfs
This package provides the additional NFS block driver for QEMU.

Install this package if you want to access remote NFS storage.
%endif

%package  audio-alsa
Summary: QEMU ALSA audio driver
Requires: %{name}-common = %{version}-%{release}

%description audio-alsa
This package provides the additional ALSA audio driver for QEMU.

%package  audio-oss
Summary: QEMU OSS audio driver
Requires: %{name}-common = %{version}-%{release}

%description audio-oss
This package provides the additional OSS audio driver for QEMU.

%package  audio-pa
Summary: QEMU PulseAudio audio driver
Requires: %{name}-common = %{version}-%{release}

%description audio-pa
This package provides the additional PulseAudi audio driver for QEMU.

%package  audio-sdl
Summary: QEMU SDL audio driver
Requires: %{name}-common = %{version}-%{release}

%description audio-sdl
This package provides the additional SDL audio driver for QEMU.

%package  ui-curses
Summary: QEMU curses UI driver
Requires: %{name}-common = %{version}-%{release}

%description ui-curses
This package provides the additional curses UI for QEMU.

%package  ui-gtk
Summary: QEMU GTK UI driver
Requires: %{name}-common = %{version}-%{release}
%if %{with opengl}
Requires: %{name}-ui-opengl = %{version}-%{release}
%endif

%description ui-gtk
This package provides the additional GTK UI for QEMU.

%package  ui-sdl
Summary: QEMU SDL UI driver
Requires: %{name}-common = %{version}-%{release}
%if %{with opengl}
Requires: %{name}-ui-opengl = %{version}-%{release}
%endif

%description ui-sdl
This package provides the additional SDL UI for QEMU.

%if %{with opengl}
%package  ui-egl-headless
Summary: QEMU EGL headless driver
Requires: %{name}-common = %{version}-%{release}
Requires: %{name}-ui-opengl = %{version}-%{release}

%description ui-egl-headless
This package provides the additional egl-headless UI for QEMU.
%endif

%package device-display-virtio-gpu
Summary: QEMU virtio-gpu display device
Requires: %{name}-common = %{version}-%{release}

%description device-display-virtio-gpu
This package provides the virtio-gpu display device for QEMU.

%package device-display-virtio-gpu-pci
Summary: QEMU virtio-gpu-pci display device
Requires: %{name}-common = %{version}-%{release}

%description device-display-virtio-gpu-pci
This package provides the virtio-gpu-pci display device for QEMU.

%package device-display-virtio-gpu-ccw
Summary: QEMU virtio-gpu-ccw display device
Requires: %{name}-common = %{version}-%{release}

%description device-display-virtio-gpu-ccw
This package provides the virtio-gpu-ccw display device for QEMU.

%package device-display-virtio-vga
Summary: QEMU virtio-vga display device
Requires: %{name}-common = %{version}-%{release}

%description device-display-virtio-vga
This package provides the virtio-vga display device for QEMU.

%package device-display-virtio-vga-gl
Summary: QEMU virtio-vga-gl display device
Requires: %{name}-common = %{version}-%{release}

%description device-display-virtio-vga-gl
This package provides the virtio-vga-gl display device for QEMU.

%package device-usb-host
Summary: QEMU usb host device
Requires: %{name}-common = %{version}-%{release}

%description device-usb-host
This package provides the USB pass through driver for QEMU.

%if %{with usb_redir}
%package device-usb-redirect
Summary: QEMU usbredir device
Requires: %{name}-common = %{version}-%{release}

%description device-usb-redirect
This package provides the usbredir device for QEMU.
%endif

%if %{with virtgl}
%package device-display-vhost-user-gpu
Summary: QEMU QXL display device
Requires: %{name}-common = %{version}-%{release}

%description device-display-vhost-user-gpu
This package provides the vhost-user-gpu display device for QEMU.
%endif

%package kvm
Summary: QEMU metapackage for KVM support
Requires: qemu-%{kvm_package} = %{version}-%{release}

%description kvm
This is a meta-package that provides a qemu-system-<arch> package for native
architectures where kvm can be enabled. For example, in an x86 system, this
will install qemu-system-x86


%package kvm-core
Summary: QEMU metapackage for KVM support
Requires: qemu-%{kvm_package}-core = %{version}-%{release}

%description kvm-core
This is a meta-package that provides a qemu-system-<arch>-core package
for native architectures where kvm can be enabled. For example, in an
x86 system, this will install qemu-system-x86-core


%package user
Summary: QEMU user mode emulation of qemu targets
Requires: %{name}-common = %{version}-%{release}

%description user
This package provides the user mode emulation of qemu targets


%package user-binfmt
Summary: QEMU user mode emulation of qemu targets
Requires: %{name}-user = %{version}-%{release}
Requires(post): systemd-units
Requires(postun): systemd-units

%description user-binfmt
This package provides the user mode emulation of qemu targets

%package user-static
Summary: QEMU user mode emulation of qemu targets static build
Requires: %{name}-common = %{version}-%{release}
Requires(post): systemd-units
Requires(postun): systemd-units

%description user-static
This package provides the user mode emulation of qemu targets built as
static binaries

%ifarch aarch64
%package system-aarch64
Summary: QEMU system emulator for AArch64
Requires: %{name}-system-aarch64-core = %{version}-%{release}
%{requires_all_modules}

%description system-aarch64
This package provides the QEMU system emulator for AArch64.

%package system-aarch64-core
Summary: QEMU system emulator for AArch64
Requires: %{name}-common = %{version}-%{release}
Requires: edk2-aarch64

%description system-aarch64-core
This package provides the QEMU system emulator for AArch64.
%endif

%ifarch loongarch64
%package system-loongarch64
Summary: QEMU system emulator for Loongarch64
Requires: %{name}-system-loongarch64-core = %{version}-%{release}

%description system-Loongarch64
This package provides the QEMU system emulator for Loongarch64.

%package system-loongarch64-core
Summary: QEMU system emulator for Loongarch64
Requires: %{name}-common = %{version}-%{release}

%description system-loongarch64-core
This package provides the QEMU system emulator for Loongarch64.
%endif

%if %{with extra_arch}
%package system-alpha
Summary: QEMU system emulator for Alpha
Requires: %{name}-system-alpha-core = %{version}-%{release}
%{requires_all_modules}

%description system-alpha
This package provides the QEMU system emulator for Alpha systems.

%package system-alpha-core
Summary: QEMU system emulator for Alpha
Requires: %{name}-common = %{version}-%{release}

%description system-alpha-core
This package provides the QEMU system emulator for Alpha systems.


%package system-arm
Summary: QEMU system emulator for ARM
Requires: %{name}-system-arm-core = %{version}-%{release}
%{requires_all_modules}

%description system-arm
This package provides the QEMU system emulator for ARM systems.

%package system-arm-core
Summary: QEMU system emulator for ARM
Requires: %{name}-common = %{version}-%{release}

%description system-arm-core
This package provides the QEMU system emulator for ARM boards.


%package system-avr
Summary: QEMU system emulator for AVR
Requires: %{name}-system-avr-core = %{version}-%{release}
%{requires_all_modules}

%description system-avr
This package provides the QEMU system emulator for AVR systems.

%package system-avr-core
Summary: QEMU system emulator for AVR
Requires: %{name}-common = %{version}-%{release}

%description system-avr-core
This package provides the QEMU system emulator for AVR systems.


%package system-cris
Summary: QEMU system emulator for CRIS
Requires: %{name}-system-cris-core = %{version}-%{release}
%{requires_all_modules}

%description system-cris
This package provides the system emulator for CRIS systems.

%package system-cris-core
Summary: QEMU system emulator for CRIS
Requires: %{name}-common = %{version}-%{release}

%description system-cris-core
This package provides the system emulator for CRIS boards.


%package system-hppa
Summary: QEMU system emulator for HPPA
Requires: %{name}-system-hppa-core = %{version}-%{release}
%{requires_all_modules}

%description system-hppa
This package provides the QEMU system emulator for HPPA.

%package system-hppa-core
Summary: QEMU system emulator for hppa
Requires: %{name}-common = %{version}-%{release}

%description system-hppa-core
This package provides the QEMU system emulator for HPPA.


%package system-m68k
Summary: QEMU system emulator for ColdFire (m68k)
Requires: %{name}-system-m68k-core = %{version}-%{release}
%{requires_all_modules}

%description system-m68k
This package provides the QEMU system emulator for ColdFire boards.

%package system-m68k-core
Summary: QEMU system emulator for ColdFire (m68k)
Requires: %{name}-common = %{version}-%{release}

%description system-m68k-core
This package provides the QEMU system emulator for ColdFire boards.


%package system-microblaze
Summary: QEMU system emulator for Microblaze
Requires: %{name}-system-microblaze-core = %{version}-%{release}
%{requires_all_modules}

%description system-microblaze
This package provides the QEMU system emulator for Microblaze boards.

%package system-microblaze-core
Summary: QEMU system emulator for Microblaze
Requires: %{name}-common = %{version}-%{release}

%description system-microblaze-core
This package provides the QEMU system emulator for Microblaze boards.


%package system-mips
Summary: QEMU system emulator for MIPS
Requires: %{name}-system-mips-core = %{version}-%{release}
%{requires_all_modules}

%description system-mips
This package provides the QEMU system emulator for MIPS systems.

%package system-mips-core
Summary: QEMU system emulator for MIPS
Requires: %{name}-common = %{version}-%{release}

%description system-mips-core
This package provides the QEMU system emulator for MIPS systems.


%package system-nios2
Summary: QEMU system emulator for nios2
Requires: %{name}-system-nios2-core = %{version}-%{release}
%{requires_all_modules}

%description system-nios2
This package provides the QEMU system emulator for NIOS2.

%package system-nios2-core
Summary: QEMU system emulator for nios2
Requires: %{name}-common = %{version}-%{release}

%description system-nios2-core
This package provides the QEMU system emulator for NIOS2.


%package system-or1k
Summary: QEMU system emulator for OpenRisc32
Requires: %{name}-system-or1k-core = %{version}-%{release}
%{requires_all_modules}

%description system-or1k
This package provides the QEMU system emulator for OpenRisc32 boards.

%package system-or1k-core
Summary: QEMU system emulator for OpenRisc32
Requires: %{name}-common = %{version}-%{release}

%description system-or1k-core
This package provides the QEMU system emulator for OpenRisc32 boards.

%package system-rx
Summary: QEMU system emulator for RX
Requires: %{name}-system-rx-core = %{version}-%{release}
%{requires_all_modules}

%description system-rx
This package provides the QEMU system emulator for RX systems.

%package system-rx-core
Summary: QEMU system emulator for RX
Requires: %{name}-common = %{version}-%{release}

%description system-rx-core
This package provides the QEMU system emulator for RX systems.

%package system-s390x
Summary: QEMU system emulator for S390
Requires: %{name}-system-s390x-core = %{version}-%{release}
%{requires_all_modules}

%description system-s390x
This package provides the QEMU system emulator for S390 systems.

%package system-s390x-core
Summary: QEMU system emulator for S390
Requires: %{name}-common = %{version}-%{release}

%description system-s390x-core
This package provides the QEMU system emulator for S390 systems.

%package system-sh4
Summary: QEMU system emulator for SH4
Requires: %{name}-system-sh4-core = %{version}-%{release}
%{requires_all_modules}

%description system-sh4
This package provides the QEMU system emulator for SH4 boards.

%package system-sh4-core
Summary: QEMU system emulator for SH4
Requires: %{name}-common = %{version}-%{release}

%description system-sh4-core
This package provides the QEMU system emulator for SH4 boards.

%package system-tricore
Summary: QEMU system emulator for tricore
Requires: %{name}-system-tricore-core = %{version}-%{release}
%{requires_all_modules}

%description system-tricore
This package provides the QEMU system emulator for Tricore.

%package system-tricore-core
Summary: QEMU system emulator for tricore
Requires: %{name}-common = %{version}-%{release}

%description system-tricore-core
This package provides the QEMU system emulator for Tricore.

%package system-xtensa
Summary: QEMU system emulator for Xtensa
Requires: %{name}-system-xtensa-core = %{version}-%{release}
%{requires_all_modules}

%description system-xtensa
This package provides the QEMU system emulator for Xtensa boards.

%package system-xtensa-core
Summary: QEMU system emulator for Xtensa
Requires: %{name}-common = %{version}-%{release}

%description system-xtensa-core
This package provides the QEMU system emulator for Xtensa boards.
%endif

%ifarch x86_64
%package system-x86
Summary: QEMU system emulator for x86
Requires: %{name}-system-x86-core = %{version}-%{release}
%{requires_all_modules}

%description system-x86
This package provides the QEMU system emulator for x86. When being run in a x86
machine that supports it, this package also provides the KVM virtualization
platform.

%package system-x86-core
Summary: QEMU system emulator for x86
Requires: %{name}-common = %{version}-%{release}
Requires: seabios-bin
Requires: sgabios-bin
Requires: seavgabios-bin
Requires: edk2-ovmf

%description system-x86-core
This package provides the QEMU system emulator for x86. When being run in a x86
machine that supports it, this package also provides the KVM virtualization
platform.
%endif

%ifarch ppc64le
%package system-ppc
Summary: QEMU system emulator for PPC
Requires: %{name}-system-ppc-core = %{version}-%{release}
%{requires_all_modules}

%description system-ppc
This package provides the QEMU system emulator for PPC and PPC64 systems.

%package system-ppc-core
Summary: QEMU system emulator for PPC
Requires: %{name}-common = %{version}-%{release}
Requires: openbios
Requires: SLOF
Requires: seavgabios-bin

%description system-ppc-core
This package provides the QEMU system emulator for PPC and PPC64 systems.
%endif

%ifarch riscv
%package system-riscv
Summary: QEMU system emulator for RISC-V
Requires: %{name}-system-riscv-core = %{version}-%{release}
%{requires_all_modules}

%description system-riscv
This package provides the QEMU system emulator for RISC-V systems.

%package system-riscv-core
Summary: QEMU system emulator for RISC-V
Requires: %{name}-common = %{version}-%{release}

%description system-riscv-core
This package provides the QEMU system emulator for RISC-V systems
%endif

%prep
%autosetup -p1

%global qemu_kvm_build qemu_kvm_build
mkdir -p %{qemu_kvm_build}
%global static_builddir static_builddir
mkdir -p %{static_builddir}



%build
%define disable_everything         \\\
  --audio-drv-list=                \\\
  --disable-attr                   \\\
  --disable-auth-pam               \\\
  --disable-avx2                   \\\
  --disable-avx512f                \\\
  --disable-block-drv-whitelist-in-tools \\\
  --disable-bpf                    \\\
  --disable-bochs                  \\\
  --disable-brlapi                 \\\
  --disable-bsd-user               \\\
  --disable-bzip2                  \\\
  --disable-cap-ng                 \\\
  --disable-cfi                    \\\
  --disable-cfi-debug              \\\
  --disable-cloop                  \\\
  --disable-cocoa                  \\\
  --disable-coroutine-pool         \\\
  --disable-crypto-afalg           \\\
  --disable-curl                   \\\
  --disable-curses                 \\\
  --disable-dbus-display           \\\
  --disable-debug-info             \\\
  --disable-debug-mutex            \\\
  --disable-debug-tcg              \\\
  --disable-dmg                    \\\
  --disable-docs                   \\\
  --disable-fdt                    \\\
  --disable-fuse                   \\\
  --disable-fuse-lseek             \\\
  --disable-gcrypt                 \\\
  --disable-gio                    \\\
  --disable-glusterfs              \\\
  --disable-gnutls                 \\\
  --disable-gtk                    \\\
  --disable-guest-agent            \\\
  --disable-guest-agent-msi        \\\
  --disable-hvf                    \\\
  --disable-iconv                  \\\
  --disable-kvm                    \\\
  --disable-libdaxctl              \\\
  --disable-libiscsi               \\\
  --disable-libnfs                 \\\
  --disable-libpmem                \\\
  --disable-libssh                 \\\
  --disable-libudev                \\\
  --disable-libusb                 \\\
  --disable-linux-aio              \\\
  --disable-linux-io-uring         \\\
  --disable-linux-user             \\\
  --disable-live-block-migration   \\\
  --disable-lto                    \\\
  --disable-lzfse                  \\\
  --disable-lzo                    \\\
  --disable-malloc-trim            \\\
  --disable-membarrier             \\\
  --disable-modules                \\\
  --disable-module-upgrades        \\\
  --disable-mpath                  \\\
  --disable-multiprocess           \\\
  --disable-netmap                 \\\
  --disable-nettle                 \\\
  --disable-numa                   \\\
  --disable-opengl                 \\\
  --disable-parallels              \\\
  --disable-pie                    \\\
  --disable-plugins                \\\
  --disable-pvrdma                 \\\
  --disable-qcow1                  \\\
  --disable-qed                    \\\
  --disable-qom-cast-debug         \\\
  --disable-rbd                    \\\
  --disable-rdma                   \\\
  --disable-replication            \\\
  --disable-rng-none               \\\
  --disable-safe-stack             \\\
  --disable-sanitizers             \\\
  --disable-sdl                    \\\
  --disable-sdl-image              \\\
  --disable-seccomp                \\\
  --disable-smartcard              \\\
  --disable-snappy                 \\\
  --disable-sparse                 \\\
  --disable-spice                  \\\
  --disable-spice-protocol         \\\
  --disable-strip                  \\\
  --disable-system                 \\\
  --disable-tcg                    \\\
  --disable-tools                  \\\
  --disable-tpm                    \\\
  --disable-u2f                    \\\
  --disable-usb-redir              \\\
  --disable-user                   \\\
  --disable-vde                    \\\
  --disable-vdi                    \\\
  --disable-virglrenderer          \\\
  --disable-virtfs                 \\\
  --disable-vnc                    \\\
  --disable-vnc-jpeg               \\\
  --disable-vnc-sasl               \\\
  --disable-vte                    \\\
  --disable-vvfat                  \\\
  --disable-werror                 \\\
  --disable-whpx                   \\\
  --disable-xen                    \\\
  --disable-xen-pci-passthrough    \\\
  --disable-xkbcommon              \\\
  --disable-zstd                   \\\
  --without-default-devices

run_configure() {
    ../configure  \
        --cc=%{__cc} \
        --cxx=/bin/false \
        --prefix="%{_prefix}" \
        --libdir="%{_libdir}" \
        --datadir="%{_datadir}" \
        --sysconfdir="%{_sysconfdir}" \
        --interp-prefix=%{_prefix}/qemu-%M \
        --localstatedir="%{_localstatedir}" \
        --docdir="%{_docdir}" \
        --libexecdir="%{_libexecdir}" \
        --extra-ldflags="%{build_ldflags}" \
        --extra-cflags="%{optflags}" \
        --with-pkgversion="%{name}-%{version}-%{release}" \
        --with-suffix="%{name}" \
        --firmwarepath="%firmwaredirs" \
        --enable-trace-backends=dtrace \
        --with-coroutine=ucontext \
        --tls-priority=@QEMU,SYSTEM \
        %{disable_everything} \
        "$@"
}


pushd %{qemu_kvm_build}
run_configure \
%if %{defined target_list}
  --target-list="%{target_list}" \
%endif
%if %{defined block_drivers_rw_list}
  --block-drv-rw-whitelist=%{block_drivers_rw_list} \
%endif
%if %{defined block_drivers_ro_list}
  --block-drv-ro-whitelist=%{block_drivers_ro_list} \
%endif
  --enable-attr \
%ifarch x86_64
  --enable-avx2 \
%endif
  --enable-bpf \
  --enable-cap-ng \
  --enable-coroutine-pool \
  --enable-curl \
  --enable-debug-info \
  --enable-docs \
  --enable-fdt=system \
  --enable-gnutls \
  --enable-guest-agent \
  --enable-iconv \
  --enable-kvm \
  --enable-libiscsi \
%if %{have_pmem}
  --enable-libpmem \
%endif
  --enable-libssh \
  --enable-libusb \
  --enable-libudev \
  --enable-linux-aio \
%if "%{_lto_cflags}" != "%{nil}"
  --enable-lto \
%endif
  --enable-lzo \
  --enable-malloc-trim \
  --enable-modules \
  --enable-mpath \
  --enable-numa \
%if %{with opengl}
  --enable-opengl \
%endif
  --enable-pie \
%if %{with rbd}
  --enable-rbd \
%endif
  --enable-rdma \
  --enable-seccomp \
  --enable-selinux \
  --enable-snappy \
  --enable-system \
  --enable-tcg \
  --enable-tools \
  --enable-tpm \
%if %{with usb_redir}
  --enable-usb-redir \
%endif
  --enable-vnc \
  --enable-vnc-sasl \
  --enable-xkbcommon \
  \
  \
  --audio-drv-list=pa,sdl,alsa,%{?jack_drv}oss \
  --target-list-exclude=moxie-softmmu \
  --with-default-devices \
  --enable-auth-pam \
  --enable-bochs \
  --enable-bzip2 \
  --enable-cloop \
  --enable-curses \
  --enable-dmg \
  --enable-fuse \
  --enable-gio \
  --enable-gtk \
  --enable-libdaxctl \
%if %{with nfs}
  --enable-libnfs \
%endif
  --enable-libudev \
  --enable-linux-io-uring \
  --enable-linux-user \
  --enable-live-block-migration \
  --enable-multiprocess \
  --enable-vnc-jpeg \
  --enable-parallels \
  --enable-pvrdma \
  --enable-qcow1 \
  --enable-qed \
  --enable-qom-cast-debug \
  --enable-replication \
  --enable-sdl \
  --enable-vdi \
  --enable-vhost-crypto \
%if %{with virgl}
  --enable-virglrenderer \
%endif
  --enable-virtfs \
  --enable-vnc-jpeg \
  --enable-vte \
  --enable-vvfat \
  --enable-zstd \


%make_build
popd

pushd %{static_builddir}

run_configure \
  --enable-attr \
  --enable-linux-user \
  --enable-tcg \
  --disable-install-blobs \
  --static

%make_build
popd



%install
install -D -m 0644 %{_sourcedir}/qemu-guest-agent.service %{buildroot}%{_unitdir}/qemu-guest-agent.service
install -D -m 0644 %{_sourcedir}/qemu-ga.sysconfig %{buildroot}%{_sysconfdir}/sysconfig/qemu-ga
install -D -m 0644 %{_sourcedir}/99-qemu-guest-agent.rules %{buildroot}%{_udevrulesdir}/99-qemu-guest-agent.rules


mkdir -p %{buildroot}%{_sysconfdir}/qemu-ga/fsfreeze-hook.d
install -p scripts/qemu-guest-agent/fsfreeze-hook %{buildroot}%{_sysconfdir}/qemu-ga/fsfreeze-hook
mkdir -p %{buildroot}%{_datadir}/%{name}/qemu-ga/fsfreeze-hook.d/
install -p -m 0644 scripts/qemu-guest-agent/fsfreeze-hook.d/*.sample %{buildroot}%{_datadir}/%{name}/qemu-ga/fsfreeze-hook.d/
mkdir -p -v %{buildroot}%{_localstatedir}/log/qemu-ga/


install -D -m 0644 %{_sourcedir}/bridge.conf %{buildroot}%{_sysconfdir}/%{name}/bridge.conf

install -m 0644 contrib/systemd/qemu-pr-helper.service %{buildroot}%{_unitdir}
install -m 0644 contrib/systemd/qemu-pr-helper.socket %{buildroot}%{_unitdir}

install -D -p -m 0644 %{_sourcedir}/vhost.conf %{buildroot}%{_sysconfdir}/modprobe.d/vhost.conf
install -D -p -m 0644 %{modprobe_kvm_conf} %{buildroot}%{_sysconfdir}/modprobe.d/kvm.conf

install -D -p -m 0644 -t %{buildroot}%{qemudocdir} README.rst COPYING COPYING.LIB LICENSE docs/interop/qmp-spec.rst
install -D -p -m 0644 qemu.sasl %{buildroot}%{_sysconfdir}/sasl2/%{name}.conf

install -m 0644 scripts/dump-guest-memory.py %{buildroot}%{_datadir}/%{name}


install -m 0755 scripts/simpletrace.py %{buildroot}%{_datadir}/%{name}/simpletrace.py
mkdir -p %{buildroot}%{_datadir}/%{name}/tracetool
install -m 0644 -t %{buildroot}%{_datadir}/%{name}/tracetool scripts/tracetool/*.py
mkdir -p %{buildroot}%{_datadir}/%{name}/tracetool/backend
install -m 0644 -t %{buildroot}%{_datadir}/%{name}/tracetool/backend scripts/tracetool/backend/*.py
mkdir -p %{buildroot}%{_datadir}/%{name}/tracetool/format
install -m 0644 -t %{buildroot}%{_datadir}/%{name}/tracetool/format scripts/tracetool/format/*.py


mkdir -p %{buildroot}%{testsdir}/python
mkdir -p %{buildroot}%{testsdir}/tests
mkdir -p %{buildroot}%{testsdir}/tests/avocado
mkdir -p %{buildroot}%{testsdir}/tests/qemu-iotests
mkdir -p %{buildroot}%{testsdir}/scripts/qmp

cp -R %{qemu_kvm_build}/tests/avocado/* %{buildroot}%{testsdir}/tests/avocado/

cp -R %{qemu_kvm_build}/python/qemu %{buildroot}%{testsdir}/python
cp -R %{qemu_kvm_build}/scripts/qmp/* %{buildroot}%{testsdir}/scripts/qmp
install -p -m 0755 tests/Makefile.include %{buildroot}%{testsdir}/tests/

cp -R tests/qemu-iotests/* %{buildroot}%{testsdir}/tests/qemu-iotests/
cp -ur %{qemu_kvm_build}/tests/qemu-iotests/* %{buildroot}%{testsdir}/tests/qemu-iotests/

pushd %{qemu_kvm_build}
%make_install
popd


chmod +x %{buildroot}%{_libdir}/%{name}/*.so

find %{buildroot}%{qemudocdir} -name .buildinfo -delete
rm -rf %{buildroot}%{qemudocdir}/specs

# Remove vof roms
rm -rf %{buildroot}%{_datadir}/%{name}/vof-nvram.bin
rm -rf %{buildroot}%{_datadir}/%{name}/vof.bin

%ifnarch ppc64le
rm -rf %{buildroot}%{_bindir}/qemu-system-ppc
rm -rf %{buildroot}%{_bindir}/qemu-system-ppc64
rm -rf %{buildroot}%{_datadir}/systemtap/tapset/qemu-system-ppc*.stp
rm -rf %{buildroot}%{_mandir}/man1/qemu-system-ppc.1*
rm -rf %{buildroot}%{_mandir}/man1/qemu-system-ppc64.1*
rm -rf %{buildroot}%{_datadir}/%{name}/bamboo.dtb
rm -rf %{buildroot}%{_datadir}/%{name}/canyonlands.dtb
rm -rf %{buildroot}%{_datadir}/%{name}/qemu_vga.ndrv
rm -rf %{buildroot}%{_datadir}/%{name}/skiboot.lid
rm -rf %{buildroot}%{_datadir}/%{name}/u-boot.e500
rm -rf %{buildroot}%{_datadir}/%{name}/u-boot-sam460-20100605.bin
%endif

%ifnarch aarch64
rm -rf %{buildroot}%{_bindir}/qemu-system-aarch64
rm -rf %{buildroot}%{_datadir}/systemtap/tapset/qemu-system-aarch64*.stp
rm -rf %{buildroot}%{_mandir}/man1/qemu-system-aarch64.1*
%endif

%ifnarch loongarch64
rm -rf %{buildroot}%{_bindir}/qemu-loongarch64
rm -rf %{buildroot}%{_bindir}/qemu-system-loongarch64
rm -rf %{buildroot}%{_datadir}/systemtap/tapset/qemu-loongarch64-log.stp
rm -rf %{buildroot}%{_datadir}/systemtap/tapset/qemu-loongarch64-simpletrace.stp
rm -rf %{buildroot}%{_datadir}/systemtap/tapset/qemu-loongarch64.stp
rm -rf %{buildroot}%{_datadir}/systemtap/tapset/qemu-system-loongarch64-log.stp
rm -rf %{buildroot}%{_datadir}/systemtap/tapset/qemu-system-loongarch64-simpletrace.stp
rm -rf %{buildroot}%{_datadir}/systemtap/tapset/qemu-system-loongarch64.stp
rm -rf %{buildroot}%{_mandir}/man1/qemu-system-loongarch64.1.gz
%endif

%ifnarch riscv
rm -rf %{buildroot}%{_bindir}/qemu-system-riscv32
rm -rf %{buildroot}%{_bindir}/qemu-system-riscv64
rm -rf %{buildroot}%{_datadir}/%{name}/opensbi-riscv*.bin
rm -rf %{buildroot}%{_datadir}/%{name}/opensbi-riscv*.elf
rm -rf %{buildroot}%{_datadir}/systemtap/tapset/qemu-system-riscv*.stp
rm -rf %{buildroot}%{_mandir}/man1/qemu-system-riscv*.1*
%endif

%ifnarch x86_64
rm -rf %{buildroot}%{_bindir}/qemu-system-i386
rm -rf %{buildroot}%{_bindir}/qemu-system-x86_64
rm -rf %{buildroot}%{_libdir}/%{name}/accel-tcg-i386.so
rm -rf %{buildroot}%{_libdir}/%{name}/accel-tcg-x86_64.so
rm -rf %{buildroot}%{_datadir}/systemtap/tapset/qemu-system-i386*.stp
rm -rf %{buildroot}%{_datadir}/systemtap/tapset/qemu-system-x86_64*.stp
rm -rf %{buildroot}%{_mandir}/man1/qemu-system-i386.1*
rm -rf %{buildroot}%{_mandir}/man1/qemu-system-x86_64.1*
rm -rf %{buildroot}%{_datadir}/%{name}/kvmvapic.bin
rm -rf %{buildroot}%{_datadir}/%{name}/linuxboot.bin
rm -rf %{buildroot}%{_datadir}/%{name}/multiboot.bin
rm -rf %{buildroot}%{_datadir}/%{name}/multiboot_dma.bin
rm -rf %{buildroot}%{_datadir}/%{name}/pvh.bin
rm -rf %{buildroot}%{_datadir}/%{name}/qboot.rom
rm -rf %{buildroot}%{_bindir}/qemu-kvm
rm -rf %{buildroot}%{_mandir}/man1/qemu-kvm.1*
%endif

rm -rf %{buildroot}%{_bindir}/qemu-system-sparc
rm -rf %{buildroot}%{_bindir}/qemu-system-sparc64
rm -rf %{buildroot}%{_datadir}/systemtap/tapset/qemu-system-sparc*.stp
rm -rf %{buildroot}%{_mandir}/man1/qemu-system-sparc.1*
rm -rf %{buildroot}%{_mandir}/man1/qemu-system-sparc64.1*
rm -rf %{buildroot}%{_datadir}/%{name}/QEMU,tcx.bin
rm -rf %{buildroot}%{_datadir}/%{name}/QEMU,cgthree.bin
rm -rf %{buildroot}%{_datadir}/%{name}/openbios-ppc
rm -rf %{buildroot}%{_datadir}/%{name}/openbios-sparc32
rm -rf %{buildroot}%{_datadir}/%{name}/openbios-sparc64
rm -rf %{buildroot}%{_datadir}/%{name}/slof.bin
rm -rf %{buildroot}%{_datadir}/%{name}/pxe*rom
rm -rf %{buildroot}%{_datadir}/%{name}/efi*rom
rm -rf %{buildroot}%{_datadir}/%{name}/vgabios*bin
rm -rf %{buildroot}%{_datadir}/%{name}/bios*.bin
rm -rf %{buildroot}%{_datadir}/%{name}/sgabios.bin
rm -rf %{buildroot}%{_datadir}/%{name}/edk2*
rm -rf %{buildroot}%{_datadir}/%{name}/firmware

%if %{without extra_arch}
rm -rf %{buildroot}%{_bindir}/qemu-system-alpha
rm -rf %{buildroot}%{_datadir}/systemtap/tapset/qemu-system-alpha*.stp
rm -rf %{buildroot}%{_mandir}/man1/qemu-system-alpha.1*
rm -rf %{buildroot}%{_datadir}/%{name}/palcode-clipper
rm -rf %{buildroot}%{_bindir}/qemu-system-arm
rm -rf %{buildroot}%{_datadir}/%{name}/npcm7xx_bootrom.bin
rm -rf %{buildroot}%{_datadir}/systemtap/tapset/qemu-system-arm*.stp
rm -rf %{buildroot}%{_mandir}/man1/qemu-system-arm.1*
rm -rf %{buildroot}%{_bindir}/qemu-system-avr
rm -rf %{buildroot}%{_datadir}/systemtap/tapset/qemu-system-avr*.stp
rm -rf %{buildroot}%{_mandir}/man1/qemu-system-avr.1*
rm -rf %{buildroot}%{_bindir}/qemu-system-cris
rm -rf %{buildroot}%{_datadir}/systemtap/tapset/qemu-system-cris*.stp
rm -rf %{buildroot}%{_mandir}/man1/qemu-system-cris.1*
rm -rf %{buildroot}%{_bindir}/qemu-system-hppa
rm -rf %{buildroot}%{_datadir}/systemtap/tapset/qemu-system-hppa*.stp
rm -rf %{buildroot}%{_mandir}/man1/qemu-system-hppa.1*
rm -rf %{buildroot}%{_datadir}/%{name}/hppa-firmware.img
rm -rf %{buildroot}%{_bindir}/qemu-system-m68k
rm -rf %{buildroot}%{_datadir}/systemtap/tapset/qemu-system-m68k*.stp
rm -rf %{buildroot}%{_mandir}/man1/qemu-system-m68k.1*
rm -rf %{buildroot}%{_bindir}/qemu-system-microblaze
rm -rf %{buildroot}%{_bindir}/qemu-system-microblazeel
rm -rf %{buildroot}%{_datadir}/systemtap/tapset/qemu-system-microblaze*.stp
rm -rf %{buildroot}%{_mandir}/man1/qemu-system-microblaze.1*
rm -rf %{buildroot}%{_mandir}/man1/qemu-system-microblazeel.1*
rm -rf %{buildroot}%{_datadir}/%{name}/petalogix*.dtb
rm -rf %{buildroot}%{_bindir}/qemu-system-mips
rm -rf %{buildroot}%{_bindir}/qemu-system-mipsel
rm -rf %{buildroot}%{_bindir}/qemu-system-mips64
rm -rf %{buildroot}%{_bindir}/qemu-system-mips64el
rm -rf %{buildroot}%{_datadir}/systemtap/tapset/qemu-system-mips*.stp
rm -rf %{buildroot}%{_mandir}/man1/qemu-system-mips.1*
rm -rf %{buildroot}%{_mandir}/man1/qemu-system-mipsel.1*
rm -rf %{buildroot}%{_mandir}/man1/qemu-system-mips64el.1*
rm -rf %{buildroot}%{_mandir}/man1/qemu-system-mips64.1*
rm -rf %{buildroot}%{_bindir}/qemu-system-nios2
rm -rf %{buildroot}%{_datadir}/systemtap/tapset/qemu-system-nios2*.stp
rm -rf %{buildroot}%{_mandir}/man1/qemu-system-nios2.1*
rm -rf %{buildroot}%{_bindir}/qemu-system-or1k
rm -rf %{buildroot}%{_datadir}/systemtap/tapset/qemu-system-or1k*.stp
rm -rf %{buildroot}%{_mandir}/man1/qemu-system-or1k.1*
rm -rf %{buildroot}%{_bindir}/qemu-system-rx
rm -rf %{buildroot}%{_datadir}/systemtap/tapset/qemu-system-rx*.stp
rm -rf %{buildroot}%{_mandir}/man1/qemu-system-rx.1*
rm -rf %{buildroot}%{_bindir}/qemu-system-s390x
rm -rf %{buildroot}%{_datadir}/systemtap/tapset/qemu-system-s390x*.stp
rm -rf %{buildroot}%{_mandir}/man1/qemu-system-s390x.1*
rm -rf %{buildroot}%{_datadir}/%{name}/s390-ccw.img
rm -rf %{buildroot}%{_datadir}/%{name}/s390-netboot.img
rm -rf %{buildroot}%{_bindir}/qemu-system-sh4
rm -rf %{buildroot}%{_bindir}/qemu-system-sh4eb
rm -rf %{buildroot}%{_datadir}/systemtap/tapset/qemu-system-sh4*.stp
rm -rf %{buildroot}%{_mandir}/man1/qemu-system-sh4.1*
rm -rf %{buildroot}%{_mandir}/man1/qemu-system-sh4eb.1*
rm -rf %{buildroot}%{_bindir}/qemu-system-tricore
rm -rf %{buildroot}%{_datadir}/systemtap/tapset/qemu-system-tricore*.stp
rm -rf %{buildroot}%{_mandir}/man1/qemu-system-tricore.1*
rm -rf %{buildroot}%{_bindir}/qemu-system-xtensa
rm -rf %{buildroot}%{_bindir}/qemu-system-xtensaeb
rm -rf %{buildroot}%{_datadir}/systemtap/tapset/qemu-system-xtensa*.stp
rm -rf %{buildroot}%{_mandir}/man1/qemu-system-xtensa.1*
rm -rf %{buildroot}%{_mandir}/man1/qemu-system-xtensaeb.1*
%endif

%find_lang %{name}

chmod -x %{buildroot}%{_mandir}/man1/*
for emu in %{buildroot}%{_bindir}/qemu-system-*; do
    ln -sf qemu.1.gz %{buildroot}%{_mandir}/man1/$(basename $emu).1.gz
 done

%ifarch x86_64
ln -sf qemu.1.gz %{buildroot}%{_mandir}/man1/qemu-kvm.1.gz
ln -sf qemu-system-x86_64 %{buildroot}%{_bindir}/qemu-kvm
%endif


%global binfmt_dir %{buildroot}%{_exec_prefix}/lib/binfmt.d
mkdir -p %{binfmt_dir}

./scripts/qemu-binfmt-conf.sh --systemd ALL --exportdir %{binfmt_dir} --qemu-path %{_bindir}
for i in %{binfmt_dir}/*; do mv $i $(echo $i | sed 's/.conf/-dynamic.conf/'); done


%define static_buildroot %{buildroot}/static/
mkdir -p %{static_buildroot}

pushd %{static_builddir}
make DESTDIR=%{static_buildroot} install
popd

for src in %{static_buildroot}%{_bindir}/qemu-*; do
    mv $src %{buildroot}%{_bindir}/$(basename $src)-static; done

for src in %{static_buildroot}%{_datadir}/systemtap/tapset/qemu-*.stp; do
  dst=`echo $src | sed -e 's/.stp/-static.stp/'`
  mv $src $dst
  perl -i -p -e 's/(qemu-\w+)/$1-static/g; s/(qemu\.user\.\w+)/$1.static/g' $dst
  mv $dst %{buildroot}%{_datadir}/systemtap/tapset
 done

for regularfmt in %{binfmt_dir}/*; do
  staticfmt="$(echo $regularfmt | sed 's/-dynamic/-static/g')"
  cat $regularfmt | tr -d '\n' | sed "s/:$/-static:F/" > $staticfmt
  done

rm -rf %{static_buildroot}



%check
pushd %{qemu_kvm_build}
%make_build check
popd

%post -n qemu-guest-agent
%systemd_post qemu-guest-agent.service
%preun -n qemu-guest-agent
%systemd_preun qemu-guest-agent.service
%postun -n qemu-guest-agent
%systemd_postun_with_restart qemu-guest-agent.service


%post common
getent group kvm >/dev/null || groupadd -g 36 -r kvm
getent group qemu >/dev/null || groupadd -g 107 -r qemu
getent passwd qemu >/dev/null || \
useradd -r -u 107 -g qemu -G kvm -d / -s /sbin/nologin \
  -c "qemu user" qemu


%post user-binfmt
/bin/systemctl --system try-restart systemd-binfmt.service &>/dev/null || :
%postun user-binfmt
/bin/systemctl --system try-restart systemd-binfmt.service &>/dev/null || :

%post user-static
/bin/systemctl --system try-restart systemd-binfmt.service &>/dev/null || :
%postun user-static
/bin/systemctl --system try-restart systemd-binfmt.service &>/dev/null || :

%files
# main pkg

%files -n qemu-img
%{_bindir}/qemu-img
%{_bindir}/qemu-io
%{_bindir}/qemu-nbd
%{_bindir}/qemu-storage-daemon
%{_mandir}/man1/qemu-img.1*
%{_mandir}/man8/qemu-nbd.8*
%{_mandir}/man1/qemu-storage-daemon.1*
%{_mandir}/man7/qemu-storage-daemon-qmp-ref.7*


%files -n qemu-guest-agent
%license COPYING
%doc README.rst
%{_bindir}/qemu-ga
%{_mandir}/man8/qemu-ga.8*
%{_unitdir}/qemu-guest-agent.service
%{_udevrulesdir}/99-qemu-guest-agent.rules
%config(noreplace) %{_sysconfdir}/sysconfig/qemu-ga
%{_sysconfdir}/qemu-ga
%{_datadir}/%{name}/qemu-ga
%dir %{_localstatedir}/log/qemu-ga



%files -n qemu-pr-helper
%{_bindir}/qemu-pr-helper
%{_unitdir}/qemu-pr-helper.service
%{_unitdir}/qemu-pr-helper.socket
%{_mandir}/man8/qemu-pr-helper.8*


%files tools
%{_bindir}/qemu-keymap
%{_bindir}/qemu-edid
%{_bindir}/qemu-trace-stap
%{_bindir}/elf2dmp
%{_datadir}/%{name}/simpletrace.py*
%{_datadir}/%{name}/tracetool/*.py*
%{_datadir}/%{name}/tracetool/backend/*.py*
%{_datadir}/%{name}/tracetool/format/*.py*
%{_datadir}/%{name}/dump-guest-memory.py*
%{_datadir}/%{name}/trace-events-all
%{_mandir}/man1/qemu-trace-stap.1*


%files docs
%doc %{qemudocdir}


%files common -f %{name}.lang
%license COPYING COPYING.LIB LICENSE
%dir %{_datadir}/%{name}/
%{_datadir}/icons/*
%{_datadir}/%{name}/keymaps/
%{_datadir}/%{name}/linuxboot_dma.bin
%attr(4755, -, -) %{_libexecdir}/qemu-bridge-helper
%dir %{_sysconfdir}/%{name}
%config(noreplace) %{_sysconfdir}/%{name}/bridge.conf
%config(noreplace) %{_sysconfdir}/modprobe.d/kvm.conf
%config(noreplace) %{_sysconfdir}/modprobe.d/vhost.conf
%config(noreplace) %{_sysconfdir}/sasl2/%{name}.conf
%{_datadir}/applications/qemu.desktop
%exclude %{_datadir}/%{name}/qemu-nsis.bmp
%{_libexecdir}/virtfs-proxy-helper
%{_mandir}/man1/%{name}.1*
%{_mandir}/man7/qemu-block-drivers.7*
%{_mandir}/man7/qemu-cpu-models.7*
%{_mandir}/man7/qemu-ga-ref.7*
%{_mandir}/man7/qemu-qmp-ref.7*
%{_mandir}/man1/virtfs-proxy-helper.1*


%files tests
%{testsdir}
%{_libdir}/%{name}/accel-qtest-*.so

%files block-curl
%{_libdir}/%{name}/block-curl.so
%files block-iscsi
%{_libdir}/%{name}/block-iscsi.so
%if %{with rbd}
%files block-rbd
%{_libdir}/%{name}/block-rbd.so
%endif
%files block-ssh
%{_libdir}/%{name}/block-ssh.so

%if %{with opengl}
%files ui-opengl
%{_libdir}/%{name}/ui-opengl.so
%endif

%files block-dmg
%{_libdir}/%{name}/block-dmg-bz2.so
%if %{with nfs}
%files block-nfs
%{_libdir}/%{name}/block-nfs.so
%endif

%files audio-alsa
%{_libdir}/%{name}/audio-alsa.so

%files audio-oss
%{_libdir}/%{name}/audio-oss.so

%files audio-pa
%{_libdir}/%{name}/audio-pa.so

%files audio-sdl
%{_libdir}/%{name}/audio-sdl.so

%files ui-curses
%{_libdir}/%{name}/ui-curses.so

%files ui-gtk
%{_libdir}/%{name}/ui-gtk.so

%files ui-sdl
%{_libdir}/%{name}/ui-sdl.so

%if %{with opengl}
%files ui-egl-headless
%{_libdir}/%{name}/ui-egl-headless.so
%endif

%files device-display-virtio-gpu
%{_libdir}/%{name}/hw-display-virtio-gpu.so

%files device-display-virtio-gpu-pci
%{_libdir}/%{name}/hw-display-virtio-gpu-pci.so

%files device-display-virtio-gpu-ccw
%{_libdir}/%{name}/hw-s390x-virtio-gpu-ccw.so

%files device-display-virtio-vga
%{_libdir}/%{name}/hw-display-virtio-vga.so

%files device-display-virtio-vga-gl
%{_libdir}/%{name}/hw-display-virtio-vga-gl.so

%files device-usb-host
%{_libdir}/%{name}/hw-usb-host.so

%if %{with usb_redir}
%files device-usb-redirect
%{_libdir}/%{name}/hw-usb-redirect.so
%endif

%if %{with virtgl}
%files device-display-vhost-user-gpu
%{_datadir}/%{name}/vhost-user/50-qemu-gpu.json
%{_libexecdir}/vhost-user-gpu
%endif

%files kvm
# Deliberately empty

%files kvm-core
# Deliberately empty


%files user
%{_bindir}/qemu-i386
%{_bindir}/qemu-x86_64
%{_bindir}/qemu-aarch64
%{_bindir}/qemu-aarch64_be
%{_bindir}/qemu-alpha
%{_bindir}/qemu-arm
%{_bindir}/qemu-armeb
%{_bindir}/qemu-cris
%{_bindir}/qemu-hppa
%{_bindir}/qemu-hexagon
%{_bindir}/qemu-m68k
%{_bindir}/qemu-microblaze
%{_bindir}/qemu-microblazeel
%{_bindir}/qemu-mips
%{_bindir}/qemu-mipsel
%{_bindir}/qemu-mips64
%{_bindir}/qemu-mips64el
%{_bindir}/qemu-mipsn32
%{_bindir}/qemu-mipsn32el
%{_bindir}/qemu-nios2
%{_bindir}/qemu-or1k
%{_bindir}/qemu-ppc
%{_bindir}/qemu-ppc64
%{_bindir}/qemu-ppc64le
%{_bindir}/qemu-riscv32
%{_bindir}/qemu-riscv64
%{_bindir}/qemu-s390x
%{_bindir}/qemu-sh4
%{_bindir}/qemu-sh4eb
%{_bindir}/qemu-sparc
%{_bindir}/qemu-sparc32plus
%{_bindir}/qemu-sparc64
%{_bindir}/qemu-xtensa
%{_bindir}/qemu-xtensaeb
%{_datadir}/systemtap/tapset/qemu-i386*.stp
%{_datadir}/systemtap/tapset/qemu-x86_64*.stp
%{_datadir}/systemtap/tapset/qemu-aarch64*.stp
%{_datadir}/systemtap/tapset/qemu-alpha*.stp
%{_datadir}/systemtap/tapset/qemu-arm*.stp
%{_datadir}/systemtap/tapset/qemu-cris*.stp
%{_datadir}/systemtap/tapset/qemu-hppa*.stp
%{_datadir}/systemtap/tapset/qemu-hexagon*.stp
%{_datadir}/systemtap/tapset/qemu-m68k*.stp
%{_datadir}/systemtap/tapset/qemu-microblaze*.stp
%{_datadir}/systemtap/tapset/qemu-mips*.stp
%{_datadir}/systemtap/tapset/qemu-nios2*.stp
%{_datadir}/systemtap/tapset/qemu-or1k*.stp
%{_datadir}/systemtap/tapset/qemu-ppc*.stp
%{_datadir}/systemtap/tapset/qemu-riscv*.stp
%{_datadir}/systemtap/tapset/qemu-s390x*.stp
%{_datadir}/systemtap/tapset/qemu-sh4*.stp
%{_datadir}/systemtap/tapset/qemu-sparc*.stp
%{_datadir}/systemtap/tapset/qemu-xtensa*.stp


%files user-binfmt
%{_exec_prefix}/lib/binfmt.d/qemu-*-dynamic.conf

%files user-static
%{_exec_prefix}/lib/binfmt.d/qemu-*-static.conf
%{_bindir}/qemu-*-static
%{_datadir}/systemtap/tapset/qemu-*-static.stp

%ifarch aarch64
%files system-aarch64
%files system-aarch64-core
%{_bindir}/qemu-system-aarch64
%{_datadir}/systemtap/tapset/qemu-system-aarch64*.stp
%{_mandir}/man1/qemu-system-aarch64.1*
%endif

%ifarch loongarch64
%files system-loongarch64
%files system-loongarch64-core
%{_bindir}/qemu-loongarch64
%{_bindir}/qemu-system-loongarch64
%{_datadir}/systemtap/tapset/qemu-loongarch64-log.stp
%{_datadir}/systemtap/tapset/qemu-loongarch64-simpletrace.stp
%{_datadir}/systemtap/tapset/qemu-loongarch64.stp
%{_datadir}/systemtap/tapset/qemu-system-loongarch64-log.stp
%{_datadir}/systemtap/tapset/qemu-system-loongarch64-simpletrace.stp
%{_datadir}/systemtap/tapset/qemu-system-loongarch64.stp
%{_mandir}/man1/qemu-system-loongarch64.1.gz
%endif

%if %{with extra_arch}
%files system-alpha
%files system-alpha-core
%{_bindir}/qemu-system-alpha
%{_datadir}/systemtap/tapset/qemu-system-alpha*.stp
%{_mandir}/man1/qemu-system-alpha.1*
%{_datadir}/%{name}/palcode-clipper


%files system-arm
%files system-arm-core
%{_bindir}/qemu-system-arm
%{_datadir}/%{name}/npcm7xx_bootrom.bin
%{_datadir}/systemtap/tapset/qemu-system-arm*.stp
%{_mandir}/man1/qemu-system-arm.1*


%files system-avr
%files system-avr-core
%{_bindir}/qemu-system-avr
%{_datadir}/systemtap/tapset/qemu-system-avr*.stp
%{_mandir}/man1/qemu-system-avr.1*


%files system-cris
%files system-cris-core
%{_bindir}/qemu-system-cris
%{_datadir}/systemtap/tapset/qemu-system-cris*.stp
%{_mandir}/man1/qemu-system-cris.1*


%files system-hppa

%files system-hppa-core
%{_bindir}/qemu-system-hppa
%{_datadir}/systemtap/tapset/qemu-system-hppa*.stp
%{_mandir}/man1/qemu-system-hppa.1*
%{_datadir}/%{name}/hppa-firmware.img


%files system-m68k

%files system-m68k-core
%{_bindir}/qemu-system-m68k
%{_datadir}/systemtap/tapset/qemu-system-m68k*.stp
%{_mandir}/man1/qemu-system-m68k.1*


%files system-microblaze

%files system-microblaze-core
%{_bindir}/qemu-system-microblaze
%{_bindir}/qemu-system-microblazeel
%{_datadir}/systemtap/tapset/qemu-system-microblaze*.stp
%{_mandir}/man1/qemu-system-microblaze.1*
%{_mandir}/man1/qemu-system-microblazeel.1*
%{_datadir}/%{name}/petalogix*.dtb


%files system-mips

%files system-mips-core
%{_bindir}/qemu-system-mips
%{_bindir}/qemu-system-mipsel
%{_bindir}/qemu-system-mips64
%{_bindir}/qemu-system-mips64el
%{_datadir}/systemtap/tapset/qemu-system-mips*.stp
%{_mandir}/man1/qemu-system-mips.1*
%{_mandir}/man1/qemu-system-mipsel.1*
%{_mandir}/man1/qemu-system-mips64el.1*
%{_mandir}/man1/qemu-system-mips64.1*


%files system-nios2
%files system-nios2-core
%{_bindir}/qemu-system-nios2
%{_datadir}/systemtap/tapset/qemu-system-nios2*.stp
%{_mandir}/man1/qemu-system-nios2.1*


%files system-or1k
%files system-or1k-core
%{_bindir}/qemu-system-or1k
%{_datadir}/systemtap/tapset/qemu-system-or1k*.stp
%{_mandir}/man1/qemu-system-or1k.1*

%files system-rx
%files system-rx-core
%{_bindir}/qemu-system-rx
%{_datadir}/systemtap/tapset/qemu-system-rx*.stp
%{_mandir}/man1/qemu-system-rx.1*


%files system-s390x
%files system-s390x-core
%{_bindir}/qemu-system-s390x
%{_datadir}/systemtap/tapset/qemu-system-s390x*.stp
%{_mandir}/man1/qemu-system-s390x.1*
%{_datadir}/%{name}/s390-ccw.img
%{_datadir}/%{name}/s390-netboot.img


%files system-sh4
%files system-sh4-core
%{_bindir}/qemu-system-sh4
%{_bindir}/qemu-system-sh4eb
%{_datadir}/systemtap/tapset/qemu-system-sh4*.stp
%{_mandir}/man1/qemu-system-sh4.1*
%{_mandir}/man1/qemu-system-sh4eb.1*


%files system-tricore
%files system-tricore-core
%{_bindir}/qemu-system-tricore
%{_datadir}/systemtap/tapset/qemu-system-tricore*.stp
%{_mandir}/man1/qemu-system-tricore.1*

%files system-xtensa
%files system-xtensa-core
%{_bindir}/qemu-system-xtensa
%{_bindir}/qemu-system-xtensaeb
%{_datadir}/systemtap/tapset/qemu-system-xtensa*.stp
%{_mandir}/man1/qemu-system-xtensa.1*
%{_mandir}/man1/qemu-system-xtensaeb.1*
%endif

%ifarch x86_64
%files system-x86
%files system-x86-core
%{_bindir}/qemu-system-i386
%{_bindir}/qemu-system-x86_64
%{_libdir}/%{name}/accel-tcg-i386.so
%{_libdir}/%{name}/accel-tcg-x86_64.so
%{_datadir}/systemtap/tapset/qemu-system-i386*.stp
%{_datadir}/systemtap/tapset/qemu-system-x86_64*.stp
%{_mandir}/man1/qemu-system-i386.1*
%{_mandir}/man1/qemu-system-x86_64.1*
%{_datadir}/%{name}/kvmvapic.bin
%{_datadir}/%{name}/linuxboot.bin
%{_datadir}/%{name}/multiboot.bin
%{_datadir}/%{name}/multiboot_dma.bin
%{_datadir}/%{name}/pvh.bin
%{_datadir}/%{name}/qboot.rom
%{_bindir}/qemu-kvm
%{_mandir}/man1/qemu-kvm.1*
%endif

%ifarch ppc64le
%files system-ppc
%files system-ppc-core
%{_bindir}/qemu-system-ppc
%{_bindir}/qemu-system-ppc64
%{_datadir}/systemtap/tapset/qemu-system-ppc*.stp
%{_mandir}/man1/qemu-system-ppc.1*
%{_mandir}/man1/qemu-system-ppc64.1*
%{_datadir}/%{name}/bamboo.dtb
%{_datadir}/%{name}/canyonlands.dtb
%{_datadir}/%{name}/qemu_vga.ndrv
%{_datadir}/%{name}/skiboot.lid
%{_datadir}/%{name}/u-boot.e500
%{_datadir}/%{name}/u-boot-sam460-20100605.bin
%endif

%ifarch riscv
%files system-riscv
%files system-riscv-core
%{_bindir}/qemu-system-riscv32
%{_bindir}/qemu-system-riscv64
%{_datadir}/%{name}/opensbi-riscv*.bin
%{_datadir}/%{name}/opensbi-riscv*.elf
%{_datadir}/systemtap/tapset/qemu-system-riscv*.stp
%{_mandir}/man1/qemu-system-riscv*.1*
%endif


%changelog
* Wed Apr 17 2024 Upgrade Robot <upbot@opencloudos.org> - 8.2.2-1
- Upgrade to version 8.2.2
- fix vnc module display problem, see
- https://gitlab.com/qemu-project/qemu/-/issues/2051

* Mon Mar 25 2024 Mengbiao Xiong <xiongmengbiao@hygon.cn> - 8.2.0-2
- Support hygon tkm key isolation

* Fri Jan 26 2024 Upgrade Robot <upbot@opencloudos.org> - 8.2.0-1
- Upgrade to version 8.2.0

* Mon Dec 11 2023 cunshunxia <cunshunxia@tencent.com> - 8.0.2-13
- fix-CVE-2023-2861

* Wed Nov 08 2023 cunshunxia <cunshunxia@tencent.com> - 8.0.2-12
- fix CVE-2023-5088 CVE-2023-3301

* Thu Oct 19 2023 jackeyji <jackeyji@tencent.com> - 8.0.2-11
- fix CVE-2023-40360 CVE-2023-4135 CVE-2023-3354 CVE-2023-3255 CVE-2023-3180

* Wed Oct 18 2023 jackeyji <jackeyji@tencent.com> - 8.0.2-10
- fix CVE-2023-42467

* Thu Oct 12 2023 Miaojun Dong <zoedong@tencent.com> - 8.0.2-9
- Rebuild for curl-8.4.0

* Fri Sep 08 2023 OpenCloudOS Release Engineering <releng@opencloudos.tech> - 8.0.2-8
- Rebuilt for OpenCloudOS Stream 23.09

* Wed Aug 23 2023 kianli <kianli@tencent.com> - 8.0.2-7
- Rebuilt for device-mapper-multipath 0.9.5

* Tue Aug 22 2023 Shuo Wang <abushwang@tencent.com> - 8.0.2-6
- Rebuilt for ndctl 78

* Fri Aug 18 2023 Miaojun Dong <zoedong@tencent.com> - 8.0.2-5
- Rebuild for ceph-18.2.0

* Thu Aug 17 2023 cunshunxia <cunshunxia@tencent.com> - 8.0.2-4
- Rebuilt for SDL2 2.28.2

* Fri Aug 11 2023 Wang Guodong <gordonwwang@tencent.com> - 8.0.2-3
- Replace pcre-static with pcre2-static, to adjust for glib2 switching

* Mon Jul 17 2023 kianli <kianli@tencent.com> - 8.0.2-2
- Rebuild with libbpf 1.2.0

* Tue Jul 11 2023 cunshunxia <cunshunxia@tencent.com> - 8.0.2-1
- upgrade to 8.0.2.

* Fri Apr 28 2023 OpenCloudOS Release Engineering <releng@opencloudos.tech> - 6.2.0-8
- Rebuilt for OpenCloudOS Stream 23.05

* Fri Mar 31 2023 OpenCloudOS Release Engineering <releng@opencloudos.tech> - 6.2.0-7
- Rebuilt for OpenCloudOS Stream 23

* Tue Feb 14 2023 cunshunxia <cunshunxia@tencent.com> - 6.2.0-6
- qemu-kvm require and build qemu-system-x86/qemu-system-riscv
  only on x86/riscv.

* Thu Feb 9 2023 cunshunxia <cunshunxia@tencent.com> - 6.2.0-5
- require edk2-ovmf only on x86_64.

* Fri Feb 3 2023 cunshunxia <cunshunxia@tencent.com> - 6.2.0-4
- not require ipxe on arm.

* Wed Feb 1 2023 cunshunxia <cunshunxia@tencent.com> - 6.2.0-3
- fix the changelog date error

* Wed Jan 18 2023 cunshunxia <cunshunxia@tencent.com> - 6.2.0-2
- enable ceph on qemu

* Thu Dec 15 2022 cunshunxia <cunshunxia@tencent.com> - 6.2.0-1
- initial build
