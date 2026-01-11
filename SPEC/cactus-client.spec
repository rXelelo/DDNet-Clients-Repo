Name:           cactus-client
Version:        1.14
Release:        3%{?dist}
Summary:        A DDRaceNetwork modification adding new features
License:        Unknown
URL:            https://cactuss.top/
Source0:        https://dw.cactuss.top/%{version}/Cactus-%{version}-public-linux_x86_64.tar.xz
Source1:        https://rxelelo.gitlab.io/rxrepo/rxrepo/os/x86_64/cactus-client.png
ExclusiveArch:  x86_64

# Runtime dependencies
Requires:       freetype
Requires:       opusfile
Requires:       curl
Requires:       glew
Requires:       wavpack
Requires:       (ffmpeg-free or ffmpeg)
Requires:       libnotify
Requires:       miniupnpc
Requires:       sqlite
Requires:       mariadb-connector-c
Requires:       vulkan-loader

# Build dependencies
BuildRequires:  tar
BuildRequires: patchelf

%description
A DDRaceNetwork modification adding new features. DDRaceNetwork is a 
multiplayer racing game based on Teeworlds with additional gameplay 
mechanics and features.

%global debug_package %{nil}
%prep
%setup -c -T
mkdir -p cactus
tar xf %{SOURCE0} -C cactus

%build

%install
install -dm0755 %{buildroot}/opt
install -dm0755 %{buildroot}%{_bindir}
install -dm0755 %{buildroot}%{_datadir}/applications
install -dm0755 %{buildroot}/opt/%{name}

cp -a cactus/* %{buildroot}/opt/%{name}/

chmod +x %{buildroot}/opt/%{name}/Cactus-%{version}-public-linux_x86_64/DDNet

cat > %{buildroot}%{_bindir}/%{name} << 'EOF'
#!/bin/bash
cd /opt/cactus-client/Cactus-1.14-public-linux_x86_64/
exec ./DDNet "$@"
EOF

chmod +x %{buildroot}%{_bindir}/%{name}

cat > %{buildroot}%{_datadir}/applications/%{name}.desktop << 'EOF'
[Desktop Entry]
Name=Cactus Client
Comment=A DDRaceNetwork modification adding new features
Exec=cactus-client
Icon=/opt/cactus-client/cactus-client.png
Terminal=false
Type=Application
Categories=Game;
EOF

install -Dm644 %{SOURCE1} %{buildroot}/opt/%{name}/%{name}.png

for binary in %{buildroot}/opt/cactus-client/Cactus-1.14-public-linux_x86_64/*; do
    if file "$binary" | grep -q "ELF.*executable"; then
        patchelf --set-rpath '$ORIGIN' "$binary" 2>/dev/null || true
    fi
done


%files
/opt/%{name}/
%{_bindir}/%{name}
%{_datadir}/applications/%{name}.desktop

%changelog
* Sun Aug 10 2025 Rain Xelelo <rxelelo@outlook.com> - 1.14-2
- Initial package for Fedora
