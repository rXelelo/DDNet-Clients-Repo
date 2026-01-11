Name:           rclient
Version:        2.1.0
Release:        1%{?dist}
Summary:        Yet another fork of TaterClient for DDNet
License:        Unknown
URL:            https://rushie-client.ru/
Source0:        https://github.com/RushieClient/RushieClient-ddnet/releases/download/V%{version}/RClient-ubuntu.tar.xz
Source1:        https://rxelelo.gitlab.io/rxrepo/rxrepo/os/x86_64/rclient.png
ExclusiveArch:  x86_64

# Runtime dependencies
Requires:       freetype
Requires:       opusfile
Requires:       curl
Requires:       glew
Requires:       wavpack
Requires:       (ffmpeg-free or ffmpeg or libavcodec-free)
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
mkdir -p rclient
tar xf %{SOURCE0} -C rclient

%build

%install
install -dm0755 %{buildroot}/opt
install -dm0755 %{buildroot}%{_bindir}
install -dm0755 %{buildroot}%{_datadir}/applications
install -dm0755 %{buildroot}/opt/%{name}
install -dm0755 %{buildroot}/opt/%{name}/game

cp -a rclient/RClient-*-linux_x86_64/* %{buildroot}/opt/%{name}/game

chmod +x %{buildroot}/opt/%{name}/game/DDNet

cat > %{buildroot}%{_bindir}/%{name} << 'EOF'
#!/bin/bash
cd /opt/%{name}/game/
exec ./DDNet "$@"
EOF

chmod +x %{buildroot}%{_bindir}/%{name}

cat > %{buildroot}%{_datadir}/applications/%{name}.desktop << 'EOF'
[Desktop Entry]
Name=RClient
Comment=A DDRaceNetwork modification adding new features
Exec=%{name}
Icon=/opt/%{name}/%{name}.png
Terminal=false
Type=Application
Categories=Game;
EOF

install -Dm644 %{SOURCE1} %{buildroot}/opt/%{name}/%{name}.png

for binary in %{buildroot}/opt/%{name}/game/*; do
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
